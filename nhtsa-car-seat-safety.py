import json, requests
from os.path import exists

baseUrl = "https://api.nhtsa.gov/childSeats?offset=0&max=100&sort=make&order=asc&data=modes&dataSet=ratings"
jsonFile = "car-seat-results.json"

def load_api(url):
    results = []
    while url:
        try:
            response = requests.get(url)
        except Exception as e:
            raise e
        obj = response.json()
        url = obj["meta"]["pagination"]["nextUrl"]
        results.extend(obj["results"])
    return results

def load_json(file):
    with open(file, "r") as f:
        results = json.load(f)
    return results

def save_json(file, results):
    with open(file, "w") as f:
        json.dump(results, f, indent=2)

def load_from_cache(url, file):
    if not exists(file):
        results = load_api(url)
        save_json(file, results)
    else:
        results = load_json(file)
    return results

results = load_from_cache(baseUrl, jsonFile)
