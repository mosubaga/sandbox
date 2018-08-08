use strict;
use Data::Dumper;
use File::Find;
use File::Copy;

# -- main

{
  my $list_file = $ARGV[0];
  
  open(LIST,"<$list_file") or die "Cannot open $list_file\n";
  my @lines=<LIST>;
  close LIST;
  
  foreach my $line (@lines){
    chomp($line);
    if ($line=~/\w/){
      print "Converting $line to UNIX format ...\n";
      convert2unix($line);
    }
  }

  print "Finished conversion ...\n";
}

sub convert2unix($)
{
my $file = shift;
#############################################################
#
#############################################################

  my $backup_file = $file . ".bak";
  my $rm_backup = 1;
  
  open(DOS,"<$file") or die "Cannot open $file\n";
  binmode(DOS);
  open(OUT,">tmp.txt") or die "Cannot open tmp.txt\n";
  binmode(OUT);
  
  copy($file,$backup_file);
  while (my $line=<DOS>){
    $line=~s/(\s+)$//;
    print OUT "$line\n";
  }
  
  close DOS;
  close OUT;
  
  unlink($file);
  copy("tmp.txt",$file);
  unlink("tmp.txt");
  unlink $backup_file if ($rm_backup);
  
  print "Done converting $file ...\n\n";
}


