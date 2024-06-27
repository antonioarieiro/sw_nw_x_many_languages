import requests

def search_blast(sequence, program="blastn", database="nt"):
    url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
    params = {
        "CMD": "Put",
        "PROGRAM": program,
        "DATABASE": database,
        "QUERY": sequence,
        "FORMAT_TYPE": "JSON2"
    }

    response = requests.post(url, data=params)
    if response.status_code == 200:
        rid = response.text.split("\n")[0].split("=")[1].strip()
        return rid
    else:
        return None

def get_blast_results(rid):
    url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
    params = {
        "CMD": "Get",
        "RID": rid,
        "FORMAT_TYPE": "JSON2"
    }

    while True:
        response = requests.get(url, params=params)
        if response.status_code == 200 and "Status=WAITING" not in response.text:
            return response.json()
        time.sleep(5)
