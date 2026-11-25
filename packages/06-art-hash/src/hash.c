/* art-hash: SHA-256 / SHA-512 файлов (OpenSSL EVP), сообщения
 * переведены через gettext
 *   art-hash [-5] FILE... */
#include <libintl.h>
#include <locale.h>
#include <stdio.h>
#include <string.h>
#include <openssl/evp.h>

#define _(s) gettext(s)
#ifndef LOCALEDIR
#define LOCALEDIR "/usr/share/locale"
#endif

static int digest(const EVP_MD *md, const char *name)
{
    unsigned char buf[65536], out[EVP_MAX_MD_SIZE];
    unsigned int len;
    size_t n;
    FILE *f = fopen(name, "rb");
    EVP_MD_CTX *ctx;

    if (!f) {
        fprintf(stderr, _("art-hash: cannot open %s\n"), name);
        return 1;
    }
    ctx = EVP_MD_CTX_new();
    EVP_DigestInit_ex(ctx, md, NULL);
    while ((n = fread(buf, 1, sizeof buf, f)) > 0)
        EVP_DigestUpdate(ctx, buf, n);
    EVP_DigestFinal_ex(ctx, out, &len);
    EVP_MD_CTX_free(ctx);
    fclose(f);
    for (unsigned int i = 0; i < len; i++)
        printf("%02x", out[i]);
    printf("  %s\n", name);
    return 0;
}

int main(int argc, char **argv)
{
    const EVP_MD *md = EVP_sha256();
    int i = 1, rc = 0;

    setlocale(LC_ALL, "");
    bindtextdomain("art-hash", LOCALEDIR);
    textdomain("art-hash");

    if (argc > 1 && !strcmp(argv[1], "-5")) {
        md = EVP_sha512();
        i++;
    }
    if (i >= argc) {
        fprintf(stderr, _("usage: art-hash [-5] FILE...\n"));
        return 2;
    }
    for (; i < argc; i++)
        rc |= digest(md, argv[i]);
    return rc;
}
