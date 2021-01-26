from new.functions import *
from new.context import *
from new.exceptions import *
from new.postgres_serializer import *

import logging

pwd = ""
bdd_name = ""
path = ""
ctx = Context().add_source_path("")
postgres_serializer = Postgres_serializer().add_pwd(pwd).add_bdd_name(bdd_name)
it = None

try:
    it = source(ctx, combinator)
except SourceError as e:
    logging.error(e)

if it:
    for item in it:
        try:
            processed_line = pipeline(item)
            processed_line.integrate(ctx, postgres_serializer)
        except TransformError as e:
            logging.error(e)

        except SerializationError as e:
            logging.error(e)
