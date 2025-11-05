# SEO-структура сайта

## 1. Структура /regions/ (48 городов)

### Областные центры и крупные города РФ (17):
- moscow (Москва)
- kazan (Казань)
- samara (Самара)
- kaluga (Калуга)
- obninsk (Обнинск)
- tula (Тула)
- tver (Тверь)
- yaroslavl (Ярославль)
- saint-petersburg (Санкт-Петербург)
- nizhny-novgorod (Нижний Новгород)
- nizhnekamsk (Нижнекамск)
- naberezhnye-chelny (Набережные Челны)
- izhevsk (Ижевск)
- ufa (Уфа)
- chelyabinsk (Челябинск)
- ekaterinburg (Екатеринбург)
- perm (Пермь)

### Города Московской области (31):
- balashikha (Балашиха)
- podolsk (Подольск)
- khimki (Химки)
- korolev (Королёв)
- mytishchi (Мытищи)
- lyubertsy (Люберцы)
- krasnogorsk (Красногорск)
- elektrostal (Электросталь)
- kolomna (Коломна)
- odintsovo (Одинцово)
- domodedovo (Домодедово)
- serpukhov (Серпухов)
- shchelkovo (Щёлково)
- orekhovo-zuevo (Орехово-Зуево)
- ramenskoe (Раменское)
- dolgoprudny (Долгопрудный)
- zhukovsky (Жуковский)
- pushkino (Пушкино)
- reutov (Реутов)
- sergiev-posad (Сергиев Посад)
- voskresensk (Воскресенск)
- lobnya (Лобня)
- klin (Клин)
- ivanteyevka (Ивантеевка)
- dubna (Дубна)
- egoryevsk (Егорьевск)
- chekhov (Чехов)
- dmitrov (Дмитров)
- noginsk (Ногинск)
- fryazino (Фрязино)
- dzerzhinsky (Дзержинский)

### Структура каждого города:
```
/regions/
├── {город}/
│   ├── index.html              # Главная страница города
│   ├── klaster1/index.html     # Кластер 1
│   ├── klaster2/index.html     # Кластер 2
│   ├── klaster3/index.html     # Кластер 3
│   └── klasterN/index.html     # ...и так далее по количеству кластеров
```

---

## 2. Структура /routes/ (272 страницы)

### 2.1. Москва ↔ 16 областных центров (32 страницы)

**Из Москвы (16 страниц):**
1. /routes/moskva-kazan/
2. /routes/moskva-samara/
3. /routes/moskva-kaluga/
4. /routes/moskva-obninsk/
5. /routes/moskva-tula/
6. /routes/moskva-tver/
7. /routes/moskva-yaroslavl/
8. /routes/moskva-spb/
9. /routes/moskva-nizhny-novgorod/
10. /routes/moskva-nizhnekamsk/
11. /routes/moskva-naberezhnye-chelny/
12. /routes/moskva-izhevsk/
13. /routes/moskva-ufa/
14. /routes/moskva-chelyabinsk/
15. /routes/moskva-ekaterinburg/
16. /routes/moskva-perm/

**В Москву (16 страниц):**
1. /routes/kazan-moskva/
2. /routes/samara-moskva/
3. /routes/kaluga-moskva/
4. /routes/obninsk-moskva/
5. /routes/tula-moskva/
6. /routes/tver-moskva/
7. /routes/yaroslavl-moskva/
8. /routes/spb-moskva/
9. /routes/nizhny-novgorod-moskva/
10. /routes/nizhnekamsk-moskva/
11. /routes/naberezhnye-chelny-moskva/
12. /routes/izhevsk-moskva/
13. /routes/ufa-moskva/
14. /routes/chelyabinsk-moskva/
15. /routes/ekaterinburg-moskva/
16. /routes/perm-moskva/

### 2.2. СПб ↔ 15 областных центров без Москвы (30 страниц)

**Из СПб (15 страниц):**
1. /routes/spb-kazan/
2. /routes/spb-samara/
3. /routes/spb-kaluga/
4. /routes/spb-obninsk/
5. /routes/spb-tula/
6. /routes/spb-tver/
7. /routes/spb-yaroslavl/
8. /routes/spb-nizhny-novgorod/
9. /routes/spb-nizhnekamsk/
10. /routes/spb-naberezhnye-chelny/
11. /routes/spb-izhevsk/
12. /routes/spb-ufa/
13. /routes/spb-chelyabinsk/
14. /routes/spb-ekaterinburg/
15. /routes/spb-perm/

