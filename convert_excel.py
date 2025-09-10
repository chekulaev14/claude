#!/usr/bin/env python3
import pandas as pd
import json
import sys

def convert_excel_to_json(excel_file, output_file):
    """
    Конвертирует Excel файл в JSON формат для использования на веб-странице
    """
    try:
        # Читаем Excel файл без заголовков, первая строка - это данные
        df = pd.read_excel(excel_file, engine='openpyxl', header=None)
        # Назначаем правильные названия колонок
        df.columns = ['name', 'inn']
        
        # Выводим информацию о структуре данных
        print(f"Найдено {len(df)} записей")
        print(f"Колонки: {list(df.columns)}")
        print("\nПервые 3 записи:")
        print(df.head(3).to_string())
        
        # Конвертируем NaN в пустые строки
        df = df.fillna('')
        
        # Конвертируем в список словарей
        clients = df.to_dict('records')
        
        # Сохраняем в JSON файл
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(clients, f, ensure_ascii=False, indent=2)
        
        print(f"\nДанные сохранены в {output_file}")
        return clients
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    clients = convert_excel_to_json("sheet.xlsx", "assets/data/clients.json")