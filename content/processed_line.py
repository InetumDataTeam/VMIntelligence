from content.exceptions import FuncNotCompliantException
from loguru import logger


class Processed_line:

    def __init__(self, item):
        self.content, self.type_file = item
        self.content = self.__construct_line()

    def integrate(self, postgres_serializer):
        postgres_serializer.insert(self.content)

    def get_values(self):
        return self.content

    def __construct_line(self):
        type, filename = self.type_file
        _, _, func = type

        try:
            return func.init(_, self.content, filename)
        except FuncNotCompliantException:
            pass
