#!/usr/bin/python3
"""Случайный выбор исключаемой директивы BuildRequires и создание
урезанных spec-файлов.

Для каждого пакета packages/NN-NAME/NAME.spec из его директив
BuildRequires равновероятно выбирается одна; файл NAME-trimmed.spec —
копия полного spec-файла без этой строки. Генератор инициализируется
фиксированным зерном, поэтому выбор воспроизводим; зерно и выбор
фиксируются в experiment/removed.tsv до снятия состава хост-системы.
"""
import pathlib
import random

SEED = 20261125  # дата постановки эксперимента

top = pathlib.Path(__file__).resolve().parent.parent
rng = random.Random(SEED)
rows = ["package\tdeclared\tremoved\tindex"]

for pkgdir in sorted(top.glob("packages/[0-9][0-9]-*")):
    name = pkgdir.name[3:]
    spec = pkgdir / f"{name}.spec"
    lines = spec.read_text().splitlines(keepends=True)
    brs = [i for i, line in enumerate(lines) if line.startswith("BuildRequires:")]
    k = rng.randrange(len(brs))
    removed = lines[brs[k]].split(":", 1)[1].strip()
    trimmed = lines[: brs[k]] + lines[brs[k] + 1 :]
    (pkgdir / f"{name}-trimmed.spec").write_text("".join(trimmed))
    declared = ",".join(lines[i].split(":", 1)[1].strip() for i in brs)
    rows.append(f"{pkgdir.name}\t{declared}\t{removed}\t{k + 1}/{len(brs)}")

out = top / "experiment" / "removed.tsv"
out.parent.mkdir(exist_ok=True)
out.write_text(f"# seed={SEED}\n" + "\n".join(rows) + "\n")
print(out.read_text(), end="")
