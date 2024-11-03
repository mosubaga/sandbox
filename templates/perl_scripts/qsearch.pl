
#!/usr/bin/perl

use strict;
use warnings;

my @FILE_LIST;


# Function to list files recursively
# ---------------------------------------------------------------------
sub list_files
# ---------------------------------------------------------------------
{
    my ($dir) = @_;

    # Open the directory
    opendir(my $dh, $dir) or die "Unable to open directory $dir: $!";

    # Read the directory contents
    my @files = readdir($dh);

    # Iterate through directory contents
    foreach my $file (@files) {
        next if $file eq '.' or $file eq '..'; # Skip '.' and '..' entries

        my $path = "$dir/$file"; # Full path of the file

        # If it's a directory, call the function recursively
        if (-d $path) {
            list_files($path);
        } else {
            # If it's a file, print its path
            push @FILE_LIST, $path if ($path =~ /(.+)\.(py|pl|js|html|go|cpp)$/)
        }
    }

    # Close the directory handle
    closedir($dh);

    return @FILE_LIST;
}


# Main 

{
    my $directory = "[FilePath]";
    my $keyword = "[Keyword]";

    list_files($directory);

    for my $file (@FILE_LIST) 
    {
        
        open(IN,"<$file") or die "Cannot open $file\n";
        my @lines = <IN>;
        close IN;

        my $i = 1;
        foreach my $line (@lines)
        {
            chomp($line);
            $line =~ s/^[\s|\t]+//;
            print "$file (" . $i . ")" . ": $line\n" if (index($line, $keyword) != -1);
            $i++;
       }
    }
}