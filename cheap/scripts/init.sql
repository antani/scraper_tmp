create schema cheapr;

DROP TABLE mobile_brands;
DROP TABLE mobile_models;

TRUNCATE TABLE mobile_models;
TRUNCATE TABLE mobile_brands;

CREATE TABLE cheapr.mobile_models(name VARCHAR(400),canonical_name VARCHAR(1024),img VARCHAR(1024),url VARCHAR(1024),description VARCHAR(1024),maker VARCHAR(256),fields TEXT,id integer NOT NULL primary key,top_mobile integer DEFAULT 0);

CREATE TABLE mobile_brands (
link VARCHAR(1024),
name VARCHAR(200),
img VARCHAR(1024),
id integer NOT NULL primary key,
top_brand integer DEFAULT 0
);



CREATE EXTENSION pg_trgm;

CREATE INDEX trgm_idx_brands ON mobile_brands USING gin (name gin_trgm_ops);
CREATE INDEX trgm_idx_models ON mobile_models USING gin (name gin_trgm_ops);

CREATE INDEX trgm_idx_brands_gist ON mobile_brands USING gist (name gist_trgm_ops);
CREATE INDEX trgm_idx_models_gist ON mobile_models USING gist (name gist_trgm_ops);

CREATE INDEX top_mobile_brands_idx ON mobile_brands ( top_brand desc );
CREATE INDEX top_mobile_models_idx ON mobile_models ( top_mobile desc );

CREATE INDEX mobile_models_name_idx ON mobile_models ( maker );

SELECT * FROM mobile_brands order by top_brand desc;
SELECT * FROM mobile_models where maker = 'Samsung';

update mobile_brands set top_brand=1 where name in ('Samsung','Nokia','Micromax','Apple','Lava','XOLO','LG','Motorola');

SELECT name, canonical_name, description, img, fields, similarity(name, 'moto x (2nd gen) (black)') AS sml FROM mobile_models WHERE name % 'moto x (2nd gen) (black)' ORDER BY sml DESC, name;

u''

SELECT * FROM mobile_models WHERE name LIKE '%okia%520%';

SELECT name, canonical_name, description, img, fields, similarity(name, 'moto e') AS sml
  FROM mobile_models
  WHERE name % 'moto e'
  ORDER BY sml DESC, name;

select name from mobile_models where name % 'motorola moto e (black)';


select similarity('amzer mobile back cover for motorola moto e xt1022 (black)','moto e') from mobile_models limit(1);