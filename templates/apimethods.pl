use strict;
use Encode;
use File::Slurp;
use LWP::UserAgent;
use LWP::Simple;
use HTTP::Request;
use Data::Dumper;

# ------
# __main__
# ------
{
  my $sProd   = $ARGV[0];
  my $sMethod = $ARGV[1];
  my $sURI    = $ARGV[2];

  getResponse($sProd,$sMethod,$sURI);
}

# --------------------------------------------------------------------
sub getResponse($$$)
# --------------------------------------------------------------------
{
  my $hProd = {
 .  '<product_key>' => '<product_value>'
  };

  my $header = ['Content-Type' => 'application/json; charset=UTF-8'];
  my ($sProd,$sMethod,$sURI) = @_;
  my $sURL = $hProd->{$sProd} . $sURI;
  $sMethod = uc($sMethod);
  my $useragent = LWP::UserAgent->new;

  if ($sMethod=~/(GET|DELETE)/)
  {
    my $req = HTTP::Request->new($sMethod, $sURL, $header);
    my $res = $useragent->request($req);
    my $sResponse = $res->as_string;
    $sResponse = decode("utf8",$sResponse);

    open(OUT,">:utf8","out.json") or die "Cannot open out.json";
    print OUT $sResponse;
    close OUT;

    print $sResponse;
  }
  elsif ($sMethod=~/(POST|PUT|PATCH)/)
  {
    my $sContent = read_file("data.json");
    my $req = HTTP::Request->new($sMethod, $sURL, $header, $sContent);
    my $res = $useragent->request($req);
    my $sResponse = $res->as_string;
    $sResponse = decode("utf8",$sResponse);

    open(OUT,">:utf8","out.json") or die "Cannot open out.json";
    print OUT $sResponse;
    close OUT;

    print $sResponse;
  }
  else
  {
    print "ERROR:: Unknown method."
  }
}
