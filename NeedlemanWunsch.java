// NeedlemanWunsch.java
import java.util.*;

public class NeedlemanWunsch {
    public static int max(int a, int b, int c) {
        return Math.max(a, Math.max(b, c));
    }

    public static int needlemanWunsch(String seq1, String seq2, int matchScore, int gapCost, int mismatchCost) {
        int n = seq1.length();
        int m = seq2.length();
        int[][] score = new int[n + 1][m + 1];

        for (int i = 0; i <= n; i++) {
            score[i][0] = gapCost * i;
        }
        for (int j = 0; j <= m; j++) {
            score[0][j] = gapCost * j;
        }

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                int match = score[i - 1][j - 1] + (seq1.charAt(i - 1) == seq2.charAt(j - 1) ? matchScore : mismatchCost);
                int delete = score[i - 1][j] + gapCost;
                int insert = score[i][j - 1] + gapCost;
                score[i][j] = max(match, delete, insert);
            }
        }

        return score[n][m];
    }

    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java NeedlemanWunsch sequence1 sequence2");
            return;
        }
        String seq1 = args[0];
        String seq2 = args[1];
        long start = System.nanoTime();
        int score = needlemanWunsch(seq1, seq2, 1, -1, -1);
        long end = System.nanoTime();
        double timeSpent = (end - start) / 1e9;
        System.out.println(timeSpent + " " + score);
    }
}
