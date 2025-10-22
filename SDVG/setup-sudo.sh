#!/bin/bash

# Скрипт для настройки sudo без пароля для focus.sh
# Запускать ОДИН РАЗ: sudo ./setup-sudo.sh

echo "🔧 Настройка sudo для focus.sh..."
echo ""

# Получаем текущего пользователя
CURRENT_USER=$(whoami)

# Путь к скрипту
SCRIPT_PATH="/Users/petrcekulaev/Desktop/CLAUDE/SDVG/focus.sh"

# Создаем sudoers файл для нашего скрипта
SUDOERS_FILE="/etc/sudoers.d/sdvg-focus"

# Команды которым нужен sudo без пароля
SUDO_COMMANDS="
# SDVG Focus Block - команды без пароля
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/cp /etc/hosts /tmp/hosts.backup
$CURRENT_USER ALL=(ALL) NOPASSWD: /usr/bin/tee -a /etc/hosts
$CURRENT_USER ALL=(ALL) NOPASSWD: /usr/bin/sed -i * /etc/hosts
$CURRENT_USER ALL=(ALL) NOPASSWD: /usr/bin/dscacheutil -flushcache
$CURRENT_USER ALL=(ALL) NOPASSWD: /usr/bin/killall -HUP mDNSResponder
"

# Создаем файл
echo "$SUDO_COMMANDS" | sudo tee $SUDOERS_FILE > /dev/null

# Устанавливаем правильные права
sudo chmod 0440 $SUDOERS_FILE

# Проверяем синтаксис
if sudo visudo -c -f $SUDOERS_FILE; then
    echo "✅ Настройка завершена!"
    echo ""
    echo "Теперь можно запускать:"
    echo "  ./focus.sh"
    echo ""
    echo "Без ввода пароля!"
else
    echo "❌ Ошибка в конфигурации!"
    sudo rm $SUDOERS_FILE
    exit 1
fi
