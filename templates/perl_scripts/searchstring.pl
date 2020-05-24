use strict;
use File::Find;
use File::Copy;
use Data::Dumper;

my @FILE_LIST=();
my $result_log = "result.log";

{
    open(OUT, ">$result_log") or die "Cannot open $result_log\n";
    my $rootDir = "[FolderPath]";
    my $keyword = "[Keyword]";
    
    print "\nGetting files from $rootDir ..\n";
    my @filelist = GetFileList($rootDir);
       
    foreach my $file (@filelist)
    {
       open(IN,"<$file") or die "Cannot open $file\n";
       my @lines = <IN>;
       close IN;

       my $i = 1;
       foreach my $line (@lines)
       {
	    print LOG "$file (" . $i . ")" . ": $line" if ($line=~/\Q$keyword\E/);
	    print "$file (" . $i . ")" . ": $line" if ($line=~/\Q$keyword\E/);
	    $i++;
       }	       
    }

    print "-- Scan complete --\n";
}

# ------------------------------------------------------------------------
sub GetFileList($)
# ------------------------------------------------------------------------
{
    my $root = shift;

    @FILE_LIST = ();
    find(\&filter, $root);
    return @FILE_LIST;
}

# ------------------------------------------------------------------------
sub filter 
# ------------------------------------------------------------------------
{
    my $root = $File::Find::topdir;
    my $path = $File::Find::name;
    my $file_name = $_;

    $root =~ s/\\/\\\\/g;
    push @FILE_LIST, $path if ($path =~ /(.+)\.py$/)
}

