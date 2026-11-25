PREFIX ?= /usr/local
CFLAGS ?= -O2 -Wall

all: art-xq art-xq.1

art-xq: xq.c
	$(CC) $(CFLAGS) -I/usr/include/libxml2 $(LDFLAGS) -o $@ xq.c -lxml2

art-xq.1: art-xq.xml man.xsl
	xsltproc --nonet -o $@ man.xsl art-xq.xml

check: art-xq
	test "$$(./art-xq art-xq.xml 'count(//para)')" = "2"
	test "$$(./art-xq art-xq.xml 'string(/manpage/@section)')" = "1"

install: all
	install -Dm755 art-xq $(DESTDIR)$(PREFIX)/bin/art-xq
	install -Dm644 art-xq.1 $(DESTDIR)$(PREFIX)/share/man/man1/art-xq.1

.PHONY: all check install
