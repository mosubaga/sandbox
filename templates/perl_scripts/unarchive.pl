use strict;
use File::Find;
use File::Copy;
use File::Basename;
use Archive::Zip;

################################################################################
my $ROOT_DIR = $ARGV[0];
my @FILE_LIST;
my $DEBUG = 0;
################################################################################

my @xlz_list = GetFileList($ROOT_DIR);

foreach my $xlz_file (@xlz_list)
{
  UnzipXLZ($xlz_file);
  
  print "Uncompressing " . $xlz_file . "....\n";
}

print "Done\n";

################################################################################
################################################################################

sub UnzipXLZ($)
################################################################################
#
################################################################################
{
   my $dwb = shift;
   my $zip_file = $dwb;
   $zip_file =~ s/\.xlz/\.zip/;

   copy($dwb,$zip_file);
   my $unzip_path = dirname($zip_file);

   my $zip = Archive::Zip->new($zip_file);
   my @members = $zip->memberNames();

   my $xlf_file;

   foreach my $member (@members) {
    if ($member =~ /\.xlf/){
      my $status = $zip->extractMember($member,$unzip_path . "\\" . $member) if ($member =~ /\.xlf/);
      $xlf_file = $unzip_path . "\\" . $member;
    }
   }

   unlink($zip_file);

   return $xlf_file;
}

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

  if( $file_name =~ /\.xlz$/i )
  {
    $root =~ s/\\/\\\\/g;
#    $path =~ s/^$root[\/\\]//;
    push @FILE_LIST, $path;
  }
}

