USE demodb;

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username STRING NOT NULL UNIQUE,
    email_address STRING NOT NULL UNIQUE,
    active BOOL DEFAULT true,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO writer_user;
