# algorithms.py
def needleman_wunsch(seq1, seq2):
    match_award = 1
    mismatch_penalty = -1
    gap_penalty = -1

    n = len(seq1)
    m = len(seq2)
    
    score = [[0 for j in range(m+1)] for i in range(n+1)]

    for i in range(1, n+1):
        score[i][0] = gap_penalty * i
    for j in range(1, m+1):
        score[0][j] = gap_penalty * j

    for i in range(1, n+1):
        for j in range(1, m+1):
            match = score[i-1][j-1] + (match_award if seq1[i-1] == seq2[j-1] else mismatch_penalty)
            delete = score[i-1][j] + gap_penalty
            insert = score[i][j-1] + gap_penalty
            score[i][j] = max(match, delete, insert)

    align1, align2 = '', ''
    i, j = n, m

    while i > 0 and j > 0:
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]

        if score_current == score_diagonal + (match_award if seq1[i-1] == seq2[j-1] else mismatch_penalty):
            align1 += seq1[i-1]
            align2 += seq2[j-1]
            i -= 1
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1 += seq1[i-1]
            align2 += '-'
            i -= 1
        elif score_current == score_up + gap_penalty:
            align1 += '-'
            align2 += seq2[j-1]
            j -= 1

    while i > 0:
        align1 += seq1[i-1]
        align2 += '-'
        i -= 1

    while j > 0:
        align1 += '-'
        align2 += seq2[j-1]
        j -= 1

    align1 = align1[::-1]
    align2 = align2[::-1]

    gaps = align1.count('-') + align2.count('-')

    return score[n][m], gaps
def smith_waterman(seq1, seq2):
    match_award = 2
    mismatch_penalty = -1
    gap_penalty = -1

    n = len(seq1)
    m = len(seq2)

    score = [[0 for j in range(m+1)] for i in range(n+1)]
    max_score = 0

    for i in range(1, n+1):
        for j in range(1, m+1):
            match = score[i-1][j-1] + (match_award if seq1[i-1] == seq2[j-1] else mismatch_penalty)
            delete = score[i-1][j] + gap_penalty
            insert = score[i][j-1] + gap_penalty
            score[i][j] = max(0, match, delete, insert)
            max_score = max(max_score, score[i][j])

    align1, align2 = '', ''
    i, j = n, m

    while i > 0 and j > 0 and score[i][j] != 0:
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]

        if score_current == score_diagonal + (match_award if seq1[i-1] == seq2[j-1] else mismatch_penalty):
            align1 += seq1[i-1]
            align2 += seq2[j-1]
            i -= 1
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1 += seq1[i-1]
            align2 += '-'
            i -= 1
        elif score_current == score_up + gap_penalty:
            align1 += '-'
            align2 += seq2[j-1]
            j -= 1

    align1 = align1[::-1]
    align2 = align2[::-1]

    gaps = align1.count('-') + align2.count('-')

    return max_score, gaps