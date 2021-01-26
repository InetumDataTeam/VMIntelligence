from new.processed_line import Processed_line


def pipeline(item):
    return Processed_line()

def source(ctx, conbinator):
    return conbinator(ctx)

def combinator(ctx):
    return []

