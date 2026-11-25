#!/usr/bin/python3
"""Сводка 30 попыток сборки и точный тест Фишера.

Попытка считается обнаружившей необъявленную зависимость, если сборка
завершилась отказом и в журнале есть диагностика, относящаяся к
исключённому пакету (шаблон DIAG). Отказ по другой причине выводится
отдельно и в число обнаружений не входит.

Результаты: results/results.tsv (30 строк) и results/summary.md.
"""
import math
import pathlib
import re

top = pathlib.Path(__file__).resolve().parent.parent
res = top / "results"

# признак в журнале, указывающий на отсутствие исключённой зависимости
DIAG = {
    "zlib-devel": r"zlib\.h: No such file",
    "scdoc": r"scdoc: command not found",
    "libreadline-devel": r"readline/readline\.h: No such file",
    "flex": r"flex: No such file",
    "libxml2-devel": r"libxml/parser\.h: No such file",
    "discount": r"markdown: No such file",
    "cmake": r"cmake: command not found|Macro %cmake not found",
    "glib2-devel": r'Dependency "glib-2\.0" not found',
    "python3-dev": r"Python\.h: No such file",
    "autoconf-archive": r"AX_CHECK_COMPILE_FLAG",
}
LEVELS = [
    ("level1", "1: хост-система"),
    ("level2", "2: hasher + все BuildRequires полного spec"),
    ("level3", "3: минимальный hasher"),
]


def tsv(path):
    lines = [l for l in path.read_text().splitlines() if l and not l.startswith("#")]
    head = lines[0].split("\t")
    return [dict(zip(head, l.split("\t"))) for l in lines[1:]]


def first_diag(log, pattern):
    for line in log.splitlines():
        if "rpmi:" not in line and re.search(pattern, line):
            return line.strip()
    return ""


def fisher(a, b, c, d):
    """Точный тест Фишера для таблицы [[a, b], [c, d]]:
    двусторонний p и односторонний p для гипотезы «в первой строке
    доля первого столбца больше, чем во второй»."""
    n1, n2, k = a + b, c + d, a + c
    total = math.comb(n1 + n2, k)
    prob = lambda x: math.comb(n1, x) * math.comb(n2, k - x) / total
    xs = range(max(0, k - n2), min(k, n1) + 1)
    p_obs = prob(a)
    two = sum(prob(x) for x in xs if prob(x) <= p_obs * (1 + 1e-9))
    one = sum(prob(x) for x in xs if x >= a)
    return min(two, 1.0), min(one, 1.0)


def name_of(nvr):
    return nvr.rsplit("-", 2)[0]


removed = {r["package"]: r["removed"] for r in tsv(top / "experiment" / "removed.tsv")}
base = set((top / "experiment" / "hasher-base.txt").read_text().split())
host_size = len((top / "experiment" / "host-before-level1.txt").read_text().split())

rows, detected, env = [], {}, {}
for level, _ in LEVELS:
    summary = {r["package"]: r for r in tsv(res / level / "summary.tsv")}
    detected[level], env[level] = 0, []
    for pkg in sorted(removed):
        rc = int(summary[pkg]["rc"])
        log = (res / level / f"{pkg}.log").read_text(errors="replace")
        diag = first_diag(log, DIAG[removed[pkg]]) if rc else ""
        if rc and diag:
            outcome = "обнаружена"
            detected[level] += 1
        elif rc:
            outcome = "отказ по другой причине"
        else:
            outcome = "случайный успех"
        if level == "level1":
            size = host_size
        else:
            added = {name_of(l) for l in (res / level / f"{pkg}.pkgs").read_text().split()}
            size = len(base | added)
        env[level].append(size)
        rows.append([pkg, level, removed[pkg], str(rc), outcome, str(size), diag])

(res / "results.tsv").write_text(
    "package\tlevel\tremoved\trc\toutcome\tenv_packages\tdiagnostic\n"
    + "".join("\t".join(r) + "\n" for r in rows)
)

n = len(removed)
d1, d2, d3 = detected["level1"], detected["level2"], detected["level3"]
p13 = fisher(d3, n - d3, d1, n - d1)
p23 = fisher(d3, n - d3, d2, n - d2)

md = ["# Сводка эксперимента", "",
      "| Уровень изоляции | Обнаружено | Случайный успех | Доля случайных успехов | Пакетов в среде |",
      "|---|---|---|---|---|"]
for level, title in LEVELS:
    d = detected[level]
    sizes = env[level]
    size = str(sizes[0]) if min(sizes) == max(sizes) else f"{min(sizes)}–{max(sizes)}"
    md.append(f"| {title} | {d}/{n} | {n - d}/{n} | {(n - d) / n:.1f} | {size} |")
md += ["",
       "Точный тест Фишера (уровень значимости 0,05):", "",
       f"* уровень 3 против уровня 1: {d3}/{n} и {d1}/{n}, "
       f"двусторонний p = {p13[0]:.4f}, односторонний p = {p13[1]:.4f}",
       f"* уровень 3 против уровня 2: {d3}/{n} и {d2}/{n}, "
       f"двусторонний p = {p23[0]:.4f}, односторонний p = {p23[1]:.4f}",
       "",
       "Гипотеза (уровень 3 строго больше уровня 1 и различие значимо): "
       + ("подтверждена" if d3 > d1 and p13[0] < 0.05 else "не подтверждена"),
       ""]
(res / "summary.md").write_text("\n".join(md))
print("\n".join(md))
