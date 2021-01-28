from content.exceptions import FuncNotCompliantException


class Processed_line:

    def __init__(self, item):
        self.type_file = item.get("type_file")
        self.content = item.get("content")
        self.content = self._construct_line()

    def integrate(self, postgres_serializer):  # insertion des données
        postgres_serializer.insert(self.content)

    def get_values(self):
        return self.content

    def _construct_line(self):
        _, _, func = self.type_file
        try:
            return func(self.content)
        except FuncNotCompliantException:
            pass
