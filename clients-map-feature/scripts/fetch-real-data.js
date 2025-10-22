/**
 * Скрипт для сбора реальных данных клиентов
 * Запрашивает адреса по ИНН и геокодирует их
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const zlib = require('zlib');

// Пути к файлам
const CLIENTS_FILE = path.join(__dirname, '../../assets/data/clients.json');
const OUTPUT_DIR = path.join(__dirname, '../assets/data');
const PROGRESS_FILE = path.join(__dirname, '../progress.json');

// Google Maps API ключ
const GOOGLE_API_KEY = 'AIzaSyAeGxooF2L5rdIFszMLZBYhcVhT11u83MY';

/**
 * Получить данные по ИНН из egrul.itsoft.ru
 */
function fetchInnData(inn) {
  return new Promise((resolve, reject) => {
    const url = `https://egrul.itsoft.ru/short_data/?${inn}`;

    https.get(url, (res) => {
      const isGzipped = res.headers['content-encoding'] === 'gzip';
      let stream = res;

      // Если ответ сжат gzip, распаковываем
      if (isGzipped) {
        stream = res.pipe(zlib.createGunzip());
      }

      let data = '';

      stream.on('data', (chunk) => {
        data += chunk.toString();
      });

      stream.on('end', () => {
        try {
          const result = JSON.parse(data);
          resolve(result);
        } catch (error) {
          reject(error);
        }
      });

      stream.on('error', reject);
    }).on('error', reject);
  });
}

/**
 * Геокодирование города через Google Maps API
 */
