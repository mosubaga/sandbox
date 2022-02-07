use strict;
use Data::Dumper;
use File::Find;
use File::Copy;
use File::Basename;
use XML::DOM;

my @FILE_LIST=();

{
  my $rootdir = '[SRC]';
  my @filelist = GetFileList($rootdir);

  for my $file (@filelist){
    Parsetxlf($file);
  }

}

# -------------------------------------------------------------------------

sub Parsetxlf($)
{
   my $txlf = shift;
   my $tgtpath = '[TGT]';
   my $tbasename = basename($txlf);
   my $tgttxlf = $tgtpath . "\\" . $tbasename;

   my $parser = new XML::DOM::Parser;
   my $doc = $parser->parsefile ($txlf);

   my $nodes = $doc->getElementsByTagName("group");
   my $n = $nodes->getLength;

   for (my $i = 0; $i < $n; $i++)
   {
     my $node = $nodes->item($i);
     my $restype = $node->getAttributeNode("restype")->getValue;
     if ($restype eq "x-page"){
       my @children = $node->getChildNodes;
       for my $kid (@children){
         my $sKid = $kid->toString();
         unless ($sKid =~ /<target/){
           $node->removeChild($kid);
         }
       }
     }
   }

   # Print doc file
   $doc->printToFile ($tgttxlf);
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

  if( $file_name =~ /\.txlf$/i ){
    push @FILE_LIST, $path;
  }
}
