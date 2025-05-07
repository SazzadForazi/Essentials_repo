import os
import logging

# Create and configure logger
logging.basicConfig(filename="logs/logfile.log",
                    format='%(asctime)s: %(levelname)s: %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)




def test_func(input):
    print(f'Test function {input}')

if __name__ == '__main__':
    # Test messages
    logger.debug("Harmless debug Message")
    logger.info("Just an information")
    logger.warning("Its a Warning")
    logger.error("Did you try to divide by zero")
    logger.critical("Internet is down")
    test_func('Hello')