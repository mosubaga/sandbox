#!/usr/bin/perl

use strict;
use warnings;
use File::Copy qw(copy move);
use File::Path qw(make_path remove_tree);
use File::Basename qw(dirname);
use File::Find;

# Check if path exists
sub path_exists {
    my ($path) = @_;
    return defined($path) && -e $path;
}

# Check if file exists
sub file_exists {
    my ($path) = @_;
    return defined($path) && -f $path;
}

# Check if directory exists
sub dir_exists {
    my ($path) = @_;
    return defined($path) && -d $path;
}

# Read file into array of lines (chomped)
sub read_file_lines {
    my ($path) = @_;
    open my $fh, '<', $path or die "Unable to read $path: $!";
    my @lines = <$fh>;
    close $fh;
    chomp @lines;
    return @lines;
}

# Read file into single string
sub read_file {
    my ($path) = @_;
    open my $fh, '<', $path or die "Unable to read $path: $!";
    local $/;
    my $content = <$fh>;
    close $fh;
    return $content;
}

# Write string content to file (overwrite)
sub write_file {
    my ($path, $content) = @_;
    open my $fh, '>', $path or die "Unable to write $path: $!";
    print $fh $content // '';
    close $fh;
}

# Append string content to file
sub append_file {
    my ($path, $content) = @_;
    open my $fh, '>>', $path or die "Unable to append $path: $!";
    print $fh $content // '';
    close $fh;
}

# Ensure directory exists
sub ensure_dir {
    my ($path) = @_;
    return if dir_exists($path);
    make_path($path) or die "Unable to create directory $path: $!";
}

# Touch a file (create if missing, update mtime if exists)
sub touch_file {
    my ($path) = @_;
    if (!path_exists($path)) {
        open my $fh, '>', $path or die "Unable to create $path: $!";
        close $fh;
    } else {
        utime undef, undef, $path or die "Unable to update mtime for $path: $!";
    }
}

# List all entries in directory (excluding . and ..)
sub list_entries {
    my ($dir) = @_;
    opendir my $dh, $dir or die "Unable to open directory $dir: $!";
    my @entries = grep { $_ ne '.' && $_ ne '..' } readdir $dh;
    closedir $dh;
    return @entries;
}

# List files in directory
sub list_files {
    my ($dir) = @_;
    return grep { -f "$dir/$_" } list_entries($dir);
}

# List subdirectories in directory
sub list_dirs {
    my ($dir) = @_;
    return grep { -d "$dir/$_" } list_entries($dir);
}

# Copy a file
sub copy_file {
    my ($src, $dest) = @_;
    my $dest_dir = dirname($dest);
    ensure_dir($dest_dir) if defined $dest_dir && $dest_dir ne '';
    copy($src, $dest) or die "Unable to copy $src to $dest: $!";
}

# Copy a directory recursively
sub copy_dir {
    my ($src, $dest) = @_;
    die "Source directory not found: $src" unless dir_exists($src);
    ensure_dir($dest);

    find({
        no_chdir => 1,
        wanted => sub {
            my $path = $File::Find::name;
            return if $path eq $src;
            my $rel = $path;
            $rel =~ s/^\Q$src\E\/?//;
            my $target = "$dest/$rel";

            if (-d $path) {
                ensure_dir($target);
            } elsif (-f $path) {
                my $target_dir = dirname($target);
                ensure_dir($target_dir) if defined $target_dir && $target_dir ne '';
                copy($path, $target) or die "Unable to copy $path to $target: $!";
            }
        },
    }, $src);
}

# Move file or directory
sub move_path {
    my ($src, $dest) = @_;
    my $dest_dir = dirname($dest);
    ensure_dir($dest_dir) if defined $dest_dir && $dest_dir ne '';

    if (move($src, $dest)) {
        return;
    }

    if (-d $src) {
        copy_dir($src, $dest);
        remove_tree($src) or die "Unable to remove $src after copy: $!";
    } else {
        copy($src, $dest) or die "Unable to copy $src to $dest: $!";
        unlink $src or die "Unable to remove $src after copy: $!";
    }
}

# Delete file
sub delete_file {
    my ($path) = @_;
    return unless file_exists($path);
    unlink $path or die "Unable to delete $path: $!";
}

# Delete directory recursively
sub delete_dir {
    my ($path) = @_;
    return unless dir_exists($path);
    remove_tree($path) or die "Unable to delete directory $path: $!";
}

# Get file size in bytes
sub file_size {
    my ($path) = @_;
    return -s $path;
}

# Get file modification time (epoch seconds)
sub file_mtime {
    my ($path) = @_;
    return (stat($path))[9];
}

1;
