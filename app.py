from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import subprocess
from algorithms import needleman_wunsch, smith_waterman
import requests

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

@app.route('/align', methods=['POST'])
def align():
    data = request.json
    seq1 = data['sequence1']
    seq2 = data['sequence2']

    results = {}

    code_lines = {
        'Needleman-Wunsch': {
            'C': 59,
            'C++': 48,
            'C#': 47,
            'Java': 52,
            'Perl': 43
        },
        'Smith-Waterman': {
            'C': 59,
            'C++': 48,
            'C#': 47,
            'Java': 52,
            'Perl': 43
        }
    }

    algorithms = {
        'Needleman-Wunsch': needleman_wunsch,
        'Smith-Waterman': smith_waterman
    }

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

    for algo_name, algo_func in algorithms.items():
        python_score, python_gaps = algo_func(seq1, seq2)
        for lang, script in scripts[algo_name].items():
            if lang == 'C#':
                time_spent, output = run_script('mono', [script, seq1, seq2])
            else:
                time_spent, output = run_script(script, [seq1, seq2])
            if lang not in results:
                results[lang] = {}
            results[lang][algo_name] = {
                'time': time_spent,
                'score': python_score,
                'gaps': python_gaps,
                'code_lines': code_lines[algo_name][lang],
                'output': output,
                'is_fastest': False
            }

    for algo in scripts:
        fastest_language = min(results, key=lambda k: results[k][algo]['time'])
        results[fastest_language][algo]['is_fastest'] = True

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
