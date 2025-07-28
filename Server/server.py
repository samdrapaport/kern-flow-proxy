from flask import Flask, jsonify
import requests
import csv
import io

app = Flask(__name__)

@app.route("/kern-flow.json")
def kern_flow():
    url = "https://www.dreamflows.com/realtime.csv.php"
    response = requests.get(url)
    response.raise_for_status()

    csv_file = io.StringIO(response.text)
    reader = csv.DictReader(csv_file)

    kern_data = {
        "above_fairview": None,
        "below_fairview": None,
        "below_lake_isabella": None
    }

    for row in reader:
        site = row["Site Name"].lower()
        flow = row["Flow"]

        if "kern" in site:
            if "above fairview" in site:
                kern_data["above_fairview"] = flow
            elif "below fairview" in site:
                kern_data["below_fairview"] = flow
            elif "below lake isabella" in site:
                kern_data["below_lake_isabella"] = flow

    return jsonify(kern_data)