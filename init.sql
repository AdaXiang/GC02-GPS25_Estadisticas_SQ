--
-- PostgreSQL database dump
--

\restrict fLbr23K4IglVRztuqFdoQV2eN3Ft4trWUD0H5syumTsjZKDEWof1hKpjtiUgeGa

-- Dumped from database version 16.10
-- Dumped by pg_dump version 16.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: artistasmensual; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artistasmensual (
    idartista integer NOT NULL,
    numoyentes bigint DEFAULT 0 NOT NULL,
    valoracionmedia bigint DEFAULT 0 NOT NULL,
    CONSTRAINT artistasmensual_numoyentes_check CHECK ((numoyentes >= 0)),
    CONSTRAINT artistasmensual_numseguidores_check CHECK ((valoracionmedia >= 0))
);


ALTER TABLE public.artistasmensual OWNER TO postgres;

--
-- Name: busquedasartistas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.busquedasartistas (
    id integer NOT NULL,
    idartista integer NOT NULL,
    idusuario integer,
    fecha timestamp without time zone DEFAULT now()
);


ALTER TABLE public.busquedasartistas OWNER TO postgres;

--
-- Name: busquedasartistas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.busquedasartistas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.busquedasartistas_id_seq OWNER TO postgres;

--
-- Name: busquedasartistas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.busquedasartistas_id_seq OWNED BY public.busquedasartistas.id;


--
-- Name: comunidadesmensual; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comunidadesmensual (
    idcomunidad integer NOT NULL,
    numpublicaciones bigint DEFAULT 0 NOT NULL,
    nummiembros bigint DEFAULT 0 NOT NULL,
    CONSTRAINT comunidadesmensual_nummiembros_check CHECK ((nummiembros >= 0)),
    CONSTRAINT comunidadesmensual_numpublicaciones_check CHECK ((numpublicaciones >= 0))
);


ALTER TABLE public.comunidadesmensual OWNER TO postgres;

--
-- Name: contenidosmensual; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contenidosmensual (
    idcontenido integer NOT NULL,
    esalbum boolean NOT NULL,
    sumavaloraciones numeric(2,1) DEFAULT 0 NOT NULL,
    numcomentarios integer DEFAULT 0 NOT NULL,
    numventas bigint DEFAULT 0 NOT NULL,
    genero character varying(35),
    esnovedad boolean DEFAULT false,
    CONSTRAINT contenidosmensual_numcomentarios_check CHECK ((numcomentarios >= 0)),
    CONSTRAINT contenidosmensual_numreproducciones_check CHECK ((numventas >= 0)),
    CONSTRAINT contenidosmensual_sumavaloraciones_check CHECK ((sumavaloraciones >= (0)::numeric))
);


ALTER TABLE public.contenidosmensual OWNER TO postgres;

--
-- Name: generosmensual; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.generosmensual (
    idgenero integer NOT NULL,
    numreproducciones bigint NOT NULL,
    CONSTRAINT generosmensual_numreproducciones_check CHECK ((numreproducciones >= 0))
);


ALTER TABLE public.generosmensual OWNER TO postgres;

--
-- Name: busquedasartistas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.busquedasartistas ALTER COLUMN id SET DEFAULT nextval('public.busquedasartistas_id_seq'::regclass);


--
-- Name: artistasmensual artistasmensual_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artistasmensual
    ADD CONSTRAINT artistasmensual_pkey PRIMARY KEY (idartista);


--
-- Name: busquedasartistas busquedasartistas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.busquedasartistas
    ADD CONSTRAINT busquedasartistas_pkey PRIMARY KEY (id);


--
-- Name: comunidadesmensual comunidadesmensual_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comunidadesmensual
    ADD CONSTRAINT comunidadesmensual_pkey PRIMARY KEY (idcomunidad);


--
-- Name: contenidosmensual contenidosmensual_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contenidosmensual
    ADD CONSTRAINT contenidosmensual_pkey PRIMARY KEY (idcontenido);


--
-- Name: generosmensual generosmensual_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.generosmensual
    ADD CONSTRAINT generosmensual_pkey PRIMARY KEY (idgenero);


--
-- PostgreSQL database dump complete
--

\unrestrict fLbr23K4IglVRztuqFdoQV2eN3Ft4trWUD0H5syumTsjZKDEWof1hKpjtiUgeGa

