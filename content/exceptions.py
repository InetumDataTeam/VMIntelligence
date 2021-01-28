class SourceError(Exception):
    pass


class TransformError(Exception):
    pass


class SerializationError(Exception):
    pass


class FileNameException(Exception):
    pass


class FileTypeException(object):
    pass


class DirNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        default_message = "The directory does not exists"
        if not args:
            super().__init__(default_message)
