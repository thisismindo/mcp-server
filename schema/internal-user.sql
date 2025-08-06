-- Secure mode
-- Uncomment below for production environment
--
-- CREATE USER reader_user WITH LOGIN PASSWORD 'replace-me-with-secure-password';
-- CREATE USER writer_user WITH LOGIN PASSWORD 'replace-me-with-secure-password';
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader_user;
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO writer_user;

-- Insecure mode
CREATE USER reader_user;
CREATE USER writer_user;

CREATE DATABASE demodb;

REVOKE ALL ON DATABASE demodb FROM PUBLIC;

GRANT CONNECT ON DATABASE demodb TO reader_user;
GRANT USAGE ON SCHEMA demodb.public TO reader_user;
GRANT SELECT ON ALL TABLES IN SCHEMA demodb.public TO reader_user;

GRANT CONNECT ON DATABASE demodb TO writer_user;
GRANT USAGE ON SCHEMA demodb.public TO writer_user;
GRANT ALL ON ALL TABLES IN SCHEMA demodb.public TO writer_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA demodb.public GRANT SELECT ON TABLES TO reader_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA demodb.public GRANT ALL ON TABLES TO writer_user;
