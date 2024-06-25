// NeedlemanWunsch.cs
using System;
using System.Diagnostics;

class NeedlemanWunsch {
    static int Max(int a, int b, int c) {
        return Math.Max(a, Math.Max(b, c));
    }

    static int NeedlemanWunschAlgorithm(string seq1, string seq2, int matchScore, int gapCost, int mismatchCost) {
        int n = seq1.Length;
        int m = seq2.Length;
        int[,] score = new int[n + 1, m + 1];

        for (int i = 0; i <= n; i++) {
            score[i, 0] = gapCost * i;
        }
        for (int j = 0; j <= m; j++) {
            score[0, j] = gapCost * j;
        }

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                int match = score[i - 1, j - 1] + (seq1[i - 1] == seq2[j - 1] ? matchScore : mismatchCost);
                int delete = score[i - 1, j] + gapCost;
                int insert = score[i, j - 1] + gapCost;
                score[i, j] = Max(match, delete, insert);
            }
        }

        return score[n, m];
    }

    static void Main(string[] args) {
        if (args.Length < 2) {
            Console.WriteLine("Usage: NeedlemanWunsch sequence1 sequence2");
            return;
        }
        string seq1 = args[0];
        string seq2 = args[1];
        Stopwatch stopwatch = Stopwatch.StartNew();
        int score = NeedlemanWunschAlgorithm(seq1, seq2, 1, -1, -1);
        stopwatch.Stop();
        double timeSpent = stopwatch.Elapsed.TotalSeconds;
        Console.WriteLine($"{timeSpent} {score}");
    }
}
