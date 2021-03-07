-- Table: public.clicklog

-- DROP TABLE public.clicklog;

CREATE TABLE public.clicklog
(
    id uuid NOT NULL,
    ts timestamp with time zone NOT NULL,
    token character varying(20) COLLATE pg_catalog."default" NOT NULL,
    source character varying(100) COLLATE pg_catalog."default" NOT NULL,
    headers json NOT NULL,
    CONSTRAINT clicklog_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.clicklog
    OWNER to admin;

GRANT INSERT, SELECT ON TABLE public.clicklog TO clicklog;