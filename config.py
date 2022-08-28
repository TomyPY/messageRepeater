import logging
import os

logging.basicConfig(
    filename="test_rollCall.log",
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'

)

TELEGRAM_TOKEN='5468621967:AAGedvS4KfHEv8702ZacnG0eybxBIz1D27E'

location='./MessagesDatabase.json'