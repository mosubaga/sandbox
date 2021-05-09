use strict;
use Data::Dumper;
use File::Find;
use File::Copy;
use File::Basename;

{
  open (PRO, "<test.properties") or die "Cannot open properties file\n"; 
  my @lines = <PRO>;
  close PRO;

  my $count = 0;

  open (TMP, ">tmp.txt") or die "Cannot open tmp.txt\n"; 
  my $line_no = scalar(@lines);

  while ($count < $line_no + 1){
    chomp($lines[$count]);
    if ($lines[$count] =~ /\\$/){
      $lines[$count] = FixMultiline(\@lines,\$count); 
    }
    
    print TMP $lines[$count] . "\n";

    $count++;
  }
  
  close TMP;

  print "Done\n";
}

sub FixMultiline($$)
{
  my ($lines_ref,$count_ref) = @_;
  my @lines = @{$lines_ref};
  my $count = $$count_ref;

  my $string = $lines[$count];

  while ($count < scalar(@lines)+1){
    unless ($lines[$count] =~ /\\$/){
      $string =~ s/\\//g;
      last;
    }
    else{
      chomp($lines[$count+1]);
      $string .= $lines[$count+1]; 
    }
   $count++;
  } 

  ${$count_ref} = $count;
  return $string;
}
