import os
import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details:sys) -> None:
        self.error_message = error_message
        _,_,exec_tb = error_details.exc_info()
        
        self.lineno = exec_tb.tb_lineno
        self.file_name = exec_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(self.file_name, self.lineno, str(self.error_message))

    
if __name__ == "__main__":
    try:
        logger.logging.info("Entering the try block")
        a = 1/0
        print("This will not be printed", a)
    except Exception as e:
        raise NetworkSecurityException(e, sys)



