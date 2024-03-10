
#!/usr/bin/perl

use strict;
use warnings;

# Function to list files recursively
sub list_files {
    my ($dir) = @_;

    # Open the directory
    opendir(my $dh, $dir) or die "Unable to open directory $dir: $!";

    # Read the directory contents
    my @files = readdir($dh);

    # Close the directory handle
    closedir($dh);

    # Iterate through directory contents
    foreach my $file (@files) {
        next if $file eq '.' or $file eq '..'; # Skip '.' and '..' entries

        my $path = "$dir/$file"; # Full path of the file

        # If it's a directory, call the function recursively
        if (-d $path) {
            list_files($path);
        } else {
            # If it's a file, print its path
            print "$path\n";
        }
    }
}

# Main program
my $directory = shift || '.'; # Default to current directory if no argument provided
list_files($directory);