**В СПб (15 страниц):**
1. /routes/kazan-spb/
2. /routes/samara-spb/
3. /routes/kaluga-spb/
4. /routes/obninsk-spb/
5. /routes/tula-spb/
6. /routes/tver-spb/
7. /routes/yaroslavl-spb/
8. /routes/nizhny-novgorod-spb/
9. /routes/nizhnekamsk-spb/
10. /routes/naberezhnye-chelny-spb/
11. /routes/izhevsk-spb/
12. /routes/ufa-spb/
13. /routes/chelyabinsk-spb/
14. /routes/ekaterinburg-spb/
15. /routes/perm-spb/

### 2.3. Межрегиональные маршруты - 15 областных центров между собой (210 страниц)

**Казань (28 страниц):**
*Из Казани:*
1. /routes/kazan-samara/
2. /routes/kazan-kaluga/
3. /routes/kazan-obninsk/
4. /routes/kazan-tula/
5. /routes/kazan-tver/
6. /routes/kazan-yaroslavl/
7. /routes/kazan-nizhny-novgorod/
8. /routes/kazan-nizhnekamsk/
9. /routes/kazan-naberezhnye-chelny/
10. /routes/kazan-izhevsk/
11. /routes/kazan-ufa/
12. /routes/kazan-chelyabinsk/
13. /routes/kazan-ekaterinburg/
14. /routes/kazan-perm/
*В Казань:*
15. /routes/samara-kazan/
16. /routes/kaluga-kazan/
17. /routes/obninsk-kazan/
18. /routes/tula-kazan/
19. /routes/tver-kazan/
20. /routes/yaroslavl-kazan/
21. /routes/nizhny-novgorod-kazan/
22. /routes/nizhnekamsk-kazan/
23. /routes/naberezhnye-chelny-kazan/
24. /routes/izhevsk-kazan/
25. /routes/ufa-kazan/
26. /routes/chelyabinsk-kazan/
27. /routes/ekaterinburg-kazan/
28. /routes/perm-kazan/

**Самара (28 страниц):**
*Из Самары:*
1. /routes/samara-kazan/
2. /routes/samara-kaluga/
3. /routes/samara-obninsk/
4. /routes/samara-tula/
5. /routes/samara-tver/
6. /routes/samara-yaroslavl/
7. /routes/samara-nizhny-novgorod/
8. /routes/samara-nizhnekamsk/
9. /routes/samara-naberezhnye-chelny/
10. /routes/samara-izhevsk/
11. /routes/samara-ufa/
12. /routes/samara-chelyabinsk/
13. /routes/samara-ekaterinburg/
14. /routes/samara-perm/
*В Самару:*
15. /routes/kazan-samara/
16. /routes/kaluga-samara/
17. /routes/obninsk-samara/
18. /routes/tula-samara/
19. /routes/tver-samara/
20. /routes/yaroslavl-samara/
21. /routes/nizhny-novgorod-samara/
22. /routes/nizhnekamsk-samara/
23. /routes/naberezhnye-chelny-samara/
24. /routes/izhevsk-samara/
25. /routes/ufa-samara/
26. /routes/chelyabinsk-samara/
27. /routes/ekaterinburg-samara/
28. /routes/perm-samara/

**Калуга (28 страниц):**
*Из Калуги:*
1. /routes/kaluga-kazan/
2. /routes/kaluga-samara/
3. /routes/kaluga-obninsk/
4. /routes/kaluga-tula/
5. /routes/kaluga-tver/
6. /routes/kaluga-yaroslavl/
7. /routes/kaluga-nizhny-novgorod/
8. /routes/kaluga-nizhnekamsk/
9. /routes/kaluga-naberezhnye-chelny/
10. /routes/kaluga-izhevsk/
11. /routes/kaluga-ufa/
12. /routes/kaluga-chelyabinsk/
13. /routes/kaluga-ekaterinburg/
14. /routes/kaluga-perm/
*В Калугу:*
15. /routes/kazan-kaluga/
16. /routes/samara-kaluga/
17. /routes/obninsk-kaluga/
18. /routes/tula-kaluga/
19. /routes/tver-kaluga/
20. /routes/yaroslavl-kaluga/
21. /routes/nizhny-novgorod-kaluga/
22. /routes/nizhnekamsk-kaluga/
23. /routes/naberezhnye-chelny-kaluga/
24. /routes/izhevsk-kaluga/
25. /routes/ufa-kaluga/
26. /routes/chelyabinsk-kaluga/
27. /routes/ekaterinburg-kaluga/
28. /routes/perm-kaluga/

