/**
 * Netlify Function для сбора адресов клиентов по ИНН
 * Обрабатывает 85 клиентов в день через API egrul.itsoft.ru
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const zlib = require('zlib');

// Путь к файлам данных
const CLIENTS_FILE = path.join(__dirname, '../../assets/data/clients.json');
const PROGRESS_FILE = path.join(__dirname, '../../assets/data/clients-addresses-progress.json');
const OUTPUT_FILE = path.join(__dirname, '../../assets/data/clients-with-addresses.json');

// Лимит запросов в день
const DAILY_LIMIT = 85;

// Секретный токен для защиты endpoint
const SECRET_TOKEN = process.env.FETCH_ADDRESSES_TOKEN || 'change-me-in-production';

/**
 * Получить данные по ИНН из egrul.itsoft.ru
 */
function fetchInnData(inn) {
  return new Promise((resolve, reject) => {
    const url = `https://egrul.itsoft.ru/short_data/?${inn}`;

    https.get(url, {
      headers: {
        'Accept-encoding': 'gzip'
      }
    }, (res) => {
      const chunks = [];
      const gunzip = zlib.createGunzip();

      res.pipe(gunzip);

      gunzip.on('data', (chunk) => {
        chunks.push(chunk);
      });

      gunzip.on('end', () => {
        try {
          const data = JSON.parse(Buffer.concat(chunks).toString());
          resolve(data);
        } catch (error) {
          reject(error);
        }
      });

      gunzip.on('error', reject);
    }).on('error', reject);
  });
}

/**
 * Загрузить или создать файл прогресса
 */
function loadProgress() {
  try {
    if (fs.existsSync(PROGRESS_FILE)) {
      return JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8'));
    }
  } catch (error) {
    console.error('Ошибка загрузки прогресса:', error);
  }

  return {
    processedInns: [],
    lastRun: null,
    totalProcessed: 0
  };
}

/**
 * Сохранить прогресс
 */
function saveProgress(progress) {
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(progress, null, 2));
}

/**
 * Загрузить существующие данные с адресами
 */
function loadExistingData() {
  try {
    if (fs.existsSync(OUTPUT_FILE)) {
      return JSON.parse(fs.readFileSync(OUTPUT_FILE, 'utf8'));
    }
  } catch (error) {
    console.error('Ошибка загрузки существующих данных:', error);
  }
  return [];
}

/**
 * Основная функция
 */
exports.handler = async (event, context) => {
  // Проверка токена
  const token = event.queryStringParameters?.token;
  if (token !== SECRET_TOKEN) {
    return {
      statusCode: 401,
      body: JSON.stringify({ error: 'Unauthorized' })
    };
  }

  try {
    // Загрузить данные
    const clients = JSON.parse(fs.readFileSync(CLIENTS_FILE, 'utf8'));
    const progress = loadProgress();
    const existingData = loadExistingData();

    // Фильтровать клиентов с валидными ИНН (не ИП)
    const validClients = clients.filter(c =>
      c.inn && c.inn !== '0' && c.inn !== 0 && !progress.processedInns.includes(c.inn.toString())
    );

    // Взять следующие 85 клиентов
    const batch = validClients.slice(0, DAILY_LIMIT);

    if (batch.length === 0) {
      return {
        statusCode: 200,
        body: JSON.stringify({
          message: 'Все клиенты обработаны',
          totalProcessed: progress.totalProcessed
        })
      };
    }

    console.log(`Обработка ${batch.length} клиентов...`);

    // Обработать пачку
    const results = [];
    for (const client of batch) {
      try {
        const data = await fetchInnData(client.inn);

        if (data && data.address) {
          results.push({
            name: client.name,
            inn: client.inn.toString(),
            address: data.address,
            addressStruct: data.address_struct,
            region: data.address_struct?.region || '',
            city: data.address_struct?.city || data.address_struct?.region || ''
          });

          console.log(`✓ ${client.name}: ${data.address}`);
        }

        // Добавить в обработанные
        progress.processedInns.push(client.inn.toString());

        // Задержка между запросами (100мс)
        await new Promise(resolve => setTimeout(resolve, 100));

      } catch (error) {
        console.error(`Ошибка для ${client.name}:`, error.message);
        // Всё равно добавляем в обработанные, чтобы не застревать
        progress.processedInns.push(client.inn.toString());
      }
    }

    // Обновить прогресс
    progress.lastRun = new Date().toISOString();
    progress.totalProcessed += results.length;
    saveProgress(progress);

    // Объединить с существующими данными
    const allData = [...existingData, ...results];
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(allData, null, 2));

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        success: true,
        processed: results.length,
        totalProcessed: progress.totalProcessed,
        remaining: validClients.length - batch.length,
        lastRun: progress.lastRun
      })
    };

  } catch (error) {
    console.error('Ошибка:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        error: error.message
      })
    };
  }
};
