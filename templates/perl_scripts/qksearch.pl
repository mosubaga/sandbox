#!/usr/bin/perl

use strict;
use warnings;

# main
{
    my ($folder, $term, $regex, $outfile, $help);

    parse_args(\@ARGV);

    if ($help) {
        print usage();
        exit 0;
    }

    if (!defined $folder || $folder eq q{}) {
        die ">> qksearch: -f <folder> is required\n";
    }

    if (!-d $folder) {
        die ">> qksearch: not a valid directory: $folder\n";
    }

    my $use_regex = defined $regex && $regex ne q{};
    my $pattern   = $use_regex ? $regex : $term;

    if (!defined $pattern || $pattern eq q{}) {
        die ">> qksearch: -t <term> or -e <regex> is required\n";
    }

    my $compiled_regex;
    if ($use_regex) {
        $compiled_regex = eval { qr/$regex/ };
        if ($@) {
            chomp $@;
            die ">> qksearch: invalid regex '$regex': $@\n";
        }
    }

    my $out_fh;
    if (defined $outfile && $outfile ne q{}) {
        open $out_fh, '>', $outfile
            or die ">> qksearch: cannot open output file: $outfile\n";
    }
    else {
        $out_fh = *STDOUT;
    }

    walk_tree($folder, sub {
        my ($path) = @_;

        return if !-f $path;
        return if -B $path;

        search_file($path, $pattern, $compiled_regex, $use_regex, $out_fh);
    });

    exit 0;
}

sub search_file {
    my ($path, $plain_pattern, $compiled, $use_regex, $out_fh) = @_;

    open my $in_fh, '<', $path
        or do {
            warn ">> qksearch: cannot open file, skipped: $path\n";
            return;
        };

    my $line_no = 0;

    while (my $line = <$in_fh>) {
        ++$line_no;

        my $found = $use_regex
            ? ($line =~ $compiled)
            : (index($line, $plain_pattern) >= 0);

        next if !$found;

        $line =~ s/^\s+//;
        $line =~ s/\s+$//;

        print {$out_fh} "[$path]($line_no): $line\n";
    }
}

sub walk_tree {
    my ($path, $callback) = @_;

    return if $path =~ m{(?:^|/)node_modules(?:/|$)};

    if (-d $path) {
        opendir my $dir_fh, $path
            or do {
                warn ">> qksearch: cannot open directory, skipped: $path\n";
                return;
            };

        while (my $entry = readdir $dir_fh) {
            next if $entry eq '.' || $entry eq '..';
            walk_tree("$path/$entry", $callback);
        }

        closedir $dir_fh;
        return;
    }

    $callback->($path);
}

sub parse_args {
    my ($argv) = @_;

    while (@{$argv}) {
        my $arg = shift @{$argv};

        if ($arg eq '-f' || $arg eq '--folder') {
            $folder = shift_arg($arg, $argv);
        }
        elsif ($arg eq '-t' || $arg eq '--term') {
            $term = shift_arg($arg, $argv);
        }
        elsif ($arg eq '-e' || $arg eq '--regex') {
            $regex = shift_arg($arg, $argv);
        }
        elsif ($arg eq '-o' || $arg eq '--output') {
            $outfile = shift_arg($arg, $argv);
        }
        elsif ($arg eq '-h' || $arg eq '--help') {
            $help = 1;
        }
        else {
            die ">> qksearch: unknown option: $arg\n";
        }
    }
}

sub shift_arg {
    my ($flag, $argv) = @_;

    if (!@{$argv}) {
        die ">> qksearch: missing value for $flag\n";
    }

    return shift @{$argv};
}

sub usage {
    return <<"USAGE";
Usage: $0 -f <folder> -t <term> [-e <regex>] [-o <outfile>]

  -f, --folder   folder path to search
  -t, --term     plain text term to search for
  -e, --regex    regular expression to search for (overrides -t)
  -o, --output   write output to this file instead of stdout
  -h, --help     show this help
USAGE
}
