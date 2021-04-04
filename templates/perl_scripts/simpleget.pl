use strict;
use Encode;
use LWP::UserAgent;
use LWP::Simple;
use HTTP::Request;
use Data::Dumper;
use JSON;

# sudo apt-get install emboss bioperl ncbi-blast+ gzip libjson-perl libtext-csv-perl libfile-slurp-perl liblwp-protocol-https-perl libwww-perl libjson-perl
# ------
# __main__
# ------
{
    my $sURL = "[sURL]";
    my $sContent = getResponse($sURL);
    my $json_text = decode_json($sContent);
    for my $object (@$json_text) {

        my $fDeathRate = 0;
        if ($object->{'positive'} > 0){
            $fDeathRate = ($object->{'death'} / $object->{'positive'}) * 100;
        }
        print $object->{'state'} , " " , $object->{'positive'}, " ", $object->{'death'} , " ", $fDeathRate;
        print "\n";
    }
}

# --------------------------------------------------------------------
sub getResponse($)
# --------------------------------------------------------------------
{
    my $sURL = shift;
    my $header = ['Content-Type' => 'application/json; charset=UTF-8'];
    my $useragent = LWP::UserAgent->new;
    my $req = HTTP::Request->new("GET", $sURL, $header);
    my $res = $useragent->request($req);
    my $sResponse = $res->content;
    $sResponse = decode("utf8",$sResponse);

    open(OUT,">:utf8","out.json") or die "Cannot open out.json";
    print OUT $sResponse;
    close OUT;

    return $sResponse;
}