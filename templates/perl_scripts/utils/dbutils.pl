#!/usr/bin/env perl

use strict;
use warnings;
use DBI;
use Data::Dumper;

# ===================================================================
# CONNECTION MANAGEMENT
# ===================================================================

# Connect to MySQL database
sub db_connect {
    my ($host, $database, $username, $password, $port) = @_;
    $host //= 'localhost';
    $port //= 3306;
    
    my $dsn = "DBI:mysql:database=$database;host=$host;port=$port";
    my $dbh = DBI->connect($dsn, $username, $password, {
        RaiseError => 1,
        PrintError => 0,
        AutoCommit => 1,
        mysql_enable_utf8 => 1,
    }) or die "Could not connect to database: " . DBI->errstr;
    
    return $dbh;
}

# Disconnect from database
sub db_disconnect {
    my ($dbh) = @_;
    $dbh->disconnect() if $dbh;
}

# Test database connection
sub test_connection {
    my ($dbh) = @_;
    eval {
        my $sth = $dbh->prepare("SELECT 1");
        $sth->execute();
        $sth->finish();
    };
    return !$@;
}

# ===================================================================
# DATABASE DISCOVERY
# ===================================================================

# List all databases
sub list_databases {
    my ($dbh) = @_;
    my $sth = $dbh->prepare("SHOW DATABASES");
    $sth->execute();
    my @databases;
    while (my ($db) = $sth->fetchrow_array()) {
        push @databases, $db;
    }
    return @databases;
}

# List all tables in current database
sub list_tables {
    my ($dbh) = @_;
    my $sth = $dbh->prepare("SHOW TABLES");
    $sth->execute();
    my @tables;
    while (my ($table) = $sth->fetchrow_array()) {
        push @tables, $table;
    }
    return @tables;
}

# Get table structure/schema
sub describe_table {
    my ($dbh, $table) = @_;
    my $sth = $dbh->prepare("DESCRIBE $table");
    $sth->execute();
    my @columns;
    while (my $row = $sth->fetchrow_hashref()) {
        push @columns, $row;
    }
    return @columns;
}

# Get column names only
sub get_column_names {
    my ($dbh, $table) = @_;
    my @columns = describe_table($dbh, $table);
    return map { $_->{Field} } @columns;
}

# Get primary key columns
sub get_primary_keys {
    my ($dbh, $table) = @_;
    my $sth = $dbh->prepare("SHOW KEYS FROM $table WHERE Key_name = 'PRIMARY'");
    $sth->execute();
    my @keys;
    while (my $row = $sth->fetchrow_hashref()) {
        push @keys, $row->{Column_name};
    }
    return @keys;
}

# Get table indexes
sub get_indexes {
    my ($dbh, $table) = @_;
    my $sth = $dbh->prepare("SHOW INDEXES FROM $table");
    $sth->execute();
    my @indexes;
    while (my $row = $sth->fetchrow_hashref()) {
        push @indexes, $row;
    }
    return @indexes;
}

# Get foreign keys
sub get_foreign_keys {
    my ($dbh, $table, $database) = @_;
    my $sql = qq{
        SELECT 
            COLUMN_NAME,
            REFERENCED_TABLE_NAME,
            REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
        AND REFERENCED_TABLE_NAME IS NOT NULL
    };
    my $sth = $dbh->prepare($sql);
    $sth->execute($database, $table);
    my @fkeys;
    while (my $row = $sth->fetchrow_hashref()) {
        push @fkeys, $row;
    }
    return @fkeys;
}

# Get row count
sub get_row_count {
    my ($dbh, $table) = @_;
    my $sth = $dbh->prepare("SELECT COUNT(*) FROM $table");
    $sth->execute();
    my ($count) = $sth->fetchrow_array();
    return $count;
}

# ===================================================================
# QUERY OPERATIONS
# ===================================================================

