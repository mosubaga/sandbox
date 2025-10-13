#!/usr/bin/perl

use strict;
use warnings;

# Check if string contains substring
sub contains {
    my ($str, $substr) = @_;
    return index($str, $substr) != -1;
}

# Check if string starts with prefix
sub starts_with {
    my ($str, $prefix) = @_;
    return substr($str, 0, length($prefix)) eq $prefix;
}

# Check if string ends with suffix
sub ends_with {
    my ($str, $suffix) = @_;
    my $len = length($suffix);
    return substr($str, -$len) eq $suffix;
}

# Concatenate multiple strings
sub concat {
    return join('', @_);
}

# Join strings with delimiter
sub join_strings {
    my ($delimiter, @strings) = @_;
    return join($delimiter, @strings);
}

# Split string by delimiter
sub split_string {
    my ($str, $delimiter, $limit) = @_;
    if (defined $limit) {
        return split(quotemeta($delimiter), $str, $limit);
    }
    return split(quotemeta($delimiter), $str);
}

# Trim whitespace from both ends
sub trim {
    my ($str) = @_;
    $str =~ s/^\s+|\s+$//g;
    return $str;
}

# Trim whitespace from left
sub ltrim {
    my ($str) = @_;
    $str =~ s/^\s+//;
    return $str;
}

# Trim whitespace from right
sub rtrim {
    my ($str) = @_;
    $str =~ s/\s+$//;
    return $str;
}

# Convert to uppercase
sub upper {
    my ($str) = @_;
    return uc($str);
}

# Convert to lowercase
sub lower {
    my ($str) = @_;
    return lc($str);
}

# Capitalize first letter
sub capitalize {
    my ($str) = @_;
    return ucfirst(lc($str));
}

# Title case (capitalize each word)
sub title_case {
    my ($str) = @_;
    return join(' ', map { ucfirst(lc($_)) } split(/\s+/, $str));
}

# Reverse string
sub reverse_string {
    my ($str) = @_;
    return scalar reverse($str);
}

# Get substring
sub substring {
    my ($str, $start, $length) = @_;
    if (defined $length) {
        return substr($str, $start, $length);
    }
    return substr($str, $start);
}

# Get substring before first occurrence
sub substr_before {
    my ($str, $delimiter) = @_;
    my $pos = index($str, $delimiter);
    return $pos == -1 ? $str : substr($str, 0, $pos);
}

# Get substring after first occurrence
sub substr_after {
    my ($str, $delimiter) = @_;
    my $pos = index($str, $delimiter);
    return $pos == -1 ? '' : substr($str, $pos + length($delimiter));
}

# Replace all occurrences
sub replace {
    my ($str, $search, $replace) = @_;
    $search = quotemeta($search);
    $str =~ s/$search/$replace/g;
    return $str;
}

# Replace first occurrence
sub replace_first {
    my ($str, $search, $replace) = @_;
    $search = quotemeta($search);
    $str =~ s/$search/$replace/;
    return $str;
}

# Replace last occurrence
sub replace_last {
    my ($str, $search, $replace) = @_;
    my $pos = rindex($str, $search);
    if ($pos != -1) {
        substr($str, $pos, length($search)) = $replace;
    }
    return $str;
}

# Count occurrences of substring
sub count_occurrences {
    my ($str, $substr) = @_;
    my $count = 0;
    my $pos = 0;
    while (($pos = index($str, $substr, $pos)) != -1) {
        $count++;
        $pos += length($substr);
    }
    return $count;
}

# Check if string is empty
sub is_empty {
    my ($str) = @_;
    return !defined($str) || $str eq '';
}

# Check if string is blank (empty or whitespace)
sub is_blank {
    my ($str) = @_;
    return !defined($str) || $str =~ /^\s*$/;
}

# Pad left with character
sub pad_left {
    my ($str, $length, $char) = @_;
    $char //= ' ';
    my $padding = $length - length($str);
    return $padding > 0 ? ($char x $padding) . $str : $str;
}

# Pad right with character
sub pad_right {
    my ($str, $length, $char) = @_;
    $char //= ' ';
    my $padding = $length - length($str);
    return $padding > 0 ? $str . ($char x $padding) : $str;
}

# Center string with padding
sub center {
    my ($str, $length, $char) = @_;
    $char //= ' ';
    my $padding = $length - length($str);
    return $str if $padding <= 0;
    my $left = int($padding / 2);
    my $right = $padding - $left;
    return ($char x $left) . $str . ($char x $right);
}

# Repeat string n times
sub repeat {
    my ($str, $times) = @_;
    return $str x $times;
}

# Remove all occurrences
sub remove {
    my ($str, $substr) = @_;
    return replace($str, $substr, '');
}

