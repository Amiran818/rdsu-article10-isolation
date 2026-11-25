/* art-ini: чтение значений из INI-файла (GLib GKeyFile)
 *   art-ini [--list] FILE [GROUP KEY] */
#include <glib.h>
#include <stdio.h>

static gboolean list_all;

static GOptionEntry entries[] = {
    { "list", 'l', 0, G_OPTION_ARG_NONE, &list_all, "List all groups and keys", NULL },
    { NULL }
};

int main(int argc, char **argv)
{
    GOptionContext *ctx = g_option_context_new("FILE [GROUP KEY]");
    GKeyFile *kf = g_key_file_new();
    GError *err = NULL;
    int rc = 0;

    g_option_context_add_main_entries(ctx, entries, NULL);
    if (!g_option_context_parse(ctx, &argc, &argv, &err) ||
        (argc != 2 && argc != 4) ||
        !g_key_file_load_from_file(kf, argv[1], G_KEY_FILE_NONE, &err)) {
        g_printerr("art-ini: %s\n", err ? err->message : "wrong arguments");
        rc = 2;
    } else if (list_all || argc == 2) {
        gchar **groups = g_key_file_get_groups(kf, NULL);
        for (gchar **g = groups; *g; g++) {
            gchar **keys = g_key_file_get_keys(kf, *g, NULL, NULL);
            for (gchar **k = keys; *k; k++)
                g_print("%s.%s\n", *g, *k);
            g_strfreev(keys);
        }
        g_strfreev(groups);
    } else {
        gchar *v = g_key_file_get_string(kf, argv[2], argv[3], &err);
        if (v)
            g_print("%s\n", v);
        else {
            g_printerr("art-ini: %s\n", err->message);
            rc = 1;
        }
        g_free(v);
    }
    g_clear_error(&err);
    g_key_file_free(kf);
    g_option_context_free(ctx);
    return rc;
}