**Обнинск (28 страниц):**
*Из Обнинска:*
1. /routes/obninsk-kazan/
2. /routes/obninsk-samara/
3. /routes/obninsk-kaluga/
4. /routes/obninsk-tula/
5. /routes/obninsk-tver/
6. /routes/obninsk-yaroslavl/
7. /routes/obninsk-nizhny-novgorod/
8. /routes/obninsk-nizhnekamsk/
9. /routes/obninsk-naberezhnye-chelny/
10. /routes/obninsk-izhevsk/
11. /routes/obninsk-ufa/
12. /routes/obninsk-chelyabinsk/
13. /routes/obninsk-ekaterinburg/
14. /routes/obninsk-perm/
*В Обнинск:*
15. /routes/kazan-obninsk/
16. /routes/samara-obninsk/
17. /routes/kaluga-obninsk/
18. /routes/tula-obninsk/
19. /routes/tver-obninsk/
20. /routes/yaroslavl-obninsk/
21. /routes/nizhny-novgorod-obninsk/
22. /routes/nizhnekamsk-obninsk/
23. /routes/naberezhnye-chelny-obninsk/
24. /routes/izhevsk-obninsk/
25. /routes/ufa-obninsk/
26. /routes/chelyabinsk-obninsk/
27. /routes/ekaterinburg-obninsk/
28. /routes/perm-obninsk/

**Тула (28 страниц):**
*Из Тулы:*
1. /routes/tula-kazan/
2. /routes/tula-samara/
3. /routes/tula-kaluga/
4. /routes/tula-obninsk/
5. /routes/tula-tver/
6. /routes/tula-yaroslavl/
7. /routes/tula-nizhny-novgorod/
8. /routes/tula-nizhnekamsk/
9. /routes/tula-naberezhnye-chelny/
10. /routes/tula-izhevsk/
11. /routes/tula-ufa/
12. /routes/tula-chelyabinsk/
13. /routes/tula-ekaterinburg/
14. /routes/tula-perm/
*В Тулу:*
15. /routes/kazan-tula/
16. /routes/samara-tula/
17. /routes/kaluga-tula/
18. /routes/obninsk-tula/
19. /routes/tver-tula/
20. /routes/yaroslavl-tula/
21. /routes/nizhny-novgorod-tula/
22. /routes/nizhnekamsk-tula/
23. /routes/naberezhnye-chelny-tula/
24. /routes/izhevsk-tula/
25. /routes/ufa-tula/
26. /routes/chelyabinsk-tula/
27. /routes/ekaterinburg-tula/
28. /routes/perm-tula/

**Тверь (28 страниц):**
*Из Твери:*
1. /routes/tver-kazan/
2. /routes/tver-samara/
3. /routes/tver-kaluga/
4. /routes/tver-obninsk/
5. /routes/tver-tula/
6. /routes/tver-yaroslavl/
7. /routes/tver-nizhny-novgorod/
8. /routes/tver-nizhnekamsk/
9. /routes/tver-naberezhnye-chelny/
10. /routes/tver-izhevsk/
11. /routes/tver-ufa/
12. /routes/tver-chelyabinsk/
13. /routes/tver-ekaterinburg/
14. /routes/tver-perm/
*В Тверь:*
15. /routes/kazan-tver/
16. /routes/samara-tver/
17. /routes/kaluga-tver/
18. /routes/obninsk-tver/
19. /routes/tula-tver/
20. /routes/yaroslavl-tver/
21. /routes/nizhny-novgorod-tver/
22. /routes/nizhnekamsk-tver/
23. /routes/naberezhnye-chelny-tver/
24. /routes/izhevsk-tver/
25. /routes/ufa-tver/
26. /routes/chelyabinsk-tver/
27. /routes/ekaterinburg-tver/
28. /routes/perm-tver/

