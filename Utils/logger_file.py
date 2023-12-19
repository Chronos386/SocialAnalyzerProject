import logging
from logging.handlers import TimedRotatingFileHandler


class CustomFileHandler(TimedRotatingFileHandler):
    def emit(self, record):
        super().emit(record)
        self.stream.write("\n")


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)  # Устанавливаем уровень логирования на ERROR и выше

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = CustomFileHandler('Logs/error.log', when="midnight", interval=1, backupCount=5, encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
