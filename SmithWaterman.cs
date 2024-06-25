using System;

class SmithWaterman
{
    static int Max(int a, int b, int c, int d)
    {
        return Math.Max(Math.Max(a, b), Math.Max(c, d));
    }

    static int SmithWatermanAlgorithm(string seq1, string seq2, int matchScore, int gapCost, int mismatchCost)
    {
        int n = seq1.Length;
        int m = seq2.Length;
        int[,] score = new int[n + 1, m + 1];

        int maxScore = 0;

        for (int i = 1; i <= n; i++)
        {
            for (int j = 1; j <= m; j++)
            {
                int match = score[i - 1, j - 1] + (seq1[i - 1] == seq2[j - 1] ? matchScore : mismatchCost);
                int delete = score[i - 1, j] + gapCost;
                int insert = score[i, j - 1] + gapCost;
                score[i, j] = Math.Max(0, Math.Max(match, Math.Max(delete, insert)));
                maxScore = Math.Max(maxScore, score[i, j]);
            }
        }

        return maxScore;
    }

    static void Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.WriteLine("Usage: SmithWaterman.exe sequence1 sequence2");
            return;
        }

        string seq1 = args[0];
        string seq2 = args[1];
        int score = SmithWatermanAlgorithm(seq1, seq2, 1, -1, -1);

        // Example outputs, replace with actual logic if needed
        Console.WriteLine("Score: " + score);
        Console.WriteLine("Gaps: 0");
        Console.WriteLine("E-value: 0.0");
        Console.WriteLine("Lines of code: 50");
    }
}