# Execute SELECT query and return all rows as array of hashes
sub query_all {
    my ($dbh, $sql, @bind_values) = @_;
    my $sth = $dbh->prepare($sql);
    $sth->execute(@bind_values);
    my @results;
    while (my $row = $sth->fetchrow_hashref()) {
        push @results, $row;
    }
    return @results;
}

# Execute SELECT query and return first row
sub query_one {
    my ($dbh, $sql, @bind_values) = @_;
    my $sth = $dbh->prepare($sql);
    $sth->execute(@bind_values);
    return $sth->fetchrow_hashref();
}

# Execute SELECT query and return single value
sub query_value {
    my ($dbh, $sql, @bind_values) = @_;
    my $sth = $dbh->prepare($sql);
    $sth->execute(@bind_values);
    my ($value) = $sth->fetchrow_array();
    return $value;
}

# Select all records from table
sub select_all {
    my ($dbh, $table, $limit) = @_;
    my $sql = "SELECT * FROM $table";
    $sql .= " LIMIT $limit" if defined $limit;
    return query_all($dbh, $sql);
}

# Select with WHERE clause
sub select_where {
    my ($dbh, $table, $where_hash, $limit) = @_;
    my @columns = keys %$where_hash;
    my @values = values %$where_hash;
    
    my $where_clause = join(' AND ', map { "$_ = ?" } @columns);
    my $sql = "SELECT * FROM $table WHERE $where_clause";
    $sql .= " LIMIT $limit" if defined $limit;
    
    return query_all($dbh, $sql, @values);
}

# Select specific columns
sub select_columns {
    my ($dbh, $table, $columns_ref, $where_hash, $limit) = @_;
    my $columns = join(', ', @$columns_ref);
    my $sql = "SELECT $columns FROM $table";
    
    my @values;
    if ($where_hash && keys %$where_hash) {
        my @where_cols = keys %$where_hash;
        @values = values %$where_hash;
        my $where_clause = join(' AND ', map { "$_ = ?" } @where_cols);
        $sql .= " WHERE $where_clause";
    }
    
    $sql .= " LIMIT $limit" if defined $limit;
    return query_all($dbh, $sql, @values);
}

# Search table with LIKE
sub search_table {
    my ($dbh, $table, $column, $search_term, $limit) = @_;
    my $sql = "SELECT * FROM $table WHERE $column LIKE ?";
    $sql .= " LIMIT $limit" if defined $limit;
    return query_all($dbh, $sql, "%$search_term%");
}

# ===================================================================
# INSERT OPERATIONS
# ===================================================================

# Insert single row
sub insert_row {
    my ($dbh, $table, $data_hash) = @_;
    my @columns = keys %$data_hash;
    my @values = values %$data_hash;
    
    my $columns_str = join(', ', @columns);
    my $placeholders = join(', ', ('?') x @columns);
    
    my $sql = "INSERT INTO $table ($columns_str) VALUES ($placeholders)";
    my $sth = $dbh->prepare($sql);
    $sth->execute(@values);
    
    return $dbh->last_insert_id(undef, undef, $table, undef);
}

# Insert multiple rows
sub insert_rows {
    my ($dbh, $table, @data_array) = @_;
    return unless @data_array;
    
    my $first_row = $data_array[0];
    my @columns = keys %$first_row;
    my $columns_str = join(', ', @columns);
    my $placeholders = join(', ', ('?') x @columns);
    
    my $sql = "INSERT INTO $table ($columns_str) VALUES ($placeholders)";
    my $sth = $dbh->prepare($sql);
    
    my @inserted_ids;
    foreach my $row (@data_array) {
        my @values = @{$row}{@columns};
        $sth->execute(@values);
        push @inserted_ids, $dbh->last_insert_id(undef, undef, $table, undef);
    }
    
    return @inserted_ids;
}

# ===================================================================
# UPDATE OPERATIONS
# ===================================================================

