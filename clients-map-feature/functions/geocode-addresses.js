/**
 * Netlify Function для геокодирования городов через Google Maps API
 * Создает карту с кластерами (несколько клиентов в одном городе)
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Путь к файлам данных
const INPUT_FILE = path.join(__dirname, '../../assets/data/clients-with-addresses.json');
const OUTPUT_FILE = path.join(__dirname, '../../assets/data/clients-map-data.json');

// Google Maps API ключ (тот же что используется на сайте)
const GOOGLE_API_KEY = 'AIzaSyAeGxooF2L5rdIFszMLZBYhcVhT11u83MY';

// Секретный токен
const SECRET_TOKEN = process.env.GEOCODE_TOKEN || 'change-me-in-production';

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
    // Проверить что есть данные с адресами
    if (!fs.existsSync(INPUT_FILE)) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          error: 'Сначала нужно собрать адреса через fetch-client-addresses'
        })
      };
    }

    // Загрузить данные
    const clientsWithAddresses = JSON.parse(fs.readFileSync(INPUT_FILE, 'utf8'));

    // Сгруппировать клиентов по городам
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

    console.log(`Найдено ${citiesMap.size} уникальных городов`);

    // Геокодировать уникальные города
    const results = [];
    let processed = 0;

    for (const [cityKey, cityData] of citiesMap) {
      try {
        const coords = await geocodeCity(cityData.city, cityData.region);

        if (coords) {
          results.push({
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

        // Задержка между запросами (100мс)
        await new Promise(resolve => setTimeout(resolve, 100));

      } catch (error) {
        console.error(`Ошибка для ${cityData.city}:`, error.message);
      }
    }

    // Сохранить результаты
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(results, null, 2));

    // Также создать упрощенную версию для быстрой загрузки на карте
    const simplifiedData = results.map(r => ({
      city: r.city,
      region: r.region,
      lat: r.lat,
      lng: r.lng,
      count: r.count
    }));

    fs.writeFileSync(
      path.join(__dirname, '../../assets/data/clients-map-simple.json'),
      JSON.stringify(simplifiedData, null, 2)
    );

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        success: true,
        totalCities: citiesMap.size,
        geocoded: processed,
        totalClients: clientsWithAddresses.length,
        outputFile: 'clients-map-data.json'
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
