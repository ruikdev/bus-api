from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def scrape_t2c_horaires(stop_id):
    url = f"http://qr.t2c.fr/qrcode?_stop_id={stop_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table')
        if not table:
            return None, None

        departures = []
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) == 4:
                departure = {
                    'ligne': cols[0].text.strip(),
                    'destination': cols[1].text.strip() or "Non spécifiée",
                    'depart': cols[2].text.strip() or "Non spécifié",
                    'info': cols[3].text.strip()
                }
                departures.append(departure)

        warning = soup.find('h3', string=lambda t: t and "Arrêt perturbé ou reporté" in t)
        perturbation = warning.text.strip() if warning else None

        return departures, perturbation

    except requests.RequestException as e:
        return None, f"Erreur lors de la requête : {e}"
    except Exception as e:
        return None, f"Une erreur inattendue s'est produite : {e}"


@app.route('/<stop_id>')
def get_horaires(stop_id):
    resultats, perturbation = scrape_t2c_horaires(stop_id)

    if resultats is None:
        return jsonify({"error": perturbation}), 400

    return jsonify({
        "departures": resultats,
        "perturbation": perturbation
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
