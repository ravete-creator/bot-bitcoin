import requests
import time

TOKEN = "8970298887:AAG6tLyBCnTNMLJkqSZIbd45NeLqJUDJk8I"
CHAT_ID = "929309450"

def pegar_preco_bitcoin():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"

    resposta = requests.get(url)
    dados = resposta.json()

    preco = dados["data"]["amount"]

    return preco

def enviar_mensagem(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    dados = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }

    requests.post(url, data=dados)

while True:
    preco = pegar_preco_bitcoin()

    mensagem = f"Bitcoin agora: ${preco}"

    enviar_mensagem(mensagem)

    print(mensagem)

    time.sleep(60)