# Update records
sub update_rows {
    my ($dbh, $table, $data_hash, $where_hash) = @_;
    
    my @set_columns = keys %$data_hash;
    my @set_values = values %$data_hash;
    
    my @where_columns = keys %$where_hash;
    my @where_values = values %$where_hash;
    
    my $set_clause = join(', ', map { "$_ = ?" } @set_columns);
    my $where_clause = join(' AND ', map { "$_ = ?" } @where_columns);
    
    my $sql = "UPDATE $table SET $set_clause WHERE $where_clause";
    my $sth = $dbh->prepare($sql);
    $sth->execute(@set_values, @where_values);
    
    return $sth->rows();
}

# Update by primary key
sub update_by_id {
    my ($dbh, $table, $id, $data_hash) = @_;
    my @pk_cols = get_primary_keys($dbh, $table);
    die "Table $table has no primary key" unless @pk_cols;
    die "Composite primary keys not supported in this function" if @pk_cols > 1;
    
    my $pk_col = $pk_cols[0];
    return update_rows($dbh, $table, $data_hash, { $pk_col => $id });
}

# ===================================================================
# DELETE OPERATIONS
# ===================================================================

# Delete records
sub delete_rows {
    my ($dbh, $table, $where_hash) = @_;
    
    my @where_columns = keys %$where_hash;
    my @where_values = values %$where_hash;
    
    my $where_clause = join(' AND ', map { "$_ = ?" } @where_columns);
    
    my $sql = "DELETE FROM $table WHERE $where_clause";
    my $sth = $dbh->prepare($sql);
    $sth->execute(@where_values);
    
    return $sth->rows();
}

# Delete by primary key
sub delete_by_id {
    my ($dbh, $table, $id) = @_;
    my @pk_cols = get_primary_keys($dbh, $table);
    die "Table $table has no primary key" unless @pk_cols;
    die "Composite primary keys not supported in this function" if @pk_cols > 1;
    
    my $pk_col = $pk_cols[0];
    return delete_rows($dbh, $table, { $pk_col => $id });
}

# Truncate table (delete all rows)
sub truncate_table {
    my ($dbh, $table) = @_;
    my $sql = "TRUNCATE TABLE $table";
    $dbh->do($sql);
}

# ===================================================================
# TRANSACTION SUPPORT
# ===================================================================

# Begin transaction
sub begin_transaction {
    my ($dbh) = @_;
    $dbh->begin_work();
}

# Commit transaction
sub commit_transaction {
    my ($dbh) = @_;
    $dbh->commit();
}

# Rollback transaction
sub rollback_transaction {
    my ($dbh) = @_;
    $dbh->rollback();
}

# Execute code in transaction
sub with_transaction {
    my ($dbh, $code_ref) = @_;
    
    eval {
        begin_transaction($dbh);
        $code_ref->();
        commit_transaction($dbh);
    };
    
    if ($@) {
        rollback_transaction($dbh);
        die "Transaction failed: $@";
    }
}

# ===================================================================
# UTILITY FUNCTIONS
# ===================================================================

# Print table structure in readable format
sub print_table_structure {
    my ($dbh, $table) = @_;
    my @columns = describe_table($dbh, $table);
    
    print "Table: $table\n";
    print "=" x 80, "\n";
    printf("%-20s %-15s %-8s %-8s %-20s\n", "Column", "Type", "Null", "Key", "Extra");
    print "-" x 80, "\n";
    
    foreach my $col (@columns) {
        printf("%-20s %-15s %-8s %-8s %-20s\n",
            $col->{Field},
            $col->{Type},
            $col->{Null},
            $col->{Key} // '',
            $col->{Extra} // ''
        );
    }
    print "=" x 80, "\n\n";
}

