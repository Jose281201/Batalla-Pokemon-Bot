from pathlib import Path
from datetime import datetime

import logging
import sys
import io


class LoggerConfig:
    """Configura logging para ver errores."""
    def __init__(self):
        """Inicializa la configuración del logger."""
        self.file = self.log_file
        
        # Asegura que el directorio de logs exista
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    log_file = logs_dir / f"bot_{datetime.now().strftime('%Y-%m-%d')}.log"

    def setup_logging(self):
        """Configura el logger con formato y nivel de logging."""    
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO,
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler(stream=sys.stdout),
            ]
        )
     
        # Configuración adicional para la consola en Windows
        if sys.platform == "win32":
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        
        logger = logging.getLogger(__name__)
        
        return logger