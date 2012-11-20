from helpers.log import getlogger
import logging
from helpers.ansistrm import ColorizingStreamHandler

logging.getLogger().setLevel(logging.ERROR)

test_logger = getlogger("testlogger")
test_logger.setLevel(logging.INFO)
handler = ColorizingStreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s]%(levelname)s:%(message)s", None))
test_logger.addHandler(handler)
test_logger.propagate = False

def test_error(str):
    test_logger.error(str)
    
def test_alert(str):
    test_logger.warning(str)
    
def test_info(str):
    test_logger.info(str)
    