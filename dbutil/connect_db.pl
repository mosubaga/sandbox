#!/usr/bin/perl
use strict;
use warnings;
use DBI;

my $dbname   = "DBNAME";
my $username = "USERNAME";
my $password = "PASSWORD"

my $dbh = DBI->connect("DBI:mysql:database=$dbname;host=localhost",$username,$password);
die "failed to connect to MySQL database:DBI->errstr()" unless($dbh);

# prepare SQL statement
my $sth = $dbh->prepare("[SQL]") or die "prepare statement failed: $dbh->errstr()";

$sth->execute() or die "execution failed: $dbh->errstr()";

my @row=();

#output database results
while (@row=$sth->fetchrow_array())
{
   print "@row\n";
}

$dbh->disconnect();
print "Done\n";
