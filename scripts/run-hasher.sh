#!/bin/sh
# run-hasher.sh MODE [NN...] - сборка учебных пакетов в hasher
#
#   control  полные spec-файлы, чистое окружение (проверка корректности)
#   level2   урезанные spec-файлы; перед сборкой в окружение ставятся все
#            BuildRequires полной версии spec-файла (hsh-install), затем
#            hsh-rebuild в том же окружении
#   level3   урезанные spec-файлы, чистое окружение: hsh ставит только
#            объявленные в урезанном spec-файле зависимости
#
# Необязательные аргументы NN ограничивают набор пакетов (по номеру).
# Для каждого пакета окружение создаётся заново. Результаты:
#   results/MODE/NN-NAME.log    журнал сборки
#   results/MODE/NN-NAME.pkgs   пакеты, установленные в окружение (по журналу)
#   results/MODE/summary.tsv    пакет, код возврата, число пакетов окружения
# shellcheck disable=SC2086
set -u

mode=$1
shift
top=$(cd "$(dirname "$0")/.." && pwd)
work=${HASHER_DIR:-$HOME/hasher-art}
srpms=${SRPM_DIR:-$HOME/art10/srpm}
out=$top/results/$mode
mkdir -p "$work" "$out"

case $mode in
    control) kind=full ;;
    level2|level3) kind=trimmed ;;
    *) echo "usage: $0 control|level2|level3 [NN...]" >&2; exit 2 ;;
esac

[ -f "$out/summary.tsv" ] || printf 'package\trc\tenv_packages\n' > "$out/summary.tsv"
for dir in "$top"/packages/[0-9][0-9]-*; do
    id=$(basename "$dir")
    name=${id#[0-9][0-9]-}
    if [ $# -gt 0 ] && ! echo " $* " | grep -q " ${id%%-*} "; then
        continue
    fi
    srpm=$(ls "$srpms/$kind/$name"-*.src.rpm)
    log=$out/$id.log
    echo "== $mode $id"
    case $mode in
        control|level3)
            hsh "$work" "$srpm" > "$log" 2>&1 < /dev/null
            rc=$?
            ;;
        level2)
            brs=$(sed -n 's/^BuildRequires:[[:space:]]*//p' "$dir/$name.spec")
            {
                hsh --initroot-only "$work" &&
                echo "+ hsh-install $brs" &&
                hsh-install "$work" $brs &&
                hsh-rebuild "$work" "$srpm"
            } > "$log" 2>&1 < /dev/null
            rc=$?
            ;;
    esac
    # состав окружения: все пакеты, установленные rpmi за время сборки
    sed -n 's/.*rpmi: \(.*\) [^ ]* [0-9]* installed$/\1/p' "$log" | LC_ALL=C sort -u > "$out/$id.pkgs"
    # повторный прогон пакета заменяет его строку в сводке
    grep -v "^$id	" "$out/summary.tsv" > "$out/summary.tmp"
    printf '%s\t%s\t%s\n' "$id" "$rc" "$(wc -l < "$out/$id.pkgs")" >> "$out/summary.tmp"
    { head -1 "$out/summary.tmp"; tail -n +2 "$out/summary.tmp" | LC_ALL=C sort; } > "$out/summary.tsv"
    rm -f "$out/summary.tmp"
    echo "   rc=$rc"
done
cat "$out/summary.tsv"
