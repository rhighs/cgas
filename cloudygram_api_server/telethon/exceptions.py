class TTUnathorizedException(Exception):
    def __init__(self, message: str = None):
        if message == None:
            message = "The user trying to access telegram features is not authorized."
        super().__init__(message)

class TTGenericException(Exception):
    def __init__(self, message):
        super().__init__(message)

class TTSignInException(Exception):
    def __init__(self, message: str = None):
        if message == None:
            message = "Some of the provided codes isn't valid for authentication."
        super().__init__(message)

class TTNeeds2FAException(Exception):
    def __init__(self, message: str = None):
        if message == None:
            message = "2FA detected, please provide a password at signin"
        super().__init__(message)

class TTFileTransferException(Exception):
    def __init__(self, message: str = None):
        if message == None:
            message = "Some network error occured while transferring the file."
        super().__init__(message)

