from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/kern-flow.json")
def kern_flow():
    url = "https://www.dreamflows.com/flows.php?zone=canv&page=real&form=norm&mark=All"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    targets = {
        "above_fairview": "Kern - Above Fairview Dam",
        "below_fairview": "Kern - Below Fairview Dam",
        "below_lake_isabella": "Kern - Below Lake Isabella"
    }

    flows = {}
    rows = soup.find_all("tr")
    for row in rows:
        cols = row.get_text(separator="|").split("|")
        if len(cols) < 2:
            continue
        for key, label in targets.items():
            if label.lower() in cols[0].lower():
                try:
                    flows[key] = int(cols[1].replace(",", "").strip())
                except:
                    flows[key] = None

    return jsonify(flows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
