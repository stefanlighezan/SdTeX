class SdTeXError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class SdTeXSyntaxError(SdTeXError):
    pass

class SdTeXProcessingError(SdTeXError):
    pass

class SdTeXUnclosedBracketError(SdTeXError):
    pass

class SdTeXTagNotFoundError(SdTeXError):
    pass

class SdTeXVariableError(SdTeXError):
    pass

class SdTeXStyleError(SdTeXError):
    pass

class SdTeXAttributeError(SdTeXError):
    pass

class SdTeXSrcError(SdTeXError):
    pass

# Add more error classes as needed for specific error scenarios
