use strict;
use Data::Dumper;
use File::Find;
use File::Copy;

my @FILE_LIST=();

{
 
}

# -------------------------------------------------------------------------

sub GetFileList($)
{
my $root = shift;
#########################################################################
#
#########################################################################

  @FILE_LIST = ();
  find(\&filter, $root);
  return @FILE_LIST;
}

sub filter
{
#########################################################################
#
#########################################################################

  my $root = $File::Find::topdir;
  my $path = $File::Find::name;
  my $file_name = $_;

  if( $file_name =~ /\.html$/i ){
    push @FILE_LIST, $path;
  }
}