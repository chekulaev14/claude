#!/bin/bash

# SDVG Focus - Полная блокировка отвлечений (сайты + приложения)
# Использование: ./focus.sh [минуты]

# Получаем время в минутах (по умолчанию 60 минут)
MINUTES=${1:-60}
SECONDS=$((MINUTES * 60))

# ============================================
# НАСТРОЙКИ БЛОКИРОВКИ
# ============================================

# Список сайтов для блокировки
BLOCKED_SITES=(
    "vk.com"
    "www.vk.com"
    "youtube.com"
    "www.youtube.com"
    "facebook.com"
    "www.facebook.com"
    "instagram.com"
    "www.instagram.com"
    "twitter.com"
    "www.twitter.com"
    "x.com"
    "www.x.com"
    "reddit.com"
    "www.reddit.com"
    "telegram.org"
    "web.telegram.org"
    "business-gazeta.ru"
    "www.business-gazeta.ru"
    "oboz.info"
    "www.oboz.info"
    "volga.news"
    "www.volga.news"
    "interfax.ru"
    "www.interfax.ru"
    "xnxx-ru.com"
    "www.xnxx-ru.com"
    "tubebdsm.com"
    "www.tubebdsm.com"
    "a1.bluesystem.me"
    "adult.noodlemagazine.com"
    "noodlemagazine.com"
    "www.noodlemagazine.com"
    "avito.ru"
    "www.avito.ru"
)

# Список приложений для блокировки
BLOCKED_APPS=(
    "Telegram"
    "Mail"
    "Messages"
)

# ============================================
# СИСТЕМНЫЕ ПЕРЕМЕННЫЕ
# ============================================

HOSTS_FILE="/etc/hosts"
BACKUP_FILE="/tmp/hosts.backup"
MARKER="# SDVG_FOCUS_BLOCK"
STOP_FLAG="/tmp/sdvg_stop_watchdog"

# ============================================
# ФУНКЦИИ БЛОКИРОВКИ САЙТОВ
# ============================================

block_sites() {
    echo "🌐 Блокирую отвлекающие сайты..."

    # Создаем backup
    sudo cp $HOSTS_FILE $BACKUP_FILE

    # Добавляем блокировки
    echo "" | sudo tee -a $HOSTS_FILE > /dev/null
    echo "$MARKER - START" | sudo tee -a $HOSTS_FILE > /dev/null

    for site in "${BLOCKED_SITES[@]}"; do
        echo "127.0.0.1 $site $MARKER" | sudo tee -a $HOSTS_FILE > /dev/null
        echo "  ✓ $site"
    done

    echo "$MARKER - END" | sudo tee -a $HOSTS_FILE > /dev/null

    # Сбрасываем DNS кеш
    sudo dscacheutil -flushcache
    sudo killall -HUP mDNSResponder

    echo "✅ Сайты заблокированы!"
}

unblock_sites() {
    echo ""
    echo "🌐 Разблокирую сайты..."

    # Удаляем все строки с нашим маркером
    sudo sed -i '' "/$MARKER/d" $HOSTS_FILE

    # Сбрасываем DNS кеш
    sudo dscacheutil -flushcache
    sudo killall -HUP mDNSResponder

    echo "✅ Сайты разблокированы!"
}

# ============================================
# ФУНКЦИИ БЛОКИРОВКИ ПРИЛОЖЕНИЙ
# ============================================

close_apps() {
    echo ""
    echo "📱 Блокирую приложения..."
    for app in "${BLOCKED_APPS[@]}"; do
        if pgrep -x "$app" > /dev/null; then
            echo "  ✓ $app"
            killall "$app" 2>/dev/null
        fi
    done
    echo "✅ Приложения закрыты!"
}

watchdog() {
    while [ ! -f "$STOP_FLAG" ]; do
        for app in "${BLOCKED_APPS[@]}"; do
            if pgrep -x "$app" > /dev/null; then
                killall "$app" 2>/dev/null
                osascript -e "display notification \"$app заблокирован во время фокуса\" with title \"🚫 SDVG Focus\"" 2>/dev/null
            fi
        done
        sleep 2
    done
}

stop_apps_blocking() {
    echo ""
    echo "📱 Разблокирую приложения..."
    touch $STOP_FLAG
    sleep 1
    echo "✅ Приложения разблокированы!"
}

# ============================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================

start_focus() {
    # Удаляем старый флаг остановки
    rm -f $STOP_FLAG

    echo "╔════════════════════════════════════════╗"
    echo "║       🎯 SDVG FOCUS MODE               ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    echo "⏱️  Время: $MINUTES минут(ы)"
    echo ""

    # Блокируем сайты
    block_sites

    # Закрываем приложения
    close_apps

    # Запускаем watchdog в фоне
    echo ""
    echo "👁️  Запускаю мониторинг приложений..."
    watchdog &
    WATCHDOG_PID=$!

    # Запускаем TickTick Pomodoro
    echo ""
    echo "⏰ Открываю TickTick Pomodoro..."

    # Открываем TickTick на странице Focus
    open "ticktick://focus"

    # Показываем уведомление
    osascript -e "display notification \"Установи таймер на $MINUTES минут в TickTick\" with title \"⏰ TickTick Pomodoro\"" 2>/dev/null

    echo "✅ TickTick открыт - установи таймер на $MINUTES минут"

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ ФОКУС РЕЖИМ АКТИВИРОВАН"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Заблокировано:"
    echo "  🌐 Сайтов: ${#BLOCKED_SITES[@]}"
    echo "  📱 Приложений: ${#BLOCKED_APPS[@]}"
    echo "  ⏰ Таймер: TickTick Pomodoro ($MINUTES мин)"
    echo ""
    echo "⏸️  Для остановки нажмите Ctrl+C"
    echo ""

    # Уведомление
    osascript -e "display notification \"Фокус режим на $MINUTES мин\" with title \"🎯 SDVG Focus\"" 2>/dev/null

    # Ждем
    sleep $SECONDS

    # Останавливаем
    stop_apps_blocking
    kill $WATCHDOG_PID 2>/dev/null
    unblock_sites

    # Финальное уведомление
    osascript -e "display notification \"Время вышло! Оцени результат\" with title \"⏰ SDVG Focus\"" 2>/dev/null

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎉 СЕССИЯ ЗАВЕРШЕНА!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

cleanup() {
    echo ""
    echo "⚠️  Прерывание..."
    stop_apps_blocking
    kill $WATCHDOG_PID 2>/dev/null
    unblock_sites
    echo ""
}

# Обработчик прерывания
trap cleanup EXIT INT TERM

# Запуск
start_focus
