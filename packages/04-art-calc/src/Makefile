PREFIX ?= /usr/local
CFLAGS ?= -O2 -Wall

all: art-calc art-calc.1

calc.tab.c calc.tab.h: calc.y
	bison -d calc.y

lex.yy.c: calc.l calc.tab.h
	flex calc.l

art-calc: calc.tab.c lex.yy.c
	$(CC) $(CFLAGS) -DYYSTYPE=long $(LDFLAGS) -o $@ calc.tab.c lex.yy.c

art-calc.1: art-calc.txt
	txt2man -t art-calc -s 1 -v "User Commands" art-calc.txt > $@

check: art-calc
	test "$$(printf '2+3*4\n(7-10)*-2\n17%%5\n' | ./art-calc | paste -sd,)" = "14,6,2"

install: all
	install -Dm755 art-calc $(DESTDIR)$(PREFIX)/bin/art-calc
	install -Dm644 art-calc.1 $(DESTDIR)$(PREFIX)/share/man/man1/art-calc.1

.PHONY: all check install
