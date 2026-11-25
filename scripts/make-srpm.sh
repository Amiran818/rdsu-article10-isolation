#!/bin/sh
# make-srpm.sh SPEC OUTDIR - собрать src.rpm учебного пакета
#
# Исходники берутся из каталога src/ рядом со spec-файлом и упаковываются
# в архив NAME-VERSION.tar; сборочные зависимости при создании src.rpm
# не проверяются (--nodeps), поэтому результат не зависит от хост-системы.
set -eu

spec=$(readlink -f "$1")
out=$(mkdir -p "$2" && readlink -f "$2")
pkgdir=$(dirname "$spec")
name=$(sed -n 's/^Name:[[:space:]]*//p' "$spec")
version=$(sed -n 's/^Version:[[:space:]]*//p' "$spec")

tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT
mkdir -p "$tmp/SOURCES" "$tmp/$name-$version"
cp -a "$pkgdir/src/." "$tmp/$name-$version/"
tar -C "$tmp" --owner=0 --group=0 --sort=name -cf "$tmp/SOURCES/$name-$version.tar" "$name-$version"

rpmbuild -bs --nodeps --quiet \
    --define "_topdir $tmp" --define "_sourcedir $tmp/SOURCES" \
    --define "_srcrpmdir $out" "$spec"
ls "$out/$name-$version"-*.src.rpm
