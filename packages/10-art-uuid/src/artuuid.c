/* art-uuid: генерация и разбор UUID (libuuid)
 *   art-uuid [-r | -t] [N]   - N идентификаторов (random / time)
 *   art-uuid -p UUID          - тип и вариант UUID */
#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <uuid/uuid.h>

static int parse(const char *s)
{
    uuid_t u;

    if (uuid_parse(s, u) != 0) {
        fprintf(stderr, "art-uuid: invalid UUID: %s\n", s);
        return 1;
    }
    printf("version %d variant %d\n", uuid_type(u), uuid_variant(u));
    return 0;
}

int main(int argc, char **argv)
{
    void (*gen)(uuid_t) = uuid_generate_random;
    char out[37];
    uuid_t u;
    int i = 1, n = 1;

    if (argc > 1 && !strcmp(argv[1], "--version")) {
        puts(PACKAGE_STRING);
        return 0;
    }
    if (argc > 2 && !strcmp(argv[1], "-p"))
        return parse(argv[2]);
    if (argc > 1 && !strcmp(argv[1], "-t")) {
        gen = uuid_generate_time;
        i++;
    } else if (argc > 1 && !strcmp(argv[1], "-r")) {
        i++;
    }
    if (i < argc)
        n = atoi(argv[i]);
    while (n-- > 0) {
        gen(u);
        uuid_unparse_lower(u, out);
        puts(out);
    }
    return 0;
}
