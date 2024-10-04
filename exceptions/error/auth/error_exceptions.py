class PasswordNotExist(Exception):
    pass

class EmailNotExist(Exception):
    pass

class UserDoesExist(Exception):
    pass

class NotFound(Exception):
    pass

class ValidationError(Exception):
    def __init__(self, error, *args: object) -> None:
        self.error = error

class VerifyCodeDoesNotExist(Exception):
    def __init__(self, error_message) -> None:
        self.error_message = error_message
    
        