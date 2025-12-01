--
-- PostgreSQL database dump clean + Nueva tabla historialreproducciones
--

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

-- ============================================================
-- 1. Tabla: artistasmensual
-- ============================================================
CREATE TABLE public.artistasmensual (
    idartista integer NOT NULL,
    numoyentes bigint DEFAULT 0 NOT NULL,
    valoracionmedia bigint DEFAULT 0 NOT NULL,
    CONSTRAINT artistasmensual_numoyentes_check CHECK ((numoyentes >= 0)),
    CONSTRAINT artistasmensual_numseguidores_check CHECK ((valoracionmedia >= 0))
);

ALTER TABLE public.artistasmensual OWNER TO postgres;

-- ============================================================
-- 2. Tabla: busquedasartistas (con su secuencia)
-- ============================================================
CREATE TABLE public.busquedasartistas (
    id integer NOT NULL,
    idartista integer NOT NULL,
    idusuario integer,
    fecha timestamp without time zone DEFAULT now()
);

ALTER TABLE public.busquedasartistas OWNER TO postgres;

CREATE SEQUENCE public.busquedasartistas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.busquedasartistas_id_seq OWNER TO postgres;
ALTER SEQUENCE public.busquedasartistas_id_seq OWNED BY public.busquedasartistas.id;

ALTER TABLE ONLY public.busquedasartistas ALTER COLUMN id SET DEFAULT nextval('public.busquedasartistas_id_seq'::regclass);

-- ============================================================
-- 3. Tabla: comunidadesmensual
-- ============================================================
CREATE TABLE public.comunidadesmensual (
    idcomunidad integer NOT NULL,
    numpublicaciones bigint DEFAULT 0 NOT NULL,
    nummiembros bigint DEFAULT 0 NOT NULL,
    CONSTRAINT comunidadesmensual_nummiembros_check CHECK ((nummiembros >= 0)),
    CONSTRAINT comunidadesmensual_numpublicaciones_check CHECK ((numpublicaciones >= 0))
);

ALTER TABLE public.comunidadesmensual OWNER TO postgres;

-- ============================================================
-- 4. Tabla: contenidosmensual
-- ============================================================
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

-- ============================================================
-- 6. NUEVA TABLA: historialreproducciones
-- ============================================================
CREATE TABLE public.historialreproducciones (
    id SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_contenido INT NOT NULL,
    fecha_reproduccion TIMESTAMP DEFAULT NOW(),
    segundos_reproducidos INT DEFAULT 0
);

ALTER TABLE public.historialreproducciones OWNER TO postgres;

-- ============================================================
-- Primary Keys (Resto de tablas)
-- ============================================================

ALTER TABLE ONLY public.artistasmensual
    ADD CONSTRAINT artistasmensual_pkey PRIMARY KEY (idartista);

ALTER TABLE ONLY public.busquedasartistas
    ADD CONSTRAINT busquedasartistas_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.comunidadesmensual
    ADD CONSTRAINT comunidadesmensual_pkey PRIMARY KEY (idcomunidad);

ALTER TABLE ONLY public.contenidosmensual
    ADD CONSTRAINT contenidosmensual_pkey PRIMARY KEY (idcontenido);


