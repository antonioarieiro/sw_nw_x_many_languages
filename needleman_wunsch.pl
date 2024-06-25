# needleman_wunsch.pl
use strict;
use warnings;
use Time::HiRes qw(time);

sub max {
    my ($a, $b, $c) = @_;
    return ($a >= $b && $a >= $c) ? $a : ($b >= $a && $b >= $c) ? $b : $c;
}

sub needleman_wunsch {
    my ($seq1, $seq2, $match_score, $gap_cost, $mismatch_cost) = @_;
    my $n = length($seq1);
    my $m = length($seq2);
    my @score;

    for my $i (0 .. $n) {
        $score[$i][0] = $gap_cost * $i;
    }
    for my $j (0 .. $m) {
        $score[0][$j] = $gap_cost * $j;
    }

    for my $i (1 .. $n) {
        for my $j (1 .. $m) {
            my $match = $score[$i - 1][$j - 1] + (substr($seq1, $i - 1, 1) eq substr($seq2, $j - 1, 1) ? $match_score : $mismatch_cost);
            my $delete = $score[$i - 1][$j] + $gap_cost;
            my $insert = $score[$i][$j - 1] + $gap_cost;
            $score[$i][$j] = max($match, $delete, $insert);
        }
    }

    return $score[$n][$m];
}

if (@ARGV < 2) {
    die "Usage: perl needleman_wunsch.pl sequence1 sequence2\n";
}
my ($seq1, $seq2) = @ARGV;
my $start = time();
my $score = needleman_wunsch($seq1, $seq2, 1, -1, -1);
my $time_spent = time() - $start;
print "$time_spent $score\n";
