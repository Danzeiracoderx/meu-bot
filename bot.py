import os
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import urllib.parse

TOKEN = os.getenv("TOKEN")
WEBAPP_BASE = "https://buscasbasic.infinityfree.me/index2.html"  # Seu WebApp
API_PHP = "https://buscasbasic.infinityfree.me/api.php?lista="          # Sua API PHP

async def cpf_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Use: /cpf 12345678900")
        return

    cpf = context.args[0]

    try:
        r = requests.get(API_PHP, params={"lista": cpf}, timeout=10)
        dados_formatados = r.text.strip()
    except Exception as e:
        await update.message.reply_text("Erro ao buscar dados.")
        return

    dados_url = urllib.parse.quote(dados_formatados)
    webapp_url = f"{WEBAPP_BASE}?dados={dados_url}"

    keyboard = [[InlineKeyboardButton("🔍 Ver Resultado", web_app=WebAppInfo(url=webapp_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Clique abaixo para ver os dados:", reply_markup=reply_markup)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("cpf", cpf_command))
    app.run_polling()
