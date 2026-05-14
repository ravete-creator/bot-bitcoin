import requests
import time
import json
import threading

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8970298887:AAEqZR4EHsv3NW-lWymm_TBWJ8gvWde_tao"

ARQUIVO_GRUPOS = "grupos.json"


def carregar_grupos():
    try:
        with open(ARQUIVO_GRUPOS, "r") as arquivo:
            return json.load(arquivo)
    except:
        return []


def salvar_grupos(grupos):
    with open(ARQUIVO_GRUPOS, "w") as arquivo:
        json.dump(grupos, arquivo)


async def detectar_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    grupos = carregar_grupos()

    if chat_id not in grupos:
        grupos.append(chat_id)
        salvar_grupos(grupos)

        print(f"Novo grupo salvo: {chat_id}")


def pegar_preco_bitcoin():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"

    resposta = requests.get(url)
    dados = resposta.json()

    return dados["data"]["amount"]


def enviar_mensagens():
    while True:
        try:
            preco = pegar_preco_bitcoin()

            mensagem = f"Bitcoin agora: ${preco}"

            grupos = carregar_grupos()

            for chat_id in grupos:
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

                dados = {
                    "chat_id": chat_id,
                    "text": mensagem
                }

                requests.post(url, data=dados)

                print(f"Mensagem enviada para {chat_id}")

        except Exception as erro:
            print("Erro:", erro)

        time.sleep(60)


def iniciar_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.ALL, detectar_grupo)
    )

    print("Bot iniciado...")

    app.run_polling()


thread_envio = threading.Thread(target=enviar_mensagens)

thread_envio.start()

iniciar_bot()