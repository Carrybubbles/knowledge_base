CREATE SCHEMA knowledge_base;

CREATE TABLE model (
	id serial PRIMARY KEY,
	uuid VARCHAR (256) UNIQUE NOT NULL,
	category VARCHAR (256),
	author VARCHAR (256),
	creation_time timestamp,
	variant int,
	task VARCHAR (256),
	filename VARCHAR (256),
	is_full_to_train boolean,
	updated timestamp,
	hash_data_train VARCHAR(256),
	hash_data_test VARCHAR(256),
	task_type VARCHAR(20),
	file bytea NOT NULL,
    x VARCHAR (256)[],
	y VARCHAR (256),
	description TEXT,
	metric_id int,
	CONSTRAINT fk_metric FOREIGN KEY(metric_id) REFERENCES metric(id)
);

CREATE TABLE metric(
    id serial PRIMARY KEY,
    r2 numeric,
    mse numeric,
    rmse numeric,
    maxf1 numeric,
    additional json
)
