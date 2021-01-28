class Processed_line:

    def __init__(self, item):
        type_file = item.get("type_file")
        content = item.get("content")
        self._construct_line(type_file, content)

    def integrate(self, ctx, postgres_serializer):
        pass

    def get_values(self):
        pass

    def _construct_line(self, type_file, content):
        pass
