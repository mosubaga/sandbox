use HTTP::UserAgent;
use JSON::Tiny;

my $url = '[URL]';

my $client = HTTP::UserAgent.new();
$client.timeout = 10;

my %data = from-json($resp.content);

my @output = %data<[fieldroot]>[];

for @output -> $sOut
{
    print $sOut{'[field2]'} ~ "\n";
}

