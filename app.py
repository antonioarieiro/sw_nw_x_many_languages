from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import subprocess

app = Flask(__name__)
CORS(app)  # Adiciona suporte a CORS para todas as rotas

def run_script(script, args):
    start = time.time()
    try:
        result = subprocess.run([script] + args, capture_output=True, text=True, check=True)
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

    # C
    c_time, c_output = run_script('./needleman_wunsch_c', [seq1, seq2])
    try:
        c_score = int(c_output.split()[1])
    except (ValueError, IndexError):
        c_score = "N/A"
    results['C'] = {
        'Needleman-Wunsch': {'time': c_time, 'score': c_score, 'output': c_output}
    }

    # C++
    cpp_time, cpp_output = run_script('./needleman_wunsch_cpp', [seq1, seq2])
    try:
        cpp_score = int(cpp_output.split()[1])
    except (ValueError, IndexError):
        cpp_score = "N/A"
    results['C++'] = {
        'Needleman-Wunsch': {'time': cpp_time, 'score': cpp_score, 'output': cpp_output}
    }

    # C#
    cs_time, cs_output = run_script('mono', ['NeedlemanWunsch.exe', seq1, seq2])
    try:
        cs_score = int(cs_output.split()[1])
    except (ValueError, IndexError):
        cs_score = "N/A"
    results['C#'] = {
        'Needleman-Wunsch': {'time': cs_time, 'score': cs_score, 'output': cs_output}
    }

    # Java
    java_time, java_output = run_script('java', ['NeedlemanWunsch', seq1, seq2])
    try:
        java_score = int(java_output.split()[1])
    except (ValueError, IndexError):
        java_score = "N/A"
    results['Java'] = {
        'Needleman-Wunsch': {'time': java_time, 'score': java_score, 'output': java_output}
    }

    # Perl
    perl_time, perl_output = run_script('perl', ['needleman_wunsch.pl', seq1, seq2])
    try:
        perl_score = int(perl_output.split()[1])
    except (ValueError, IndexError):
        perl_score = "N/A"
    results['Perl'] = {
        'Needleman-Wunsch': {'time': perl_time, 'score': perl_score, 'output': perl_output}
    }

    # Determine the fastest result
    fastest_language = min(results, key=lambda k: results[k]['Needleman-Wunsch']['time'])
    fastest_result = results[fastest_language]['Needleman-Wunsch']

    return jsonify({
        'fastest_language': fastest_language,
        'time': fastest_result['time'],
        'score': fastest_result['score'],
        'details': results
    })

if __name__ == '__main__':
    app.run(debug=True)
