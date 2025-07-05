"""Módulo de utilidad de logger para el bot de Telegram

Este módulo proporciona una interfaz simple para obtener instancias de logger configuradas
para diferentes módulos del bot de Telegram.
"""

import logging


def get_logger(name):
    """Obtiene una instancia del logger para un módiulo en concreto.
    
    Args:
        name: Nombre del módulo o componente para el que se desea el logger.
        
    Returns:
        logging.Logger: Instancia del logger configurada con el nombre proporcionado.
    """
    return logging.getLogger(name)