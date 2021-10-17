use HTTP::UserAgent;
use JSON::Tiny;

my $url = '[URL]';

my $client = HTTP::UserAgent.new();
$client.timeout = 10;

my $resp = $client.get($url);
my %data = from-json($resp.content);

my @output = %data<['field1']>[];

for @output -> $sOut
{
    print $sOut{'field2'} ~ "\n";
}
