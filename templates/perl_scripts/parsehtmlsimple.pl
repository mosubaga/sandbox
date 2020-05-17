use strict;
use HTML::TreeBuilder;

my $body = "[HTML]";

my $tree = HTML::TreeBuilder->new;
$tree->parse_file($body);
$tree->eof();

foreach $a ($tree->find("a")) {
  print "Topic: " . $a->as_text() . "\n";
  print "Link: " . $a->attr('href') . "\n";
  print "\n";
}

exit;
