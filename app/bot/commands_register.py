from telegram.ext import CommandHandler, Application, MessageHandler, filters, ConversationHandler

from app.bot.extension import ELEGIR_MOVIMIENTO, ELEGIR_POKEMON
from app.bot.commands import (
    start,
    help_command,
    cancel,
    elegir_pokemon,
    elegir_movimiento
)

COMMANDS = [
    ("start", start),
    ("ayuda", help_command),
    ("cancelar", cancel),
    ("elegir-pokemon", elegir_pokemon),
    ("elegir-moviiento", elegir_movimiento)
]

def register_commands(app: Application) -> None:
    """Agrega todos los CommandHandler al objeto Application."""
    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ELEGIR_POKEMON: [MessageHandler(filters.TEXT & ~filters.COMMAND, elegir_pokemon)],
            ELEGIR_MOVIMIENTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, elegir_movimiento)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('cancel', cancel))