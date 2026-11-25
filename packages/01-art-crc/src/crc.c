/* art-crc: контрольные суммы CRC-32 и Adler-32 файлов (zlib) */
#include <stdio.h>
#include <string.h>
#include <zlib.h>

#define VERSION "1.0"

static int sum_file(const char *name)
{
    FILE *f = strcmp(name, "-") ? fopen(name, "rb") : stdin;
    unsigned char buf[65536];
    uLong crc = crc32(0L, Z_NULL, 0), adl = adler32(0L, Z_NULL, 0);
    size_t n;

    if (!f) {
        perror(name);
        return 1;
    }
    while ((n = fread(buf, 1, sizeof buf, f)) > 0) {
        crc = crc32(crc, buf, (uInt)n);
        adl = adler32(adl, buf, (uInt)n);
    }
    if (f != stdin)
        fclose(f);
    printf("%08lx %08lx %s\n", crc, adl, name);
    return 0;
}

int main(int argc, char **argv)
{
    int rc = 0;

    if (argc > 1 && !strcmp(argv[1], "--help")) {
        puts("Usage: art-crc [FILE]...\n"
             "Print CRC-32 and Adler-32 checksums of FILEs (stdin if none).\n\n"
             "  --help     display this help and exit\n"
             "  --version  output version information and exit");
        return 0;
    }
    if (argc > 1 && !strcmp(argv[1], "--version")) {
        printf("art-crc " VERSION " (zlib %s)\n", zlibVersion());
        return 0;
    }
    if (argc == 1)
        return sum_file("-");
    for (int i = 1; i < argc; i++)
        rc |= sum_file(argv[i]);
    return rc;
}
