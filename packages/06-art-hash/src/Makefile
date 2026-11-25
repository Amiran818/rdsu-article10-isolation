PREFIX ?= /usr/local
LOCALEDIR ?= $(PREFIX)/share/locale
CFLAGS ?= -O2 -Wall

all: art-hash po/ru.mo README.html

art-hash: hash.c
	$(CC) $(CFLAGS) -DLOCALEDIR='"$(LOCALEDIR)"' $(LDFLAGS) -o $@ hash.c -lcrypto

po/ru.mo: po/ru.po
	msgfmt --check -o $@ po/ru.po

README.html: README.md
	markdown -o $@ README.md

check: art-hash
	printf abc > abc.txt
	./art-hash abc.txt | grep -q '^ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  abc.txt$$'

install: all
	install -Dm755 art-hash $(DESTDIR)$(PREFIX)/bin/art-hash
	install -Dm644 po/ru.mo $(DESTDIR)$(LOCALEDIR)/ru/LC_MESSAGES/art-hash.mo
	install -Dm644 README.html $(DESTDIR)$(PREFIX)/share/doc/art-hash/README.html

.PHONY: all check install
