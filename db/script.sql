CREATE SCHEMA knowledge_base;

CREATE TABLE model (
	id serial PRIMARY KEY,
	uuid VARCHAR (256) UNIQUE NOT NULL,
	category VARCHAR (256),
	model_name VARCHAR (256) NOT NULL,
    file bytea NOT NULL,
    x VARCHAR (256) [] NOT NULL,
	y VARCHAR (256) NOT NULL,
	metrics json,
	description TEXT,
);
