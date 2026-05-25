#!/usr/bin/perl
# silence-minor-changes.pl
# Post-process latexdiff output to silently accept selected (old, new) pairs.
#
# Usage:
#   perl silence-minor-changes.pl <silenced-changes.txt> <input.tex> > <output.tex>
#
# Format of silenced-changes.txt:
#   # comments...
#   protect-block: <COMMAND>     (optional, can repeat — never silence inside
#                                 \<COMMAND>{...}; defaults: ABSTRACT, TITLE,
#                                 abstract, title)
#   OLD<TAB>NEW                  (one pair per line)
#
# The script searches for latexdiff's signature pattern:
#   \DIFdelbegin \DIFdel{<OLD>}\DIFdelend \DIFaddbegin \DIFadd{<NEW>}\DIFaddend
# and replaces it with just <NEW>, silently accepting the change.
#
# Protected blocks: any text inside \<COMMAND>{...} (with brace matching) is
# left untouched. This keeps changes inside the abstract / title visible even
# when the same numerical pair is silenced elsewhere.
#
# IMPORTANT: stderr is for diagnostics. NEVER merge stderr into the output
# (no `2>&1`); keep stdout clean for the rewritten .tex content.

use strict;
use warnings;

if (@ARGV != 2) {
    die "Usage: $0 <silenced-changes.txt> <input.tex> > <output.tex>\n";
}

my ($pairs_file, $input_file) = @ARGV;

my @protect_blocks = ();
my @pairs;

# Read silenced pairs + directives
open(my $pf, '<', $pairs_file) or die "Cannot open $pairs_file: $!\n";
while (my $line = <$pf>) {
    chomp $line;
    next if $line =~ /^\s*#/ || $line =~ /^\s*$/;

    if ($line =~ /^protect-block:\s*(\S+)\s*$/) {
        push @protect_blocks, $1;
        next;
    }

    my ($old, $new) = split(/\t/, $line, 2);
    next unless defined $new;
    $old =~ s/^\s+|\s+$//g;
    $new =~ s/^\s+|\s+$//g;
    push @pairs, [$old, $new];
}
close($pf);

# Default protected blocks if none specified — covers both INFORMS-style
# uppercase commands and standard LaTeX lowercase commands.
if (@protect_blocks == 0) {
    @protect_blocks = qw(ABSTRACT TITLE abstract title);
}

# Read input file as a single string
open(my $tf, '<', $input_file) or die "Cannot open $input_file: $!\n";
local $/ = undef;
my $content = <$tf>;
close($tf);

# Find protected spans: each \<COMMAND>{...} with brace matching.
sub find_protected_spans {
    my ($text, @cmds) = @_;
    my @spans;
    foreach my $cmd (@cmds) {
        my $cmd_q = quotemeta($cmd);
        while ($text =~ /\\$cmd_q\s*\{/g) {
            my $start = $-[0];
            my $i = pos($text);
            my $depth = 1;
            while ($i < length($text) && $depth > 0) {
                my $c = substr($text, $i, 1);
                if ($c eq '\\') {
                    $i += 2;
                    next;
                }
                $depth++ if $c eq '{';
                $depth-- if $c eq '}';
                $i++;
            }
            push @spans, [$start, $i];
        }
    }
    @spans = sort { $a->[0] <=> $b->[0] } @spans;
    return @spans;
}

my @protected = find_protected_spans($content, @protect_blocks);

# Split content into segments: alternating (unprotected, protected) pieces
my @segments;
my $cursor = 0;
foreach my $span (@protected) {
    my ($s, $e) = @$span;
    push @segments, [substr($content, $cursor, $s - $cursor), 0];
    push @segments, [substr($content, $s, $e - $s),               1];
    $cursor = $e;
}
push @segments, [substr($content, $cursor), 0];

# Apply silencing only to unprotected segments
my $total_silenced = 0;
foreach my $seg (@segments) {
    my ($txt, $is_protected) = @$seg;
    next if $is_protected;

    foreach my $pair (@pairs) {
        my ($old, $new) = @$pair;
        my $old_q = quotemeta($old);
        my $new_q = quotemeta($new);

        my $pattern = qr/
            \\DIFdelbegin \s* \\DIFdel\{ \s* $old_q \s* \}\\DIFdelend
            \s+
            \\DIFaddbegin \s* \\DIFadd\{ \s* $new_q \s* \}\\DIFaddend
        /sx;

        my $count = () = ($txt =~ /$pattern/g);
        if ($count > 0) {
            $txt =~ s/$pattern/$new/g;
            $total_silenced += $count;
        }
    }
    $seg->[0] = $txt;
}

# Reassemble
my $output = join('', map { $_->[0] } @segments);

# Diagnostics to stderr ONLY
warn sprintf("Protected blocks: %s\n", join(', ', map { "\\$_" } @protect_blocks));
warn sprintf("Protected spans found: %d\n", scalar @protected);
warn sprintf("Total silenced (outside protected blocks): %d\n", $total_silenced);

print $output;
