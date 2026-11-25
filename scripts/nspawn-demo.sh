#!/bin/sh
# nspawn-demo.sh [ДЕРЕВО] - обзорное сопоставление с systemd-nspawn (от root)
#
# Запускает в контейнере systemd-nspawn то же дерево, которое hasher
# построил для сборки (по умолчанию ~user/hasher-art/chroot), только для
# чтения и без сети, и показывает, что изолировано (имя узла, процессы,
# сетевые интерфейсы), а что определяется деревом (состав пакетов).
set -eu

tree=${1:-/home/user/hasher-art/chroot}

echo "== состав дерева на хосте: $(rpm --root "$tree" -qa | wc -l) пакетов"
echo "== systemd-nspawn -D $tree --read-only --private-network --timezone=off"
# shellcheck disable=SC2016  # код выполняется внутри контейнера
systemd-nspawn -q -D "$tree" --read-only --private-network --timezone=off -M art10-nspawn -- /bin/sh -c '
echo "hostname:   $(hostname)"
echo "processes:"; ps -e -o pid,comm
echo "interfaces: $(tail -n +3 /proc/net/dev | cut -d: -f1 | tr -d " " | tr "\n" " ")"
echo "packages:   $(rpm -qa | wc -l)"
echo "rpm -q zlib-devel cmake:"; rpm -q zlib-devel cmake || true'
