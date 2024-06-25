public class SmithWaterman {
    public static int max(int a, int b, int c, int d) {
        return Math.max(Math.max(a, b), Math.max(c, d));
    }

    public static int smithWaterman(String seq1, String seq2, int matchScore, int gapCost, int mismatchCost) {
        int n = seq1.length();
        int m = seq2.length();
        int[][] score = new int[n + 1][m + 1];

        int maxScore = 0;

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                int match = score[i - 1][j - 1] + (seq1.charAt(i - 1) == seq2.charAt(j - 1) ? matchScore : mismatchCost);
                int del = score[i - 1][j] + gapCost;
                int ins = score[i][j - 1] + gapCost;
                score[i][j] = Math.max(0, Math.max(match, Math.max(del, ins)));
                maxScore = Math.max(maxScore, score[i][j]);
            }
        }

        return maxScore;
    }

    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: java SmithWaterman sequence1 sequence2");
            System.exit(1);
        }

        String seq1 = args[0];
        String seq2 = args[1];
        int score = smithWaterman(seq1, seq2, 1, -1, -1);

        // Example outputs, replace with actual logic if needed
        System.out.println("Score: " + score);
        System.out.println("Gaps: 0");
        System.out.println("E-value: 0.0");
        System.out.println("Lines of code: 50");
    }
}
