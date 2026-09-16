/*
 * qrep.c
 *
 * A small grep-like tool built with GLib that recursively scans a
 * directory tree and prints every line matching a given pattern
 * (regex), along with the file name and line number.
 *
 * Build:
 *   gcc qrep.c $(pkg-config --cflags --libs glib-2.0) -o qrep
 *
 * Usage:
 *   ./qrep [OPTIONS] PATTERN DIRECTORY
 *
 * Options:
 *   -i, --ignore-case     Case-insensitive matching
 *   -n, --no-line-number  Hide line numbers in the output
 *
 * Example:
 *   ./qrep -i "error" ./logs
 */

#include <glib.h>
#include <stdio.h>

/* Options set via GOptionContext */
static gboolean ignore_case     = FALSE;
static gboolean hide_linenum    = FALSE;

static GOptionEntry entries[] = {
    { "ignore-case",    'i', 0, G_OPTION_ARG_NONE, &ignore_case,
      "Case-insensitive matching", NULL },
    { "no-line-number", 'n', 0, G_OPTION_ARG_NONE, &hide_linenum,
      "Hide line numbers in output", NULL },
    { NULL }
};

/* Search a single file for lines matching the compiled regex. */
static void
search_file(const gchar *path, GRegex *regex)
{
    g_autoptr(GError) error = NULL;
    g_autoptr(GIOChannel) channel = g_io_channel_new_file(path, "r", &error);

    if (!channel) {
        /* Skip files we can't open (permissions, broken symlinks, etc.) */
        g_printerr("Warning: could not open '%s': %s\n", path, error->message);
        return;
    }

    /* Treat file content as raw bytes, not a specific text encoding,
     * so binary or non-UTF8 files don't abort the scan. */
    g_io_channel_set_encoding(channel, NULL, NULL);

    gchar *line = NULL;
    gsize len = 0;
    gint lineno = 0;
    GIOStatus status;

    while ((status = g_io_channel_read_line(channel, &line, &len, NULL, NULL))
           == G_IO_STATUS_NORMAL) {
        lineno++;

        if (g_regex_match(regex, line, 0, NULL)) {
            if (hide_linenum)
                g_print("%s: %s", path, line);
            else
                g_print("%s:%d: %s", path, lineno, line);

            /* Ensure a trailing newline even if the last line lacked one */
            if (len == 0 || line[len - 1] != '\n')
                g_print("\n");
        }

        g_free(line);
        line = NULL;
    }

    if (status == G_IO_STATUS_ERROR)
        g_printerr("Warning: error reading '%s'\n", path);
}

/* Recursively walk a directory, searching every regular file found. */
static void
scan_directory(const gchar *dirpath, GRegex *regex)
{
    g_autoptr(GError) error = NULL;
    g_autoptr(GDir) dir = g_dir_open(dirpath, 0, &error);

    if (!dir) {
        g_printerr("Warning: could not open directory '%s': %s\n",
                   dirpath, error->message);
        return;
    }

    const gchar *name;
    while ((name = g_dir_read_name(dir)) != NULL) {
        g_autofree gchar *full_path = g_build_filename(dirpath, name, NULL);

        if (g_file_test(full_path, G_FILE_TEST_IS_DIR)) {
            scan_directory(full_path, regex);
        } else if (g_file_test(full_path, G_FILE_TEST_IS_REGULAR)) {
            search_file(full_path, regex);
        }
        /* Symlinks, sockets, etc. are silently skipped */
    }
}

int
main(int argc, char **argv)
{
    g_autoptr(GError) error = NULL;
    g_autoptr(GOptionContext) context =
        g_option_context_new("PATTERN DIRECTORY - recursively search files for a pattern");

    g_option_context_add_main_entries(context, entries, NULL);

    if (!g_option_context_parse(context, &argc, &argv, &error)) {
        g_printerr("Option parsing failed: %s\n", error->message);
        return 1;
    }

    if (argc != 3) {
        g_printerr("%s", g_option_context_get_help(context, TRUE, NULL));
        return 1;
    }

    const gchar *pattern = argv[1];
    const gchar *directory = argv[2];

    GRegexCompileFlags flags = ignore_case ? G_REGEX_CASELESS : 0;

    g_autoptr(GRegex) regex = g_regex_new(pattern, flags, 0, &error);
    if (!regex) {
        g_printerr("Invalid pattern '%s': %s\n", pattern, error->message);
        return 1;
    }

    if (!g_file_test(directory, G_FILE_TEST_IS_DIR)) {
        g_printerr("'%s' is not a directory\n", directory);
        return 1;
    }

    scan_directory(directory, regex);

    return 0;
}

// build.sh
// gcc main.c $(pkg-config --cflags --libs glib-2.0) -o qrep