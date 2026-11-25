/* art-notes: заметки в базе SQLite; интерактивный ввод через readline
 *   art-notes DB add TEXT   - добавить заметку
 *   art-notes DB list       - показать заметки
 *   art-notes DB shell      - вводить заметки построчно (readline) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>
#include <readline/readline.h>
#include <readline/history.h>

static sqlite3 *db;

static int add(const char *text)
{
    sqlite3_stmt *st;
    int rc;

    sqlite3_prepare_v2(db, "INSERT INTO notes(text) VALUES (?)", -1, &st, NULL);
    sqlite3_bind_text(st, 1, text, -1, SQLITE_STATIC);
    rc = sqlite3_step(st) == SQLITE_DONE ? 0 : 1;
    sqlite3_finalize(st);
    return rc;
}

static int list(void)
{
    sqlite3_stmt *st;

    sqlite3_prepare_v2(db, "SELECT id, text FROM notes ORDER BY id", -1, &st, NULL);
    while (sqlite3_step(st) == SQLITE_ROW)
        printf("%d\t%s\n", sqlite3_column_int(st, 0),
               (const char *)sqlite3_column_text(st, 1));
    sqlite3_finalize(st);
    return 0;
}

static int shell(void)
{
    char *line;

    while ((line = readline("note> ")) != NULL) {
        if (*line) {
            add_history(line);
            add(line);
        }
        free(line);
    }
    return 0;
}

int main(int argc, char **argv)
{
    int rc = 2;

    if (argc < 3) {
        fprintf(stderr, "usage: art-notes DB add TEXT | list | shell\n");
        return 2;
    }
    if (sqlite3_open(argv[1], &db) != SQLITE_OK) {
        fprintf(stderr, "art-notes: %s\n", sqlite3_errmsg(db));
        return 1;
    }
    sqlite3_exec(db, "CREATE TABLE IF NOT EXISTS notes"
                     "(id INTEGER PRIMARY KEY, text TEXT)", NULL, NULL, NULL);
    if (!strcmp(argv[2], "add") && argc > 3)
        rc = add(argv[3]);
    else if (!strcmp(argv[2], "list"))
        rc = list();
    else if (!strcmp(argv[2], "shell"))
        rc = shell();
    sqlite3_close(db);
    return rc;
}
