use strict;
use Data::Dumper;
use File::Find;
use File::Copy;
use File::Basename;

my @FILE_LIST=();

{
   my $prefix = "<Some Prefix>";
   my $rootDir = '[FilePath]';
   my @videolist = GetFileList($rootDir);

   foreach my $file (@videolist)
   {
       my $filename = basename($file);
       $filename =~ s/ /_/g;
       $filename = $prefix . "_" . $filename;
       my $newpath = dirname($file) . "/" . $filename;
       copy($file,$newpath) or die "Cannot copy : $!";
   }

   print "-- Done --\n";
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

  if( $file_name =~ /\.mp4$/i ){
    push @FILE_LIST, $path;
  }
}