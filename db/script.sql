CREATE SCHEMA knowledge_base;

CREATE TABLE model (
	id serial PRIMARY KEY,
	uuid VARCHAR (256) UNIQUE NOT NULL,
	category VARCHAR (256),
	author VARCHAR (256),
	updated date,
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
    additional json
)
