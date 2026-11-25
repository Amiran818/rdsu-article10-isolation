/* art-tui: рамка с текстом в терминале (ncursesw); --dump печатает
 * вычисленную разметку без запуска экранного режима */
#include <curses.h>
#include <locale.h>
#include <stdio.h>
#include <string.h>

static void layout(int rows, int cols, const char *msg, int *y, int *x)
{
    *y = rows / 2;
    *x = (cols - (int)strlen(msg)) / 2;
    if (*x < 1)
        *x = 1;
}

int main(int argc, char **argv)
{
    const char *msg = argc > 2 ? argv[2] : "art-tui";
    int y, x;

    if (argc > 1 && !strcmp(argv[1], "--dump")) {
        layout(24, 80, msg, &y, &x);
        printf("%s %d %d %s\n", curses_version(), y, x, msg);
        return 0;
    }
    if (argc > 1)
        msg = argv[1];
    setlocale(LC_ALL, "");
    initscr();
    noecho();
    curs_set(0);
    box(stdscr, 0, 0);
    layout(LINES, COLS, msg, &y, &x);
    mvaddstr(y, x, msg);
    mvaddstr(LINES - 2, 2, "press any key");
    refresh();
    getch();
    endwin();
    return 0;
}
