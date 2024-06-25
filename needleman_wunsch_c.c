// needleman_wunsch.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int max(int a, int b, int c) {
    if (a >= b && a >= c) return a;
    if (b >= a && b >= c) return b;
    return c;
}

int needleman_wunsch(char *seq1, char *seq2, int match_score, int gap_cost, int mismatch_cost) {
    int n = strlen(seq1);
    int m = strlen(seq2);
    int **score = (int **)malloc((n + 1) * sizeof(int *));
    for (int i = 0; i <= n; i++) {
        score[i] = (int *)malloc((m + 1) * sizeof(int));
    }

    for (int i = 0; i <= n; i++) {
        score[i][0] = gap_cost * i;
    }
    for (int j = 0; j <= m; j++) {
        score[0][j] = gap_cost * j;
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            int match = score[i - 1][j - 1] + (seq1[i - 1] == seq2[j - 1] ? match_score : mismatch_cost);
            int delete = score[i - 1][j] + gap_cost;
            int insert = score[i][j - 1] + gap_cost;
            score[i][j] = max(match, delete, insert);
        }
    }

    int result = score[n][m];
    for (int i = 0; i <= n; i++) {
        free(score[i]);
    }
    free(score);

    return result;
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s sequence1 sequence2\n", argv[0]);
        return 1;
    }
    char *seq1 = argv[1];
    char *seq2 = argv[2];
    clock_t start = clock();
    int score = needleman_wunsch(seq1, seq2, 1, -1, -1);
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("%lf %d\n", time_spent, score);
    return 0;
}
