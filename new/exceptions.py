class SourceError(Exception) :
    def __init__(self, message, errors):
        super().__init__(message)

class TransformError(Exception) :
    def __init__(self, message, errors):
        super().__init__(message)

class SerializationError(Exception) :
    def __init__(self, message, errors):
        super().__init__(message)