**Ярославль (28 страниц):**
*Из Ярославля:*
1. /routes/yaroslavl-kazan/
2. /routes/yaroslavl-samara/
3. /routes/yaroslavl-kaluga/
4. /routes/yaroslavl-obninsk/
5. /routes/yaroslavl-tula/
6. /routes/yaroslavl-tver/
7. /routes/yaroslavl-nizhny-novgorod/
8. /routes/yaroslavl-nizhnekamsk/
9. /routes/yaroslavl-naberezhnye-chelny/
10. /routes/yaroslavl-izhevsk/
11. /routes/yaroslavl-ufa/
12. /routes/yaroslavl-chelyabinsk/
13. /routes/yaroslavl-ekaterinburg/
14. /routes/yaroslavl-perm/
*В Ярославль:*
15. /routes/kazan-yaroslavl/
16. /routes/samara-yaroslavl/
17. /routes/kaluga-yaroslavl/
18. /routes/obninsk-yaroslavl/
19. /routes/tula-yaroslavl/
20. /routes/tver-yaroslavl/
21. /routes/nizhny-novgorod-yaroslavl/
22. /routes/nizhnekamsk-yaroslavl/
23. /routes/naberezhnye-chelny-yaroslavl/
24. /routes/izhevsk-yaroslavl/
25. /routes/ufa-yaroslavl/
26. /routes/chelyabinsk-yaroslavl/
27. /routes/ekaterinburg-yaroslavl/
28. /routes/perm-yaroslavl/

**Нижний Новгород (28 страниц):**
*Из Нижнего Новгорода:*
1. /routes/nizhny-novgorod-kazan/
2. /routes/nizhny-novgorod-samara/
3. /routes/nizhny-novgorod-kaluga/
4. /routes/nizhny-novgorod-obninsk/
5. /routes/nizhny-novgorod-tula/
6. /routes/nizhny-novgorod-tver/
7. /routes/nizhny-novgorod-yaroslavl/
8. /routes/nizhny-novgorod-nizhnekamsk/
9. /routes/nizhny-novgorod-naberezhnye-chelny/
10. /routes/nizhny-novgorod-izhevsk/
11. /routes/nizhny-novgorod-ufa/
12. /routes/nizhny-novgorod-chelyabinsk/
13. /routes/nizhny-novgorod-ekaterinburg/
14. /routes/nizhny-novgorod-perm/
*В Нижний Новгород:*
15. /routes/kazan-nizhny-novgorod/
16. /routes/samara-nizhny-novgorod/
17. /routes/kaluga-nizhny-novgorod/
18. /routes/obninsk-nizhny-novgorod/
19. /routes/tula-nizhny-novgorod/
20. /routes/tver-nizhny-novgorod/
21. /routes/yaroslavl-nizhny-novgorod/
22. /routes/nizhnekamsk-nizhny-novgorod/
23. /routes/naberezhnye-chelny-nizhny-novgorod/
24. /routes/izhevsk-nizhny-novgorod/
25. /routes/ufa-nizhny-novgorod/
26. /routes/chelyabinsk-nizhny-novgorod/
27. /routes/ekaterinburg-nizhny-novgorod/
28. /routes/perm-nizhny-novgorod/

**Нижнекамск (28 страниц):**
*Из Нижнекамска:*
1. /routes/nizhnekamsk-kazan/
2. /routes/nizhnekamsk-samara/
3. /routes/nizhnekamsk-kaluga/
4. /routes/nizhnekamsk-obninsk/
5. /routes/nizhnekamsk-tula/
6. /routes/nizhnekamsk-tver/
7. /routes/nizhnekamsk-yaroslavl/
8. /routes/nizhnekamsk-nizhny-novgorod/
9. /routes/nizhnekamsk-naberezhnye-chelny/
10. /routes/nizhnekamsk-izhevsk/
11. /routes/nizhnekamsk-ufa/
12. /routes/nizhnekamsk-chelyabinsk/
13. /routes/nizhnekamsk-ekaterinburg/
14. /routes/nizhnekamsk-perm/
*В Нижнекамск:*
15. /routes/kazan-nizhnekamsk/
16. /routes/samara-nizhnekamsk/
17. /routes/kaluga-nizhnekamsk/
18. /routes/obninsk-nizhnekamsk/
19. /routes/tula-nizhnekamsk/
20. /routes/tver-nizhnekamsk/
21. /routes/yaroslavl-nizhnekamsk/
22. /routes/nizhny-novgorod-nizhnekamsk/
23. /routes/naberezhnye-chelny-nizhnekamsk/
24. /routes/izhevsk-nizhnekamsk/
25. /routes/ufa-nizhnekamsk/
26. /routes/chelyabinsk-nizhnekamsk/
27. /routes/ekaterinburg-nizhnekamsk/
28. /routes/perm-nizhnekamsk/

