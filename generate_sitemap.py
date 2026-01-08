#!/usr/bin/env python3
"""Генератор sitemap.xml для dinamika-cargo.ru"""

import os
from datetime import datetime

BASE_URL = "https://dinamika-cargo.ru"
TODAY = datetime.now().strftime("%Y-%m-%d")

def main():
    urls = []
    
    # Главная страница
    urls.append("")
    
    # Региональные страницы
    for root, dirs, files in os.walk("regions"):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file == "index.html":
                url_path = root.replace("\\", "/") + "/"
                urls.append(url_path)
    
    # Генерируем XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    
    for url_path in sorted(urls):
        full_url = f"{BASE_URL}/{url_path}" if url_path else BASE_URL + "/"
        full_url = full_url.replace("//", "/").replace("https:/", "https://")
        
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{full_url}</loc>")
        xml_lines.append(f"    <lastmod>{TODAY}</lastmod>")
        xml_lines.append("  </url>")
    
    xml_lines.append("</urlset>")
    
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines))
    
    print(f"Создан sitemap.xml с {len(urls)} URL")

if __name__ == "__main__":
    main()
