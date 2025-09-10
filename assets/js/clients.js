/**
 * Система управления клиентами ТК Динамика
 * Функционал: сортировка, поиск, пагинация, алфавитная навигация
 */

class ClientsManager {
    constructor() {
        this.clients = [];
        this.filteredClients = [];
        this.currentPage = 1;
        this.itemsPerPage = 20;
        this.selectedLetter = 'А';

        this.init();
    }

    async init() {
        await this.loadClients();
        this.setupEventListeners();
        this.createAlphabetNavigation();
        this.applyFilters(); // Применяем фильтр по умолчанию (А)
    }

    async loadClients() {
        try {
            const response = await fetch('../assets/data/clients.json');
            this.clients = await response.json();
            
            // Очистка данных - убираем лишние пробелы из имен
            this.clients = this.clients.map(client => ({
                ...client,
                name: client.name.trim(),
                inn: Math.round(client.inn).toString()
            }));

            this.filteredClients = [...this.clients];
            
            console.log(`Загружено ${this.clients.length} клиентов`);
        } catch (error) {
            console.error('Ошибка загрузки данных:', error);
            this.showError('Не удалось загрузить данные клиентов');
        }
    }

    setupEventListeners() {
        // Event listeners setup - currently empty as search and sorting removed
    }

    createAlphabetNavigation() {
        const alphabetNav = document.getElementById('alphabetNav');
        const letters = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'.split('');
        
        // Кнопки букв
        letters.forEach(letter => {
            const btn = document.createElement('button');
            btn.className = `btn btn-outline-primary btn-sm ${letter === 'А' ? 'active' : ''}`;
            btn.textContent = letter;
            btn.addEventListener('click', () => this.filterByLetter(letter));
            alphabetNav.appendChild(btn);
        });
    }

    filterByLetter(letter) {
        this.selectedLetter = letter;
        this.currentPage = 1;
        
        // Обновляем активную кнопку
        document.querySelectorAll('#alphabetNav .btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.textContent === letter) {
                btn.classList.add('active');
            }
        });

        this.applyFilters();
    }

    applyFilters() {
        let filtered = [...this.clients];

        // Фильтр по букве
        if (this.selectedLetter) {
            filtered = filtered.filter(client => 
                client.name.toUpperCase().startsWith(this.selectedLetter)
            );
        }

        this.filteredClients = filtered;
        this.currentPage = 1;
        this.renderClients();
    }


    renderClients() {
        const clientsList = document.getElementById('clientsList');
        const loadingSpinner = document.getElementById('loadingSpinner');
        
        // Скрываем спиннер
        loadingSpinner.style.display = 'none';

        // Рассчитываем пагинацию
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        const clientsToShow = this.filteredClients.slice(startIndex, endIndex);

        // Очищаем контейнер
        clientsList.innerHTML = '';

        // Отображаем клиентов
        if (clientsToShow.length === 0) {
            clientsList.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-warning text-center">
                        <h5>Клиенты не найдены</h5>
                        <p>Попробуйте изменить критерии поиска</p>
                    </div>
                </div>
            `;
        } else {
            clientsToShow.forEach((client, index) => {
                const clientCard = this.createClientCard(client, startIndex + index + 1);
                clientsList.appendChild(clientCard);
            });
        }

        // Обновляем статистику
        this.updateStatistics();
        
        // Обновляем пагинацию
        this.renderPagination();
    }

    createClientCard(client, index) {
        const div = document.createElement('div');
        div.className = 'col-md-6 col-lg-4 mb-3';
        
        div.innerHTML = `
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-secondary">#${index}</span>
                        <small class="text-muted">${client.inn}</small>
                    </div>
                    <h6 class="card-title">${client.name}</h6>
                    <div class="mt-auto pt-2">
                        <small class="text-muted">
                            <i class="bi bi-building"></i>
                            ИНН: ${client.inn}
                        </small>
                    </div>
                </div>
            </div>
        `;
        
        return div;
    }

    updateStatistics() {
        document.getElementById('totalClients').textContent = this.clients.length;
        document.getElementById('shownClients').textContent = this.filteredClients.length;
        document.getElementById('currentPage').textContent = this.currentPage;
        document.getElementById('totalPages').textContent = Math.ceil(this.filteredClients.length / this.itemsPerPage);
    }

    renderPagination() {
        const pagination = document.getElementById('pagination');
        const totalPages = Math.ceil(this.filteredClients.length / this.itemsPerPage);
        
        pagination.innerHTML = '';

        if (totalPages <= 1) return;

        // Предыдущая страница
        if (this.currentPage > 1) {
            const prevLi = document.createElement('li');
            prevLi.className = 'page-item';
            prevLi.innerHTML = `<a class="page-link" href="#" data-page="${this.currentPage - 1}">Предыдущая</a>`;
            pagination.appendChild(prevLi);
        }

        // Номера страниц
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(totalPages, this.currentPage + 2);

        for (let i = startPage; i <= endPage; i++) {
            const li = document.createElement('li');
            li.className = `page-item ${i === this.currentPage ? 'active' : ''}`;
            li.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
            pagination.appendChild(li);
        }

        // Следующая страница
        if (this.currentPage < totalPages) {
            const nextLi = document.createElement('li');
            nextLi.className = 'page-item';
            nextLi.innerHTML = `<a class="page-link" href="#" data-page="${this.currentPage + 1}">Следующая</a>`;
            pagination.appendChild(nextLi);
        }

        // Обработчики кликов по страницам
        pagination.addEventListener('click', (e) => {
            e.preventDefault();
            if (e.target.tagName === 'A' && e.target.dataset.page) {
                this.currentPage = parseInt(e.target.dataset.page);
                this.renderClients();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    }

    showError(message) {
        const clientsList = document.getElementById('clientsList');
        const loadingSpinner = document.getElementById('loadingSpinner');
        
        loadingSpinner.style.display = 'none';
        clientsList.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger">
                    <h5>Ошибка загрузки</h5>
                    <p>${message}</p>
                </div>
            </div>
        `;
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new ClientsManager();
});