class SourceError(Exception):
    pass


class TransformError(Exception):
    pass


class SerializationError(Exception):
    pass


class FileNameException(Exception):
    def __init__(self, *args, **kwargs):
        default_message = "Filename not compliant"
        if not args:
            super().__init__(default_message)


class FileTypeException(Exception):
    def __init__(self, *args, **kwargs):
        default_message = "Type is empty"
        if not args:
            super().__init__(default_message)


class DirNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        default_message = "The directory does not exists"
        if not args:
            super().__init__(default_message)


class FuncNotCompliantException(Exception):
    def __init__(self, *args, **kwargs):
        default_message = "Function not compliant or content is empty"
        if not args:
            super().__init__(default_message)


class InsertionException(Exception):
    def __init__(self, *args, **kwargs):
        default_message = "Content inserted is not compliant"
        if not args:
            super().__init__(default_message)

