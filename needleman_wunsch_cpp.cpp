#include <iostream>
#include <vector>
#include <string>
#include <ctime>
#include <algorithm>

int max(int a, int b, int c) {
    return std::max({a, b, c});
}

int needleman_wunsch(const std::string &seq1, const std::string &seq2, int match_score, int gap_cost, int mismatch_cost) {
    int n = seq1.length();
    int m = seq2.length();
    std::vector<std::vector<int>> score(n + 1, std::vector<int>(m + 1, 0));

    for (int i = 0; i <= n; ++i) {
        score[i][0] = gap_cost * i;
    }
    for (int j = 0; j <= m; ++j) {
        score[0][j] = gap_cost * j;
    }

    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            int match = score[i - 1][j - 1] + (seq1[i - 1] == seq2[j - 1] ? match_score : mismatch_cost);
            int del = score[i - 1][j] + gap_cost;
            int ins = score[i][j - 1] + gap_cost;
            score[i][j] = std::max({match, del, ins});
        }
    }

    return score[n][m];
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " sequence1 sequence2" << std::endl;
        return 1;
    }
    std::string seq1 = argv[1];
    std::string seq2 = argv[2];
    clock_t start = clock();
    int score = needleman_wunsch(seq1, seq2, 1, -1, -1);
    clock_t end = clock();
    double time_spent = static_cast<double>(end - start) / CLOCKS_PER_SEC;
    std::cout << time_spent << " " << score << std::endl;
    return 0;
}
