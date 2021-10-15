use File::Find;

my $directory='[PATH]';
my @filelist = find(dir => $directory, name => / "." (pl|py|rb|js) $ /);

for @filelist -> $sfile {
    my @lines = $sfile.IO.lines;

    for @lines -> $sline {
        if $sline ~~ /[KEY]/ {
            say $sline;
        }
    }
}