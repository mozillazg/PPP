-- Table: image

-- DROP TABLE image;

CREATE TABLE image
(
  image_id bigserial NOT NULL,
  description text NOT NULL DEFAULT ''::text,
  link text NOT NULL,
  username text NOT NULL DEFAULT ''::text,
  visit integer NOT NULL DEFAULT 0,
  "like" integer NOT NULL DEFAULT 0,
  img text NOT NULL,
  thumb text NOT NULL,
  CONSTRAINT image_pkey PRIMARY KEY (image_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE image OWNER TO postgres;