**Набережные Челны (28 страниц):**
*Из Набережных Челнов:*
1. /routes/naberezhnye-chelny-kazan/
2. /routes/naberezhnye-chelny-samara/
3. /routes/naberezhnye-chelny-kaluga/
4. /routes/naberezhnye-chelny-obninsk/
5. /routes/naberezhnye-chelny-tula/
6. /routes/naberezhnye-chelny-tver/
7. /routes/naberezhnye-chelny-yaroslavl/
8. /routes/naberezhnye-chelny-nizhny-novgorod/
9. /routes/naberezhnye-chelny-nizhnekamsk/
10. /routes/naberezhnye-chelny-izhevsk/
11. /routes/naberezhnye-chelny-ufa/
12. /routes/naberezhnye-chelny-chelyabinsk/
13. /routes/naberezhnye-chelny-ekaterinburg/
14. /routes/naberezhnye-chelny-perm/
*В Набережные Челны:*
15. /routes/kazan-naberezhnye-chelny/
16. /routes/samara-naberezhnye-chelny/
17. /routes/kaluga-naberezhnye-chelny/
18. /routes/obninsk-naberezhnye-chelny/
19. /routes/tula-naberezhnye-chelny/
20. /routes/tver-naberezhnye-chelny/
21. /routes/yaroslavl-naberezhnye-chelny/
22. /routes/nizhny-novgorod-naberezhnye-chelny/
23. /routes/nizhnekamsk-naberezhnye-chelny/
24. /routes/izhevsk-naberezhnye-chelny/
25. /routes/ufa-naberezhnye-chelny/
26. /routes/chelyabinsk-naberezhnye-chelny/
27. /routes/ekaterinburg-naberezhnye-chelny/
28. /routes/perm-naberezhnye-chelny/

**Ижевск (28 страниц):**
*Из Ижевска:*
1. /routes/izhevsk-kazan/
2. /routes/izhevsk-samara/
3. /routes/izhevsk-kaluga/
4. /routes/izhevsk-obninsk/
5. /routes/izhevsk-tula/
6. /routes/izhevsk-tver/
7. /routes/izhevsk-yaroslavl/
8. /routes/izhevsk-nizhny-novgorod/
9. /routes/izhevsk-nizhnekamsk/
10. /routes/izhevsk-naberezhnye-chelny/
11. /routes/izhevsk-ufa/
12. /routes/izhevsk-chelyabinsk/
13. /routes/izhevsk-ekaterinburg/
14. /routes/izhevsk-perm/
*В Ижевск:*
15. /routes/kazan-izhevsk/
16. /routes/samara-izhevsk/
17. /routes/kaluga-izhevsk/
18. /routes/obninsk-izhevsk/
19. /routes/tula-izhevsk/
20. /routes/tver-izhevsk/
21. /routes/yaroslavl-izhevsk/
22. /routes/nizhny-novgorod-izhevsk/
23. /routes/nizhnekamsk-izhevsk/
24. /routes/naberezhnye-chelny-izhevsk/
25. /routes/ufa-izhevsk/
26. /routes/chelyabinsk-izhevsk/
27. /routes/ekaterinburg-izhevsk/
28. /routes/perm-izhevsk/

**Уфа (28 страниц):**
*Из Уфы:*
1. /routes/ufa-kazan/
2. /routes/ufa-samara/
3. /routes/ufa-kaluga/
4. /routes/ufa-obninsk/
5. /routes/ufa-tula/
6. /routes/ufa-tver/
7. /routes/ufa-yaroslavl/
8. /routes/ufa-nizhny-novgorod/
9. /routes/ufa-nizhnekamsk/
10. /routes/ufa-naberezhnye-chelny/
11. /routes/ufa-izhevsk/
12. /routes/ufa-chelyabinsk/
13. /routes/ufa-ekaterinburg/
14. /routes/ufa-perm/
*В Уфу:*
15. /routes/kazan-ufa/
16. /routes/samara-ufa/
17. /routes/kaluga-ufa/
18. /routes/obninsk-ufa/
19. /routes/tula-ufa/
20. /routes/tver-ufa/
21. /routes/yaroslavl-ufa/
22. /routes/nizhny-novgorod-ufa/
23. /routes/nizhnekamsk-ufa/
24. /routes/naberezhnye-chelny-ufa/
25. /routes/izhevsk-ufa/
26. /routes/chelyabinsk-ufa/
27. /routes/ekaterinburg-ufa/
28. /routes/perm-ufa/

