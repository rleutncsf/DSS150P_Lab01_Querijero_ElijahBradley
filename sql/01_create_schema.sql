-- This schema formalizes the customers.csv source for lab purposes.
-- customer_id is used as the primary key based on profiling evidence showing
-- no null values and a consistent "C####" format in the sample file.

CREATE SCHEMA IF NOT EXISTS lab;

CREATE TABLE IF NOT EXISTS lab.customers (
    customer_id      TEXT PRIMARY KEY,
    first_name       TEXT NOT NULL,
    last_name        TEXT NOT NULL,
    email            TEXT,
    city             TEXT,
    signup_date      DATE,
    customer_segment TEXT,

    -- Guards against malformed IDs slipping past a plain TEXT column
    CONSTRAINT ck_customer_id_format CHECK (customer_id ~ '^C[0-9]{4,}$'),

    -- Only enforce known segment values because the profile observed a small,
    -- apparently fixed set of values; revisit if the source owner confirms otherwise
    CONSTRAINT ck_customer_segment_known CHECK (
        customer_segment IN ('Retail', 'SME', 'Professional', 'Student')
        OR customer_segment IS NULL
    )
);
