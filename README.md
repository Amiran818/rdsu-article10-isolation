# Влияние степени изоляции сборочной среды на выявление зависимостей

Статья №10 по дисциплине «Разработка драйверов системных устройств».
Команда RDSU22-002: Ащеулов А. А., Джакишев А. М.

**Вопрос.** Как степень изоляции сборочной среды влияет на число необъявленных
сборочных зависимостей (BuildRequires), обнаруживаемых при сборке пакетов с
намеренно неполным перечнем зависимостей?

**Результат (30 попыток: 10 пакетов × 3 уровня).**

| Уровень изоляции | Обнаружено | Случайный успех |
|---|---|---|
| 1: хост-система (2316 пакетов) | 8/10 | 2/10 |
| 2: hasher + все BuildRequires полного spec-файла | 0/10 | 10/10 |
| 3: минимальный hasher (базовый набор 180 пакетов + объявленные) | 8/10 | 2/10 |

Точный тест Фишера: уровень 3 против 1 — p = 1,0 (гипотеза не подтверждена);
уровень 3 против 2 — p = 0,0007. Оба случайных успеха уровней 1 и 3 вызваны
транзитивными зависимостями объявленных пакетов (`ctest` → `cmake`,
`python3-module-setuptools` → `python3-dev`). Текст статьи — `article/article.md`
(`article.docx`, `article.pdf`).

## Стенд

ALT Workstation 11.1 (p11), ядро 6.12.41, hasher 1.7.7, hasher-priv 2.0.14,
rpm-build 4.0.4.212, systemd 258; репозиторий окружений — зеркало p11.

## Структура

```
packages/NN-NAME/     исходники (src/), полный NAME.spec и урезанный NAME-trimmed.spec
experiment/
  removed.tsv         случайный выбор исключаемой BuildRequires (seed 20261125)
  hasher-base.txt     базовый набор окружения hasher (180 пакетов)
  host-initial.txt    состав хост-системы до эксперимента (2281 пакет)
  host-before-level1.txt  состав хоста непосредственно перед уровнем 1 (2316)
results/
  control/            контрольная сборка полных spec-файлов в чистом hasher (10/10)
  level1/ level2/ level3/   журналы 30 попыток, составы окружений, summary.tsv
  results.tsv         исход и диагностика каждой попытки
  summary.md          сводка и тест Фишера
scripts/
  make-srpm.sh        src.rpm из packages/NN-NAME (rpmbuild -bs --nodeps)
  pick-removed.py     случайный выбор и урезанные spec-файлы
  run-hasher.sh       control | level2 | level3 в hasher
  run-host.sh         уровень 1 на хост-системе
  analyze.py          сводка, точный тест Фишера
  plot.py             диаграмма article/fig/levels.png
  nspawn-demo.sh      обзорное сопоставление с systemd-nspawn (от root)
article/              текст статьи, рисунки, сборка docx/pdf (build.sh)
```

## Воспроизведение

```sh
# src.rpm полных и урезанных spec-файлов
for s in packages/*/*[!d].spec; do scripts/make-srpm.sh "$s" ~/art10/srpm/full; done
python3 scripts/pick-removed.py            # тот же выбор при том же зерне
for s in packages/*/*-trimmed.spec; do scripts/make-srpm.sh "$s" ~/art10/srpm/trimmed; done

scripts/run-hasher.sh control              # полные spec-файлы: 10/10
scripts/run-hasher.sh level3
scripts/run-hasher.sh level2
# уровень 1: на хост ставятся BuildRequires урезанных spec-файлов (от root),
# состав фиксируется rpm -qa перед запуском
scripts/run-host.sh
python3 scripts/analyze.py
```

Окружение hasher — `~/hasher-art` (переменная `HASHER_DIR`); у пользователя
должны быть настроены служебные пользователи hasher (`hasher-useradd`).