function geocodeCity(city, region) {
  return new Promise((resolve, reject) => {
    const query = region ? `${city}, ${region}, Россия` : `${city}, Россия`;
    const encodedQuery = encodeURIComponent(query);
    const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodedQuery}&key=${GOOGLE_API_KEY}&language=ru`;

    https.get(url, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const result = JSON.parse(data);

          if (result.status === 'OK' && result.results.length > 0) {
            const location = result.results[0].geometry.location;
            resolve({
              lat: location.lat,
              lng: location.lng
            });
          } else {
            resolve(null);
          }
        } catch (error) {
          reject(error);
        }
      });
    }).on('error', reject);
  });
}

/**
 * Основная функция
 */
async function main() {
  console.log('🚀 Начинаем сбор данных...\n');

  // Загрузить клиентов
  const clients = JSON.parse(fs.readFileSync(CLIENTS_FILE, 'utf8'));

  // Фильтровать клиентов с валидными ИНН
  const validClients = clients.filter(c =>
    c.inn && c.inn !== '0' && c.inn !== 0
  );

  // Загрузить прогресс
  let progress = { lastProcessedIndex: -1, processedCompanies: [] };
  if (fs.existsSync(PROGRESS_FILE)) {
    progress = JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8'));
  }

  const startIndex = progress.lastProcessedIndex + 1;
  const batchSize = 95;
  const endIndex = Math.min(startIndex + batchSize, validClients.length);

  console.log(`📊 Всего клиентов: ${clients.length}`);
  console.log(`✅ С валидными ИНН: ${validClients.length}`);
  console.log(`📍 Последний обработанный индекс: ${progress.lastProcessedIndex}`);
  console.log(`📍 Будем обрабатывать: ${endIndex - startIndex} клиентов (индексы ${startIndex}-${endIndex - 1})\n`);

  // Взять batch начиная с startIndex
  const batch = validClients.slice(startIndex, endIndex);

  // Шаг 1: Собрать адреса
  console.log('--- ЭТАП 1: Сбор адресов ---\n');
  const clientsWithAddresses = [];

  for (let i = 0; i < batch.length; i++) {
    const client = batch[i];
    const globalIndex = startIndex + i;

    try {
      const data = await fetchInnData(client.inn);

      if (data && data.address) {
        const clientData = {
          name: client.name,
          inn: client.inn.toString(),
          address: data.address,
          region: data.address_struct?.region || '',
          city: data.address_struct?.city || data.address_struct?.region || ''
        };

        clientsWithAddresses.push(clientData);
        console.log(`✓ [${i + 1}/${batch.length}] ${client.name}: ${clientData.city}`);

        // Обновить прогресс
        progress.processedCompanies.push({
          index: globalIndex,
          name: client.name,
          inn: client.inn.toString()
        });
      } else {
        console.log(`✗ [${i + 1}/${batch.length}] ${client.name}: адрес не найден`);
      }

      // Обновить lastProcessedIndex
      progress.lastProcessedIndex = globalIndex;
      progress.lastProcessedCompany = client.name;
      progress.lastProcessedInn = client.inn.toString();
      progress.totalProcessed = progress.processedCompanies.length;
      progress.totalInFile = validClients.length;
      progress.remaining = validClients.length - globalIndex - 1;
      progress.note = `Обработаны компании с индексами ${startIndex}-${globalIndex}. Следующий запуск начнётся с индекса ${globalIndex + 1}.`;
      progress.lastUpdate = new Date().toISOString();

      // Сохранить прогресс
      fs.writeFileSync(PROGRESS_FILE, JSON.stringify(progress, null, 2));

      // Задержка между запросами (300мс)
      await new Promise(resolve => setTimeout(resolve, 300));

    } catch (error) {
      console.error(`✗ [${i + 1}/${batch.length}] ${client.name}: ${error.message}`);
    }
  }

  console.log(`\n✅ Собрано адресов: ${clientsWithAddresses.length}\n`);

  // Шаг 2: Сгруппировать по городам
  console.log('--- ЭТАП 2: Группировка по городам ---\n');
  const citiesMap = new Map();

  clientsWithAddresses.forEach(client => {
    const cityKey = client.city || client.region || 'Неизвестно';

    if (!citiesMap.has(cityKey)) {
      citiesMap.set(cityKey, {
        city: cityKey,
        region: client.region,
        clients: [],
        count: 0
      });
    }

    citiesMap.get(cityKey).clients.push({
      name: client.name,
      inn: client.inn
    });
    citiesMap.get(cityKey).count++;
  });

  console.log(`📍 Найдено уникальных городов: ${citiesMap.size}\n`);

  // Шаг 3: Геокодировать города
  console.log('--- ЭТАП 3: Геокодирование ---\n');
  const mapData = [];

  let processed = 0;
  for (const [cityKey, cityData] of citiesMap) {
    try {
      const coords = await geocodeCity(cityData.city, cityData.region);

      if (coords) {
        mapData.push({
          city: cityData.city,
          region: cityData.region,
          lat: coords.lat,
          lng: coords.lng,
          count: cityData.count,
          clients: cityData.clients
        });

        console.log(`✓ ${cityData.city}: ${cityData.count} клиентов [${coords.lat}, ${coords.lng}]`);
        processed++;
      } else {
        console.log(`✗ ${cityData.city}: не удалось геокодировать`);
      }

      // Задержка между запросами (200мс)
      await new Promise(resolve => setTimeout(resolve, 200));

    } catch (error) {
      console.error(`✗ ${cityData.city}: ${error.message}`);
    }
  }

  console.log(`\n✅ Геокодировано городов: ${processed}\n`);

  // Сохранить результаты
  console.log('--- ЭТАП 4: Сохранение данных ---\n');

  // Полные данные - ОБЪЕДИНЯЕМ с существующими
  const fullDataPath = path.join(OUTPUT_DIR, 'clients-map-data.json');
  let existingData = [];

  if (fs.existsSync(fullDataPath)) {
    existingData = JSON.parse(fs.readFileSync(fullDataPath, 'utf8'));
    console.log(`📂 Загружены существующие данные: ${existingData.length} городов`);
  }

  // Объединяем данные по городам
  const mergedMap = new Map();

  // Добавляем существующие данные
  existingData.forEach(city => {
    const key = `${city.city}|${city.region}`;
    mergedMap.set(key, city);
  });

  // Добавляем/обновляем новыми данными
  mapData.forEach(city => {
    const key = `${city.city}|${city.region}`;

    if (mergedMap.has(key)) {
      // Город уже есть - объединяем клиентов
      const existing = mergedMap.get(key);
      const existingInns = new Set(existing.clients.map(c => c.inn));

      // Добавляем только новых клиентов (по ИНН)
      city.clients.forEach(client => {
        if (!existingInns.has(client.inn)) {
          existing.clients.push(client);
          existingInns.add(client.inn);
        }
      });

      existing.count = existing.clients.length;
    } else {
      // Новый город - добавляем целиком
      mergedMap.set(key, city);
    }
  });

  const mergedData = Array.from(mergedMap.values());

  fs.writeFileSync(fullDataPath, JSON.stringify(mergedData, null, 2));
  console.log(`✓ Сохранено: clients-map-data.json`);

  // Упрощенные данные (без списка клиентов)
  const simpleData = mergedData.map(r => ({
    city: r.city,
    region: r.region,
    lat: r.lat,
    lng: r.lng,
    count: r.count
  }));

  const simpleDataPath = path.join(OUTPUT_DIR, 'clients-map-simple.json');
  fs.writeFileSync(simpleDataPath, JSON.stringify(simpleData, null, 2));
  console.log(`✓ Сохранено: clients-map-simple.json`);

  // Статистика
  const totalClients = mergedData.reduce((sum, city) => sum + city.count, 0);
  const uniqueRegions = new Set(mergedData.map(city => city.region)).size;
  const newClients = mapData.reduce((sum, city) => sum + city.count, 0);

  console.log('\n--- ИТОГО ---');
  console.log(`➕ Новых клиентов в этом запуске: ${newClients}`);
  console.log(`📊 Всего клиентов на карте: ${totalClients}`);
  console.log(`📍 Городов: ${mergedData.length}`);
  console.log(`🗺️  Регионов: ${uniqueRegions}`);
  console.log('\n✅ Готово!');
}

// Запуск
main().catch(console.error);
