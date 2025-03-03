from telegram import Update, ReplyKeyboardMarkup, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes
from diccionarioAUtilizar import personas
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TOKEN = "8085222960:AAH6TDXo5-vYTniLrrbbh_VDIKAHG9fdL_w"

pregunta = 0
datos_usuario = {}

preguntas = [
    ("¿Cuál es tu edad?", ["18-22", "23-27", "28-33"]),
    ("¿Cuál es tu sexo?", ["Hombre", "Mujer"]),
    ("¿Qué buscas en una relación?", ["Relación estable", "Nada serio", "Duda"]),
    ("¿Quieres tener hijos?", ["Sí", "No", "Duda"]),
    ("¿Cuál es tu área de interés?", ["Informática", "Comercio", "Deporte", "Mecanizado"])
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"¡Bienvenid@ {user.mention_html()}! Usa el comando <b>/love</b> para empezar a encontrar el amor",
        reply_markup=ForceReply(selective=True),
    )
    logger.info(f"Se ha dado la bienvenida a {user.mention_html()}")

async def love(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /love is issued."""
    global pregunta
    user = update.effective_user

    if pregunta == 0:
        pregunta += 1
        logger.info(f"{user.mention_html()} ha empezado un nuevo cuestionario")
        await update.message.reply_html("¡Empecemos con un cuestionario para saber más sobre ti!\n"
                                        "Puedes parar el cuestionario con /stop, o volver a la pregunta anterior con /back")


def main():
    """Configura y ejecuta el bot."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("love", love))

    app.run_polling()


if __name__ == "__main__":
    main()
