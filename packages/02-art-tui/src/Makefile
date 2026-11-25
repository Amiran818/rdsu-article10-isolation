PREFIX ?= /usr/local
CFLAGS ?= -O2 -Wall
PKG_CFLAGS := $(shell pkg-config --cflags ncursesw)
PKG_LIBS := $(shell pkg-config --libs ncursesw)

all: art-tui art-tui.1

art-tui: tui.c
	$(CC) $(CFLAGS) $(PKG_CFLAGS) $(LDFLAGS) -o $@ tui.c $(PKG_LIBS)

art-tui.1: art-tui.1.scd
	scdoc < art-tui.1.scd > $@

check: art-tui
	./art-tui --dump hello | grep -q ' 12 37 hello$$'

install: all
	install -Dm755 art-tui $(DESTDIR)$(PREFIX)/bin/art-tui
	install -Dm644 art-tui.1 $(DESTDIR)$(PREFIX)/share/man/man1/art-tui.1

.PHONY: all check install
