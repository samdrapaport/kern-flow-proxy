from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)  # <-- This line must come before any route definitions

@app.route("/kern-flow.json")
def kern_flow():
    url = "https://www.dreamflows.com/flows.php?zone=canv&page=real&form=norm&mark=All"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    target_sites = {
        "above_fairview": "Kern - Above Fairview Dam",
        "below_fairview": "Kern - Below Fairview Dam",
        "below_lake_isabella": "Kern - Below Lake Isabella"
    }

    flows = {}
    table = soup.find("table", {"border": "1"})
    if not table:
        return jsonify({"error": "Could not find flow table."})

    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue
        site_name = cols[0].get_text(strip=True)
        for key, label in target_sites.items():
            if label.lower() in site_name.lower():
                try:
                    cfs = int(cols[1].get_text(strip=True).replace(",", ""))
                    flows[key] = cfs
                except:
                    flows[key] = None

    return jsonify(flows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
