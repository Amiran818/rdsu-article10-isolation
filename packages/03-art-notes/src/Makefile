PREFIX ?= /usr/local
CFLAGS ?= -O2 -Wall

all: art-notes

art-notes: notes.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ notes.c -lsqlite3 -lreadline

check: art-notes
	./art-notes test.db add first
	printf 'second\n' | ./art-notes test.db shell > /dev/null
	test "$$(./art-notes test.db list | cut -f2 | paste -sd,)" = "first,second"

install: all
	install -Dm755 art-notes $(DESTDIR)$(PREFIX)/bin/art-notes

.PHONY: all check install
