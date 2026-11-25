PREFIX ?= /usr/local
CFLAGS ?= -O2 -Wall

all: art-crc art-crc.1

art-crc: crc.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ crc.c -lz

art-crc.1: art-crc
	help2man -N --name="CRC-32 and Adler-32 checksums" -o $@ ./art-crc

check: art-crc
	test "$$(printf abc | ./art-crc | cut -d' ' -f1-2)" = "352441c2 024d0127"

install: all
	install -Dm755 art-crc $(DESTDIR)$(PREFIX)/bin/art-crc
	install -Dm644 art-crc.1 $(DESTDIR)$(PREFIX)/share/man/man1/art-crc.1

.PHONY: all check install
