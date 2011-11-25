-- Table: image

-- DROP TABLE image;

CREATE TABLE image
(
  image_id bigserial NOT NULL,
  description text NOT NULL DEFAULT ''::text,
  link text NOT NULL,
  username text NOT NULL DEFAULT ''::text,
  visit integer NOT NULL DEFAULT 0,
  likes integer NOT NULL DEFAULT 0,
  img text NOT NULL,
  thumb text NOT NULL,
  CONSTRAINT image_pkey PRIMARY KEY (image_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE image OWNER TO postgres;



-- Table: user_

-- DROP TABLE user_;

CREATE TABLE user_
(
  user_id integer NOT NULL DEFAULT nextval('user_user_id_seq'::regclass),
  user_name text NOT NULL,
  user_pass text NOT NULL,
  "admin" boolean,
  CONSTRAINT user_pkey PRIMARY KEY (user_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE user_ OWNER TO postgres;




