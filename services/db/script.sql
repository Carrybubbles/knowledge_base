CREATE SCHEMA knowsledge_base;

CREATE TABLE knowsledge_base.accounts (
	id serial PRIMARY KEY,
	model_name VARCHAR (256) UNIQUE NOT NULL,
	x VARCHAR (256) [],
	y VARCHAR (256) NOT NULL
);