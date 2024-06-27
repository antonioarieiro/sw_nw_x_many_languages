from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import subprocess

app = Flask(__name__)
CORS(app)

def run_script(script, args):
    start = time.time()
    try:
        result = subprocess.run([script] + args, capture_output=True, text=True, check=True, shell=True)
        end = time.time()
        output = result.stdout.strip()
        time_spent = end - start
        return time_spent, output
    except subprocess.CalledProcessError as e:
        end = time.time()
        return end - start, f"Error: {e.output.strip()}"
    except FileNotFoundError:
        end = time.time()
        return end - start, "Error: File not found"

def parse_output(output):

    try:
        lines = output.split('\n')
        score = int(lines[0].split()[1])
        gaps = int(lines[1].split()[1])
        evalue = float(lines[2].split()[1])
        code_lines = int(lines[3].split()[1])
        return score, gaps, evalue, code_lines
    except (IndexError, ValueError):
        return "N/A", "N/A", "N/A", "N/A"

@app.route('/align', methods=['POST'])
def align():
    data = request.json
    seq1 = data['sequence1']
    seq2 = data['sequence2']

    results = {}

    scripts = {
        'Needleman-Wunsch': {
            'C': './needleman_wunsch_c',
            'C++': './needleman_wunsch_cpp',
            'C#': 'NeedlemanWunsch.exe',
            'Java': 'NeedlemanWunsch',
            'Perl': 'needleman_wunsch.pl'
        },
        'Smith-Waterman': {
            'C': './smith_waterman_c',
            'C++': './smith_waterman_cpp',
            'C#': 'SmithWaterman.exe',
            'Java': 'SmithWaterman',
            'Perl': 'smith_waterman.pl'
        }
    }

    for algo in scripts:
        for lang, script in scripts[algo].items():
            if lang == 'C#':
                time_spent, output = run_script('mono', [script, seq1, seq2])
            else:
                time_spent, output = run_script(script, [seq1, seq2])
            score, gaps, evalue, code_lines = parse_output(output)
            if lang not in results:
                results[lang] = {}
            results[lang][algo] = {
                'time': time_spent,
                'score': score,
                'gaps': gaps,
                'evalue': evalue,
                'code_lines': code_lines,
                'output': output
            }

    fastest_results = {}
    for algo in scripts:
        fastest_language = min(results, key=lambda k: results[k][algo]['time'])
        fastest_results[algo] = {
            'fastest_language': fastest_language,
            'time': results[fastest_language][algo]['time'],
            'score': results[fastest_language][algo]['score'],
            'gaps': results[fastest_language][algo]['gaps'],
            'evalue': results[fastest_language][algo]['evalue'],
            'code_lines': results[fastest_language][algo]['code_lines']
        }

    return jsonify({
        'fastest_results': fastest_results,
        'details': results
    })

if __name__ == '__main__':
    app.run(debug=True)
