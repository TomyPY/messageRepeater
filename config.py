import logging
import os

logging.basicConfig(
    filename="test_rollCall.log",
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'

)

TELEGRAM_TOKEN=os.environ["TELEGRAM_TOKEN"]

location='./MessagesDatabase.json'