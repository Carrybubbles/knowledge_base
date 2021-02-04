CREATE SCHEMA knowledge_base;

CREATE TABLE model (
	id serial PRIMARY KEY,
	model_name VARCHAR (256) NOT NULL,
	uuid VARCHAR (256) UNIQUE NOT NULL,
	description TEXT,
	x VARCHAR (256) [] NOT NULL,
	y VARCHAR (256) NOT NULL
);
