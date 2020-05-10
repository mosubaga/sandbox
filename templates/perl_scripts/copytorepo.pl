use strict;
use File::Copy;
use File::Find;

################################################################################

my @FILE_LIST;

{

   Help('usage') unless ($ARGV[0]);
   Help('full') if ($ARGV[0] eq 'help');

   open (LOG, ">copy.log") or die "Cannot create log file..\n";

   my $src_folder = $ARGV[0];
   my $tgt_folder = $ARGV[1];;

   my @copy_files = GetFileList($src_folder);

   foreach my $files (@copy_files)
   {
     my $tgt_lang;
     my $src_file = $src_folder . "\/" . $files;
     my $tgt_file = $tgt_folder . "\/" . $files;

     if ($files =~ /[\/\\]en-US[\/\\]/i)
     {
       if ($files =~ /\.(\w\w-\w\w)\.resx$/i)
       {
         $tgt_lang = $1;
       }

       $tgt_file =~ s/en-US/$tgt_lang/i;

       # Remove .en-US from the generated file name.
       #
       $tgt_file =~ s/\.en-US// if ($files =~ /\.en-US\.\w\w-\w\w\.resx/);

       # Remove read-only attributes
       #
       system("attrib -r \"$tgt_file\"");
       copy($src_file,$tgt_file) or die "Copy failed: $!";
       print "Copying $src_file -> $tgt_file..\n";
       print LOG "Copying $src_file -> $tgt_file..\n";
     }
     else
     {
        # Remove .en-US from the generated file name.
        #
        $tgt_file =~ s/\.en-US// if ($files =~ /\.en-US\.\w\w-\w\w\.resx/);

        # Remove read-only attributes
        #
        system("attrib -r \"$tgt_file\"");
        copy($src_file,$tgt_file) or die "Copy failed: $!";
        print "Copying $src_file -> $tgt_file..\n";
        print LOG "Copying $src_file -> $tgt_file..\n";
     }
   }

   close LOG;
   print "Done copying files...\n"
}


#############################################################################

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

  if( $file_name =~ /\.(resx|js|wxl|xml)$/i )
  {
    $root =~ s/\\/\\\\/g;
    $path =~ s/^$root[\/\\]//;
    push @FILE_LIST, $path;
  }
}

sub Help($)
{
my $mode = shift;
############################################################################
#
############################################################################

  if( $mode eq 'usage' )
  {
    print <<End_of_Usage;

    Usage: copytogit.pl <src_folder> <tgt_folder>

    Where: src_folder -> location of the generated files
           tgt_folder -> SVN Repository


End_of_Usage
  }
  else
  {
     print <<End_of_Help;

     This script will copy the localized files from the generated location to the git repository.

     Usage: copytogit.pl <src_folder> <tgt_folder>

     Where: src_folder -> location of the generated files
            tgt_folder -> SVN Repository

End_of_Help

  }
  exit;

}