# Remove first occurrence
sub remove_first {
    my ($str, $substr) = @_;
    return replace_first($str, $substr, '');
}

# Remove last occurrence
sub remove_last {
    my ($str, $substr) = @_;
    return replace_last($str, $substr, '');
}

# Truncate string to length
sub truncate {
    my ($str, $length, $suffix) = @_;
    $suffix //= '...';
    return length($str) <= $length ? $str : substr($str, 0, $length - length($suffix)) . $suffix;
}

# Find index of substring
sub index_of {
    my ($str, $substr, $from) = @_;
    $from //= 0;
    return index($str, $substr, $from);
}

# Find last index of substring
sub last_index_of {
    my ($str, $substr) = @_;
    return rindex($str, $substr);
}

# Get character at position
sub char_at {
    my ($str, $pos) = @_;
    return substr($str, $pos, 1);
}

# Check if string is numeric
sub is_numeric {
    my ($str) = @_;
    return $str =~ /^-?\d+\.?\d*$/;
}

# Check if string contains only letters
sub is_alpha {
    my ($str) = @_;
    return $str =~ /^[a-zA-Z]+$/;
}

# Check if string contains only letters and numbers
sub is_alphanumeric {
    my ($str) = @_;
    return $str =~ /^[a-zA-Z0-9]+$/;
}

# Convert string to array of characters
sub to_array {
    my ($str) = @_;
    return split(//, $str);
}

# Convert array to string
sub from_array {
    my (@chars) = @_;
    return join('', @chars);
}

# Wrap text to specified width
sub wrap {
    my ($str, $width) = @_;
    $width //= 80;
    my @words = split(/\s+/, $str);
    my @lines;
    my $line = '';
    
    foreach my $word (@words) {
        if (length($line) + length($word) + 1 <= $width) {
            $line .= ($line ? ' ' : '') . $word;
        } else {
            push @lines, $line if $line;
            $line = $word;
        }
    }
    push @lines, $line if $line;
    
    return join("\n", @lines);
}

# Remove line breaks
sub unwrap {
    my ($str) = @_;
    $str =~ s/\n/ /g;
    return $str;
}

# Convert to camelCase
sub camel_case {
    my ($str) = @_;
    $str = lc($str);
    $str =~ s/[_\-\s]+(.)/uc($1)/ge;
    return $str;
}

# Convert to snake_case
sub snake_case {
    my ($str) = @_;
    $str =~ s/([A-Z])/_\L$1/g;
    $str =~ s/[\-\s]+/_/g;
    $str =~ s/^_+|_+$//g;
    return lc($str);
}

# Convert to kebab-case
sub kebab_case {
    my ($str) = @_;
    $str =~ s/([A-Z])/-\L$1/g;
    $str =~ s/[_\s]+/-/g;
    $str =~ s/^-+|-+$//g;
    return lc($str);
}

# Strip HTML tags
sub strip_html {
    my ($str) = @_;
    $str =~ s/<[^>]*>//g;
    return $str;
}

# Calculate Levenshtein distance
sub levenshtein_distance {
    my ($s1, $s2) = @_;
    my @s1 = split //, $s1;
    my @s2 = split //, $s2;
    my @d;
    
    $d[$_][0] = $_ for (0 .. @s1);
    $d[0][$_] = $_ for (0 .. @s2);
    
    for my $i (1 .. @s1) {
        for my $j (1 .. @s2) {
            $d[$i][$j] = $s1[$i-1] eq $s2[$j-1] ? $d[$i-1][$j-1] :
                1 + ($d[$i-1][$j] < $d[$i][$j-1] 
                    ? ($d[$i-1][$j] < $d[$i-1][$j-1] ? $d[$i-1][$j] : $d[$i-1][$j-1])
                    : ($d[$i][$j-1] < $d[$i-1][$j-1] ? $d[$i][$j-1] : $d[$i-1][$j-1]));
        }
    }
    
    return $d[@s1][@s2];
}

# Generate random string
sub random_string {
    my ($length, $chars) = @_;
    $length //= 10;
    $chars //= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    my @chars = split //, $chars;
    my $result = '';
    $result .= $chars[rand @chars] for (1..$length);
    return $result;
}

# Return true to indicate successful loading
1;

__END__

=head1 NAME

StringUtils.pl - String utility subroutines

=head1 USAGE

Method 1 - Using 'require':
    require './StringUtils.pl';
    my $result = trim("  hello  ");

Method 2 - Using 'do':
    do './StringUtils.pl';
    my $result = upper("hello");

Method 3 - Using library path:
    require 'StringUtils.pl';  # if in @INC path
    my $result = contains("hello world", "world");

=head1 EXAMPLES

See the example_usage.pl file for complete examples.

=cut