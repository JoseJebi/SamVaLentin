from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes, \
    ConversationHandler
from diccionarioAUtilizar import personas
import logging

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8085222960:AAH6TDXo5-vYTniLrrbbh_VDIKAHG9fdL_w"

PREGUNTA_SEXO, PREGUNTA_EDAD, PREGUNTA_GRADO, PREGUNTA_FIN, PREGUNTA_HIJOS = range(5)


def calcular_afinidad(respuestas_usuario):
    coincidencias = []
    for persona_id, datos in personas.items():
        puntuacion = 0
        if datos['Sexo'] == respuestas_usuario['Sexo']:
            puntuacion += 1
        if abs(datos['Edad'] - respuestas_usuario['Edad']) <= 3:
            puntuacion += 1
        if datos['Grado'] == respuestas_usuario['Grado']:
            puntuacion += 1
        if datos['Fin'] == respuestas_usuario['Fin']:
            puntuacion += 1
        if datos['Hijos'] == respuestas_usuario['Hijos']:
            puntuacion += 1
        coincidencias.append((datos['NombreCompleto'], puntuacion))
    coincidencias.sort(key=lambda x: x[1], reverse=True)
    return coincidencias[:3]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    await update.message.reply_text(
        f"¡Bienvenid@ {user.first_name}! Usa el comando /love para empezar el cuestionario.")
    return ConversationHandler.END


async def love(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    teclado = [["Hombre", "Mujer"]]
    reply_markup = ReplyKeyboardMarkup(teclado, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("¿Cuál es tu sexo?", reply_markup=reply_markup)
    return PREGUNTA_SEXO


async def sexo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['Sexo'] = update.message.text
    await update.message.reply_text("¿Cuál es tu edad? (Escribe un número)")
    return PREGUNTA_EDAD


async def edad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['Edad'] = int(update.message.text)
    teclado = [["Informatica", "Comercio", "Deporte", "Mecanizado"]]
    reply_markup = ReplyKeyboardMarkup(teclado, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("¿Cuál es tu área de estudio o trabajo?", reply_markup=reply_markup)
    return PREGUNTA_GRADO


async def grado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['Grado'] = update.message.text
    teclado = [["Relacion estable", "Nada serio", "Duda"]]
    reply_markup = ReplyKeyboardMarkup(teclado, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("¿Qué tipo de relación buscas?", reply_markup=reply_markup)
    return PREGUNTA_FIN


async def fin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['Fin'] = update.message.text
    teclado = [["Si quiere", "No quiere", "Duda"]]
    reply_markup = ReplyKeyboardMarkup(teclado, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("¿Quieres tener hijos?", reply_markup=reply_markup)
    return PREGUNTA_HIJOS


async def hijos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['Hijos'] = update.message.text
    resultados = calcular_afinidad(context.user_data)
    mensaje = "Aquí están tus 3 mejores coincidencias:\n"
    for nombre, puntuacion in resultados:
        mensaje += f"{nombre} (Puntuación: {puntuacion})\n"
    await update.message.reply_text(mensaje)
    return ConversationHandler.END


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Has detenido el cuestionario. Usa /love para empezar de nuevo.")
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("love", love)],
        states={
            PREGUNTA_SEXO: [MessageHandler(filters.TEXT & ~filters.COMMAND, sexo)],
            PREGUNTA_EDAD: [MessageHandler(filters.TEXT & ~filters.COMMAND, edad)],
            PREGUNTA_GRADO: [MessageHandler(filters.TEXT & ~filters.COMMAND, grado)],
            PREGUNTA_FIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, fin)],
            PREGUNTA_HIJOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, hijos)],
        },
        fallbacks=[CommandHandler("stop", stop)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
