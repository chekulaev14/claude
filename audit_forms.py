#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Аудит всех форм на сайте dinamika-cargo.ru (статический, без отправки заявок).
Для каждой страницы с <form> проверяет:
  - есть ли механизм отправки в наш сервис (forms-handler.js или прямой fetch на эндпоинт)
  - есть ли поле телефона
  - НЕТ ли регрессии: старый токен бота / Web3Forms в публичном коде
Группирует по типу формы (id), чтобы отчёт был компактным.
Запуск: python3 audit_forms.py
"""
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
ENDPOINT = "dinamika/api/lead"
OLD_TOKEN = "7779064115"
SKIP_DIRS = {".git", "node_modules"}
# Не боевые: бэкапы и черновики-шаблоны — учитываем отдельно, не как проблемы
NONPROD_RE = re.compile(r"(backup|templates-test/|template\.html$|index-improved|footer-final)")

def iter_html():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)

def form_ids(html):
    ids = re.findall(r'<form[^>]*\bid="([^"]+)"', html)
    # формы без id — помечаем как (no-id)
    n_forms = len(re.findall(r"<form\b", html))
    if n_forms > len(ids):
        ids += ["(no-id)"] * (n_forms - len(ids))
    return ids

stats = defaultdict(lambda: {"count": 0, "ok": 0, "no_send": [], "no_phone": [], "regress": []})
prod_total = nonprod_total = 0
problems = []

for path in iter_html():
    html = open(path, encoding="utf-8", errors="ignore").read()
    if "<form" not in html:
        continue
    rel = os.path.relpath(path, ROOT)
    is_prod = not NONPROD_RE.search(rel)

    has_handler = "forms-handler.js" in html
    has_direct = ENDPOINT in html
    can_send = has_handler or has_direct
    has_phone = bool(re.search(r'name="phone"|type="tel"|id="phone"|Phone', html))
    regress = OLD_TOKEN in html or "web3forms" in html.lower()

    if is_prod:
        prod_total += 1
    else:
        nonprod_total += 1

    for fid in form_ids(html):
        key = fid if is_prod else f"[non-prod] {fid}"
        s = stats[key]
        s["count"] += 1
        ok = can_send and has_phone and not regress
        if ok:
            s["ok"] += 1
        if is_prod:
            if not can_send:
                s["no_send"].append(rel)
            if not has_phone:
                s["no_phone"].append(rel)
            if regress:
                s["regress"].append(rel)
            if not ok:
                problems.append((rel, fid, "no_send" if not can_send else "regress" if regress else "no_phone"))

print("=" * 60)
print("АУДИТ ФОРМ САЙТА")
print("=" * 60)
print(f"Боевых страниц с формой:     {prod_total}")
print(f"Не боевых (бэкап/шаблоны):    {nonprod_total}")
print()
print(f"{'Тип формы (id)':<28}{'всего':>7}{'ОК':>6}{'проблем':>9}")
print("-" * 50)
for key in sorted(stats, key=lambda k: -stats[k]["count"]):
    s = stats[key]
    bad = s["count"] - s["ok"]
    flag = "  ⚠️" if (bad and not key.startswith("[non-prod]")) else ""
    print(f"{key:<28}{s['count']:>7}{s['ok']:>6}{bad:>9}{flag}")

print()
if problems:
    print(f"⚠️  ПРОБЛЕМНЫЕ БОЕВЫЕ СТРАНИЦЫ: {len(problems)}")
    shown = defaultdict(list)
    for rel, fid, why in problems:
        shown[why].append(rel)
    names = {"no_send": "нет отправки в сервис", "no_phone": "нет поля телефона", "regress": "РЕГРЕСС: старый токен/Web3Forms"}
    for why, lst in shown.items():
        print(f"\n  [{names[why]}] — {len(lst)} шт:")
        for r in lst[:15]:
            print(f"    - {r}")
        if len(lst) > 15:
            print(f"    ... и ещё {len(lst) - 15}")
else:
    print("✅ Проблемных боевых форм не найдено.")
    print("   Все боевые формы: шлют в сервис + есть телефон + нет старого токена/Web3Forms.")
