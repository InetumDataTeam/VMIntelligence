
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT * FROM pg_catalog.pg_user WHERE  usename = 'guest') THEN
      create user guest WITH PASSWORD 'tseug';
   END IF;
END
$do$;

GRANT ALL PRIVILEGES ON DATABASE postgres TO guest;

CREATE TABLE public.dimension_projet (
    idprojet integer NOT NULL,
    idsyges integer NOT NULL,
    chefprojet character varying(1000) NOT NULL,
    projet character varying(1000) NOT NULL
);

