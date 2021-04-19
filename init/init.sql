
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

CREATE SEQUENCE public.dimension_projet_idprojet_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.dimension_projet_idprojet_seq OWNED BY public.dimension_projet.idprojet;

CREATE TABLE public.dimension_projetvm (
    idprojet integer NOT NULL,
    idvm integer NOT NULL,
    idprojetvm integer NOT NULL
);

CREATE SEQUENCE public.dimension_projetvm_idprojetvm_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 
ALTER SEQUENCE public.dimension_projetvm_idprojetvm_seq OWNED BY public.dimension_projetvm.idprojetvm;

CREATE TABLE public.dimension_syges (
    idsyges integer NOT NULL,
    client character varying(1000) NOT NULL,
    costcenter character varying(1000) NOT NULL,
    syges character varying(1000) NOT NULL
); 

CREATE SEQUENCE public.dimension_syges_idsyges_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.dimension_syges_idsyges_seq OWNED BY public.dimension_syges.idsyges;

CREATE TABLE public.dimension_vm (
    idvm integer NOT NULL,
    idprojet integer NOT NULL,
    hebergeur character varying(1000) NOT NULL,
    typevm character varying(1000) NOT NULL,
    vm character varying(1000) NOT NULL
);

CREATE SEQUENCE public.dimension_vm_idvm_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.dimension_vm_idvm_seq OWNED BY public.dimension_vm.idvm;

CREATE TABLE public.fait_cout (
    date_cout date NOT NULL,
    montant_hors_licencems double precision,
    montant_licencems double precision,
    idprojetvm integer NOT NULL
);

ALTER TABLE ONLY public.dimension_projet ALTER COLUMN idprojet SET DEFAULT nextval('public.dimension_projet_idprojet_seq'::regclass);

ALTER TABLE ONLY public.dimension_projetvm ALTER COLUMN idprojetvm SET DEFAULT nextval('public.dimension_projetvm_idprojetvm_seq'::regclass);

ALTER TABLE ONLY public.dimension_syges ALTER COLUMN idsyges SET DEFAULT nextval('public.dimension_syges_idsyges_seq'::regclass);

ALTER TABLE ONLY public.dimension_vm ALTER COLUMN idvm SET DEFAULT nextval('public.dimension_vm_idvm_seq'::regclass);

ALTER TABLE ONLY public.fait_cout
    ADD CONSTRAINT cout_pk PRIMARY KEY (date_cout, idprojetvm);

ALTER TABLE ONLY public.dimension_projet
    ADD CONSTRAINT employees_pk PRIMARY KEY (idprojet);

ALTER TABLE ONLY public.dimension_projetvm
    ADD CONSTRAINT idprojet_pk PRIMARY KEY (idprojetvm);

ALTER TABLE ONLY public.dimension_syges
    ADD CONSTRAINT syges_pk PRIMARY KEY (idsyges);

ALTER TABLE ONLY public.fait_cout
    ADD CONSTRAINT unique_cout UNIQUE (date_cout, idprojetvm);

ALTER TABLE ONLY public.dimension_projet
    ADD CONSTRAINT unique_projet UNIQUE (idsyges, chefprojet, projet);

ALTER TABLE ONLY public.dimension_projetvm
    ADD CONSTRAINT unique_projetvm UNIQUE (idprojet, idvm);

ALTER TABLE ONLY public.dimension_syges
    ADD CONSTRAINT unique_syges UNIQUE (client, costcenter, syges);

ALTER TABLE ONLY public.dimension_vm
    ADD CONSTRAINT unique_vm UNIQUE (hebergeur, typevm, idprojet, vm);

ALTER TABLE ONLY public.dimension_vm
    ADD CONSTRAINT vm_pk PRIMARY KEY (idvm);
 
ALTER TABLE ONLY public.dimension_projetvm
    ADD CONSTRAINT fk_projet FOREIGN KEY (idprojet) REFERENCES public.dimension_projet(idprojet);

ALTER TABLE ONLY public.fait_cout
    ADD CONSTRAINT fk_projetvm FOREIGN KEY (idprojetvm) REFERENCES public.dimension_projetvm(idprojetvm);
 
ALTER TABLE ONLY public.dimension_projetvm
    ADD CONSTRAINT fk_vm FOREIGN KEY (idvm) REFERENCES public.dimension_vm(idvm);

GRANT ALL ON TABLE public.dimension_projet TO guest;


GRANT ALL ON SEQUENCE public.dimension_projet_idprojet_seq TO guest;


GRANT ALL ON TABLE public.dimension_projetvm TO guest;


GRANT ALL ON SEQUENCE public.dimension_projetvm_idprojetvm_seq TO guest;


GRANT ALL ON TABLE public.dimension_syges TO guest;


GRANT ALL ON SEQUENCE public.dimension_syges_idsyges_seq TO guest;


GRANT ALL ON TABLE public.dimension_vm TO guest;


GRANT ALL ON SEQUENCE public.dimension_vm_idvm_seq TO guest;


GRANT ALL ON TABLE public.fait_cout TO guest;