**Челябинск (28 страниц):**
*Из Челябинска:*
1. /routes/chelyabinsk-kazan/
2. /routes/chelyabinsk-samara/
3. /routes/chelyabinsk-kaluga/
4. /routes/chelyabinsk-obninsk/
5. /routes/chelyabinsk-tula/
6. /routes/chelyabinsk-tver/
7. /routes/chelyabinsk-yaroslavl/
8. /routes/chelyabinsk-nizhny-novgorod/
9. /routes/chelyabinsk-nizhnekamsk/
10. /routes/chelyabinsk-naberezhnye-chelny/
11. /routes/chelyabinsk-izhevsk/
12. /routes/chelyabinsk-ufa/
13. /routes/chelyabinsk-ekaterinburg/
14. /routes/chelyabinsk-perm/
*В Челябинск:*
15. /routes/kazan-chelyabinsk/
16. /routes/samara-chelyabinsk/
17. /routes/kaluga-chelyabinsk/
18. /routes/obninsk-chelyabinsk/
19. /routes/tula-chelyabinsk/
20. /routes/tver-chelyabinsk/
21. /routes/yaroslavl-chelyabinsk/
22. /routes/nizhny-novgorod-chelyabinsk/
23. /routes/nizhnekamsk-chelyabinsk/
24. /routes/naberezhnye-chelny-chelyabinsk/
25. /routes/izhevsk-chelyabinsk/
26. /routes/ufa-chelyabinsk/
27. /routes/ekaterinburg-chelyabinsk/
28. /routes/perm-chelyabinsk/

**Екатеринбург (28 страниц):**
*Из Екатеринбурга:*
1. /routes/ekaterinburg-kazan/
2. /routes/ekaterinburg-samara/
3. /routes/ekaterinburg-kaluga/
4. /routes/ekaterinburg-obninsk/
5. /routes/ekaterinburg-tula/
6. /routes/ekaterinburg-tver/
7. /routes/ekaterinburg-yaroslavl/
8. /routes/ekaterinburg-nizhny-novgorod/
9. /routes/ekaterinburg-nizhnekamsk/
10. /routes/ekaterinburg-naberezhnye-chelny/
11. /routes/ekaterinburg-izhevsk/
12. /routes/ekaterinburg-ufa/
13. /routes/ekaterinburg-chelyabinsk/
14. /routes/ekaterinburg-perm/
*В Екатеринбург:*
15. /routes/kazan-ekaterinburg/
16. /routes/samara-ekaterinburg/
17. /routes/kaluga-ekaterinburg/
18. /routes/obninsk-ekaterinburg/
19. /routes/tula-ekaterinburg/
20. /routes/tver-ekaterinburg/
21. /routes/yaroslavl-ekaterinburg/
22. /routes/nizhny-novgorod-ekaterinburg/
23. /routes/nizhnekamsk-ekaterinburg/
24. /routes/naberezhnye-chelny-ekaterinburg/
25. /routes/izhevsk-ekaterinburg/
26. /routes/ufa-ekaterinburg/
27. /routes/chelyabinsk-ekaterinburg/
28. /routes/perm-ekaterinburg/

**Пермь (28 страниц):**
*Из Перми:*
1. /routes/perm-kazan/
2. /routes/perm-samara/
3. /routes/perm-kaluga/
4. /routes/perm-obninsk/
5. /routes/perm-tula/
6. /routes/perm-tver/
7. /routes/perm-yaroslavl/
8. /routes/perm-nizhny-novgorod/
9. /routes/perm-nizhnekamsk/
10. /routes/perm-naberezhnye-chelny/
11. /routes/perm-izhevsk/
12. /routes/perm-ufa/
13. /routes/perm-chelyabinsk/
14. /routes/perm-ekaterinburg/
*В Пермь:*
15. /routes/kazan-perm/
16. /routes/samara-perm/
17. /routes/kaluga-perm/
18. /routes/obninsk-perm/
19. /routes/tula-perm/
20. /routes/tver-perm/
21. /routes/yaroslavl-perm/
22. /routes/nizhny-novgorod-perm/
23. /routes/nizhnekamsk-perm/
24. /routes/naberezhnye-chelny-perm/
25. /routes/izhevsk-perm/
26. /routes/ufa-perm/
27. /routes/chelyabinsk-perm/
28. /routes/ekaterinburg-perm/

### Структура маршрута:
```
/routes/
├── {город1-город2}/
│   └── index.html          # Страница маршрута из города1 в город2
```
