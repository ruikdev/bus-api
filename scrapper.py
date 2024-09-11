import requests
from bs4 import BeautifulSoup

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
            print("Aucune table trouvée dans le HTML.")
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
        print(f"Erreur lors de la requête : {e}")
        return None, None
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")
        return None, None

stop_id = "3377837159481522"
resultats, perturbation = scrape_t2c_horaires(stop_id)

if resultats:
    print("Prochains départs :")
    print("-" * 50)
    for dep in resultats:
        print(f"Ligne {dep['ligne']:3} | {dep['destination']:20} | Départ : {dep['depart']:10} | {dep['info']}")
    print("-" * 50)

    if perturbation:
        print("\n⚠️ ATTENTION :")
        print(perturbation)
        print("Pour plus d'infos, consultez https://www.t2c.fr/ rubrique InfosTrafic")
else:
    print("Impossible de récupérer les informations.")
