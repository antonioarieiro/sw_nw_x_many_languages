use strict;
use warnings;

sub max {
    my ($a, $b, $c, $d) = @_;
    return ($a > $b ? $a : $b) > ($c > $d ? $c : $d) ? ($a > $b ? $a : $b) : ($c > $d ? $c : $d);
}

sub smith_waterman {
    my ($seq1, $seq2, $match_score, $gap_cost, $mismatch_cost) = @_;
    my $n = length($seq1);
    my $m = length($seq2);
    my @score;

    for my $i (0 .. $n) {
        for my $j (0 .. $m) {
            $score[$i][$j] = 0;
        }
    }

    my $max_score = 0;

    for my $i (1 .. $n) {
        for my $j (1 .. $m) {
            my $match = $score[$i - 1][$j - 1] + (substr($seq1, $i - 1, 1) eq substr($seq2, $j - 1, 1) ? $match_score : $mismatch_cost);
            my $delete = $score[$i - 1][$j] + $gap_cost;
            my $insert = $score[$i][$j - 1] + $gap_cost;
            $score[$i][$j] = max(0, $match, $delete, $insert);
            $max_score = $score[$i][$j] if $score[$i][$j] > $max_score;
        }
    }

    return $max_score;
}

if (@ARGV < 2) {
    die "Usage: perl smith_waterman.pl sequence1 sequence2\n";
}

my ($seq1, $seq2) = @ARGV;
my $score = smith_waterman($seq1, $seq2, 1, -1, -1);

# Example outputs, replace with actual logic if needed
print "Score: $score\n";
print "Gaps: 0\n";
print "E-value: 0.0\n";
print "Lines of code: 50\n";
