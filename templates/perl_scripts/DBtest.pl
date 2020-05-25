use strict;
use DBI;

#open connection to Access database
my $dbh = DBI->connect('dbi:ODBC:driver=microsoft access driver (*.mdb);dbq=D:\Projects\testdb.mdb');

#prepare and execute SQL statement
my $sqlstatement=

"SELECT Master.nameFirst, Master.nameLast, '||',  Pitching.yearID, '||' , Pitching.W, Pitching.L, Pitching.SV
FROM Pitching,Master
WHERE Pitching.teamID = 'BOS' AND (Pitching.W > 5 OR Pitching.SV >20) AND Pitching.yearID > 2000 AND Master.playerID = Pitching.playerID ORDER BY Pitching.yearID";

my $sth = $dbh->prepare($sqlstatement);
$sth->execute or die "Could not execute SQL statement ... maybe invalid?";

my @row = ();

open (RESULT,">result.log") or die "Cannot open file\n";

#output database results
while (@row=$sth->fetchrow_array())
{
   print RESULT "@row\n";
}

$dbh->disconnect() if ($dbh);
close RESULT;

print "Done\n";
