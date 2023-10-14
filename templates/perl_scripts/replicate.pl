#! /usr/bin/perl

use strict;
use File::Find;
use File::Copy;
use File::Path qw(make_path remove_tree);
use File::Basename;
use Data::Dumper;

my @FILELIST = ();

# Recursively list all the files in the directory.
sub list_files
{
  my $dir = shift;

  # Open the directory.
  opendir DIR, $dir or die "Couldn't open directory '$dir': $!";

  # Read the directory entries.
  my @files = readdir DIR or die "Couldn't read directory '$dir': $!";

  # Close the directory.
  closedir DIR;

  # Print the list of files.
  foreach my $file (@files) {
    # Skip the current and parent directory entries.
    next if $file eq "." or $file eq "..";

    # If the file is a directory, recursively list the files in that directory.
    if (-d "$dir/$file") {
      list_files("$dir/$file");
    } else {
      push @FILELIST, "$dir/$file";
    }
  }

  return @FILELIST;
}

# main
{
    my $srcdirectory = "[src_dir]";
    my $tgtdirectory = "[tgt_dir]";
    my @filelist = list_files($srcdirectory);

    if (-e $tgtdirectory)
    {
        print ":: Removing old backup from $tgtdirectory ::\n";
        remove_tree($tgtdirectory);
    }

    foreach my $file (@filelist)
    {
        if ($file =~ /[filter]/)
        {
            my $dirname = dirname($file);
            my $tgtfile = $file;
            $tgtfile =~ s/$srcdirectory/$tgtdirectory/;
            $dirname =~ s/$srcdirectory/$tgtdirectory/;

            unless (-e $dirname)
            {
                make_path($dirname);
            }

            print ":: Copying $file to $tgtfile\n";
            copy($file, $tgtfile) or warn "Copy failed: $!";
        }
    }

    print ":: Done creating backup ::\n";
}