import sys
import logging
import src.logger  # This imports the logger module, which sets up logging configuration

def error_message_detail(error, error_detail):
    _,_,exc_tb = error_detail.exc_info() # gives out which file the exception has occured, on which line number
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in Python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message

class CustomException(Exception): # this inheritance will allow this class to behave like normal exceptions (you can raise and catch it), but with extra functionality that we can define
    def __init__(self, error_message, error_detail):
        super().__init__(error_message) # inherits the __init__() function from the parent class Exception
        # Ensures the base Exception properly stores the message so Python's exception system can still use it (e.g., printing the exception).
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        return self.error_message
    
# if __name__ == "__main__":
#     try:
#         a = 1/0
#     except Exception as e:
#         logging.info("Divide by zero")
#         raise CustomException(e, sys)