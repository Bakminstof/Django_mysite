CREATE ROLE django_user WITH LOGIN;
ALTER USER django_user WITH PASSWORD 'Nx4jCe1ARlnXGu+9DMhTqqjGsbLf2RUYRZmJRnVLAw24!cWL!V';

CREATE DATABASE django_db;
CREATE SCHEMA django_db_schema;

GRANT ALL ON DATABASE django_db TO django_user;

ALTER DATABASE django_db OWNER TO django_user;

GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA django_db_schema TO django_user;