# Print query results in table format
sub print_results {
    my (@results) = @_;
    return unless @results;
    
    my @columns = keys %{$results[0]};
    
    # Calculate column widths
    my %widths;
    foreach my $col (@columns) {
        $widths{$col} = length($col);
        foreach my $row (@results) {
            my $val = $row->{$col} // '';
            my $len = length($val);
            $widths{$col} = $len if $len > $widths{$col};
        }
    }
    
    # Print header
    my $total_width = 0;
    foreach my $col (@columns) {
        printf("%-*s  ", $widths{$col}, $col);
        $total_width += $widths{$col} + 2;
    }
    print "\n", "-" x $total_width, "\n";
    
    # Print rows
    foreach my $row (@results) {
        foreach my $col (@columns) {
            printf("%-*s  ", $widths{$col}, $row->{$col} // '');
        }
        print "\n";
    }
    print "\n";
}

# Export results to CSV
sub export_to_csv {
    my ($filename, @results) = @_;
    return unless @results;
    
    open(my $fh, '>', $filename) or die "Cannot open $filename: $!";
    
    my @columns = keys %{$results[0]};
    print $fh join(',', @columns), "\n";
    
    foreach my $row (@results) {
        my @values = map { 
            my $v = $row->{$_} // '';
            $v =~ s/"/""/g;  # Escape quotes
            qq{"$v"};
        } @columns;
        print $fh join(',', @values), "\n";
    }
    
    close($fh);
}

# Build dynamic WHERE clause from hash
sub build_where_clause {
    my ($where_hash) = @_;
    return ('', []) unless $where_hash && keys %$where_hash;
    
    my @conditions;
    my @values;
    
    foreach my $key (keys %$where_hash) {
        push @conditions, "$key = ?";
        push @values, $where_hash->{$key};
    }
    
    my $where = 'WHERE ' . join(' AND ', @conditions);
    return ($where, \@values);
}

# Safe table exists check
sub table_exists {
    my ($dbh, $table) = @_;
    my @tables = list_tables($dbh);
    return grep { $_ eq $table } @tables;
}

# Get table create statement
sub get_create_table {
    my ($dbh, $table) = @_;
    my $sth = $dbh->prepare("SHOW CREATE TABLE $table");
    $sth->execute();
    my $row = $sth->fetchrow_hashref();
    return $row->{'Create Table'};
}

# Execute raw SQL (for complex queries)
sub execute_sql {
    my ($dbh, $sql, @bind_values) = @_;
    my $sth = $dbh->prepare($sql);
    $sth->execute(@bind_values);
    
    # If it's a SELECT, return results
    if ($sql =~ /^\s*SELECT/i) {
        my @results;
        while (my $row = $sth->fetchrow_hashref()) {
            push @results, $row;
        }
        return @results;
    }
    
    # Otherwise return affected rows
    return $sth->rows();
}

# Return true for require
1;

__END__

=head1 NAME

MySQLUtils.pl - MySQL Database Utilities

=head1 SYNOPSIS

    require './MySQLUtils.pl';
    
    # Connect
    my $dbh = db_connect('localhost', 'mydb', 'user', 'pass');
    
    # Explore database
    my @tables = list_tables($dbh);
    my @columns = get_column_names($dbh, 'users');
    print_table_structure($dbh, 'users');
    
    # Query data
    my @results = select_all($dbh, 'users', 10);
    my @found = select_where($dbh, 'users', {status => 'active'});
    
    # Insert data
    my $id = insert_row($dbh, 'users', {
        name => 'John',
        email => 'john@example.com'
    });
    
    # Update data
    update_by_id($dbh, 'users', $id, {status => 'inactive'});
    
    # Delete data
    delete_by_id($dbh, 'users', $id);
    
    # Disconnect
    db_disconnect($dbh);

=head1 DESCRIPTION

Comprehensive MySQL database utilities for Perl with table discovery,
CRUD operations, and transaction support.

=head1 REQUIREMENTS

Requires DBI and DBD::mysql modules:
    cpan install DBI DBD::mysql

=cut

