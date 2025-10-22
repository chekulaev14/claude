/**
 * Интерактивная карта клиентов ТК Динамика
 */

let map;
let markers = [];
let infoWindow;

/**
 * Инициализация карты (вызывается Google Maps API)
 */
function initMap() {
    // Центр России
    const centerRussia = { lat: 55.7558, lng: 48.6173 };

    // Создать карту
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: centerRussia,
        styles: [
            {
                featureType: 'poi',
                elementType: 'labels',
                stylers: [{ visibility: 'off' }]
            }
        ]
    });

    // Создать info window
    infoWindow = new google.maps.InfoWindow();

    // Слушатель изменения зума для масштабирования маркеров
    map.addListener('zoom_changed', () => {
        updateMarkerScale();
    });

    // Загрузить данные клиентов
    loadClientsData();
}

/**
 * Загрузить данные клиентов
 */
async function loadClientsData() {
    try {
        const response = await fetch('../assets/data/clients-map-simple.json');

        if (!response.ok) {
            throw new Error('Данные карты еще не готовы. Запустите функции сбора данных.');
        }

        const data = await response.json();

        // Обновить статистику
        updateStatistics(data);

        // Добавить маркеры на карту
        addMarkersToMap(data);

        // Показать карту
        document.getElementById('loading').style.display = 'none';
        document.getElementById('map').style.display = 'block';

    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        document.getElementById('loading').innerHTML = `
            <div class="alert alert-warning">
                <h5>Данные карты еще не готовы</h5>
                <p>${error.message}</p>
                <p class="mb-0">Обратитесь к администратору для запуска сбора данных клиентов.</p>
            </div>
        `;
    }
}

/**
 * Обновить статистику
 */
function updateStatistics(data) {
    const totalClients = data.reduce((sum, city) => sum + city.count, 0);
    const totalCities = data.length;
    const uniqueRegions = new Set(data.map(city => city.region)).size;

    document.getElementById('totalClients').textContent = totalClients;
    document.getElementById('totalCities').textContent = totalCities;
    document.getElementById('totalRegions').textContent = uniqueRegions;
}

/**
 * Получить цвет маркера по количеству клиентов
 */
function getMarkerColor(count) {
    if (count >= 50) return '#8b5cf6'; // Фиолетовый
    if (count >= 11) return '#3b82f6'; // Синий
    return '#10b981'; // Зеленый
}

/**
 * Обновить масштаб маркеров при изменении зума
 */
function updateMarkerScale() {
    const zoom = map.getZoom();
    const defaultZoom = 4; // Начальный зум

    // Рассчитать масштаб: при зуме больше defaultZoom - уменьшаем маркеры
    let scale;
    if (zoom <= defaultZoom) {
        // При отдалении или дефолтном зуме - базовый размер
        scale = 1.5;
    } else {
        // При приближении - уменьшаем маркеры
        // Формула: чем больше зум, тем меньше маркер
        scale = 1.5 / (1 + (zoom - defaultZoom) * 0.15);
    }

    // Обновить все маркеры
    markers.forEach(marker => {
        const currentIcon = marker.getIcon();
        if (currentIcon && currentIcon.path) {
            marker.setIcon({
                ...currentIcon,
                scale: scale
            });
        }
    });
}

/**
 * Добавить маркеры на карту
 */
function addMarkersToMap(data) {
    data.forEach(city => {
        const position = { lat: city.lat, lng: city.lng };
        const color = getMarkerColor(city.count);

        // Создать SVG маркер с числом
        const svgMarker = {
            path: 'M 0,0 C -2,-20 -10,-22 -10,-30 A 10,10 0 1,1 10,-30 C 10,-22 2,-20 0,0 z',
            fillColor: color,
            fillOpacity: 1,
            strokeColor: '#ffffff',
            strokeWeight: 2,
            scale: 1.5,
            anchor: new google.maps.Point(0, 0),
            labelOrigin: new google.maps.Point(0, -28)
        };

        // Создать маркер
        const marker = new google.maps.Marker({
            position: position,
            map: map,
            icon: svgMarker,
            title: `${city.city}: ${city.count} клиентов`,
            label: {
                text: city.count.toString(),
                color: '#ffffff',
                fontSize: '12px',
                fontWeight: 'bold'
            }
        });

        // Добавить слушатель клика
        marker.addListener('click', () => {
            showCityInfo(city, marker);
        });

        markers.push(marker);
    });

    // Подогнать карту под все маркеры
    if (markers.length > 0) {
        const bounds = new google.maps.LatLngBounds();
        markers.forEach(marker => {
            bounds.extend(marker.getPosition());
        });
        map.fitBounds(bounds);
    }
}

/**
 * Показать информацию о городе
 */
async function showCityInfo(city, marker) {
    try {
        // Загрузить полные данные с именами клиентов
        const response = await fetch('../assets/data/clients-map-data.json');
        const fullData = await response.json();

        // Найти данные по городу
        const cityData = fullData.find(c => c.city === city.city && c.region === city.region);

        if (cityData && cityData.clients) {
            // Создать HTML с именами клиентов
            const clientsList = cityData.clients
                .slice(0, 10) // Показать первые 10
                .map(client => `<li>${client.name}</li>`)
                .join('');

            const moreText = cityData.clients.length > 10
                ? `<p class="mb-0"><small>и еще ${cityData.clients.length - 10} клиентов...</small></p>`
                : '';

            const content = `
                <div style="max-width: 300px;">
                    <h5 class="mb-2">${city.city}</h5>
                    <p class="mb-2"><strong>${city.count}</strong> клиентов</p>
                    <hr class="my-2">
                    <ul class="mb-2" style="padding-left: 20px; max-height: 200px; overflow-y: auto;">
                        ${clientsList}
                    </ul>
                    ${moreText}
                </div>
            `;

            infoWindow.setContent(content);
            infoWindow.open(map, marker);
        }
    } catch (error) {
        console.error('Ошибка загрузки данных клиентов:', error);

        // Показать базовую информацию
        const content = `
            <div style="max-width: 250px;">
                <h5 class="mb-2">${city.city}</h5>
                <p class="mb-0"><strong>${city.count}</strong> клиентов</p>
            </div>
        `;

        infoWindow.setContent(content);
        infoWindow.open(map, marker);
    }
}

/**
 * Инициализация при загрузке страницы
 */
document.addEventListener('DOMContentLoaded', () => {
    // Карта инициализируется через callback от Google Maps API
    console.log('Страница загружена, ожидаем Google Maps API...');
});
