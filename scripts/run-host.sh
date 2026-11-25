#!/bin/sh
# run-host.sh - уровень 1: сборка урезанных вариантов на хост-системе
#
# rpmbuild --rebuild без изоляции, во временном _topdir. Перед сборкой
# фиксируется, установлен ли на хосте пакет исключённой зависимости.
# Результаты:
#   results/level1/NN-NAME.log  журнал сборки
#   results/level1/summary.tsv  пакет, код возврата, установлена ли
#                               исключённая зависимость
set -u

top=$(cd "$(dirname "$0")/.." && pwd)
srpms=${SRPM_DIR:-$HOME/art10/srpm}
out=$top/results/level1
mkdir -p "$out"

printf 'package\trc\tremoved\tremoved_on_host\n' > "$out/summary.tsv"
for dir in "$top"/packages/[0-9][0-9]-*; do
    id=$(basename "$dir")
    name=${id#[0-9][0-9]-}
    srpm=$(ls "$srpms/trimmed/$name"-*.src.rpm)
    removed=$(awk -F'\t' -v id="$id" '$1 == id { print $3 }' "$top/experiment/removed.tsv")
    # пакет или виртуальная зависимость
    if rpm -q --whatprovides "$removed" > /dev/null 2>&1; then present=yes; else present=no; fi
    tmp=$(mktemp -d)
    echo "== level1 $id (removed: $removed, on host: $present)"
    LC_ALL=C rpmbuild --rebuild --define "_topdir $tmp" "$srpm" > "$out/$id.log" 2>&1 < /dev/null
    rc=$?
    rm -rf -- "$tmp"
    printf '%s\t%s\t%s\t%s\n' "$id" "$rc" "$removed" "$present" >> "$out/summary.tsv"
    echo "   rc=$rc"
done
cat "$out/summary.tsv"
