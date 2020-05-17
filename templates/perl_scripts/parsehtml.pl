use LWP::Simple;
use strict;
use HTML::TreeBuilder;

# ---------
{
  my $URL = "[URL]";
  my $content = get($URL);
  warn "could not get $URL\n" unless (defined ($content = get($URL)));

  open(HTML,">:utf8","[HTML]") or die "Cannot open HTML file";
  my $title = Parse_Help_Text($content);
  print HTML $title . "\n";
  close HTML;

  print "-- Done --\n";
}
# -----

sub Parse_Help_Text($)
{
  my $html = shift;

  my $parser = HTML::TreeBuilder->new();
  my $success = $parser->parse($html);
  my $title = $html;

  foreach my $text ($parser->find("title")){
    $title = $text->as_text();
  }

  $parser->delete();

  return $title;
}