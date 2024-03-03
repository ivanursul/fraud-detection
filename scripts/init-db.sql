-- Enhance the User table structure
CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    creation_date DATE
);

-- Insert Random Users with more names, emails, and creation dates
DO $$
DECLARE
    i INT;
    first_names TEXT[] := ARRAY['John', 'Jane', 'Mary', 'Michael', 'Sarah', 'Robert', 'James', 'Jennifer', 'Linda', 'William', 'Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Mia', 'Charlotte', 'Amelia', 'Evelyn', 'Abigail'];
    last_names TEXT[] := ARRAY['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin'];
    first_name TEXT;
    last_name TEXT;
    email TEXT;
    creation_date DATE;
BEGIN
    FOR i IN 1..1000 LOOP
        first_name := first_names[1 + floor(random() * array_length(first_names, 1))];
        last_name := last_names[1 + floor(random() * array_length(last_names, 1))];
        email := lower(first_name) || '.' || lower(last_name) || (1 + floor(random() * 1000))::TEXT || '@example.com';
        creation_date := (DATE '2014-01-01' + (floor(random() * (365 * 10 + 3))::INT * '1 day'::INTERVAL))::DATE;
        EXECUTE format('INSERT INTO Users (first_name, last_name, email, creation_date) VALUES (%L, %L, %L, %L)', first_name, last_name, email, creation_date);
    END LOOP;
END $$;

CREATE TABLE IF NOT EXISTS Transactions (
    id SERIAL PRIMARY KEY,
    Time NUMERIC NOT NULL,
    user_id INTEGER NOT NULL,
    V1 NUMERIC NOT NULL,
    V2 NUMERIC NOT NULL,
    V3 NUMERIC NOT NULL,
    V4 NUMERIC NOT NULL,
    V5 NUMERIC NOT NULL,
    V6 NUMERIC NOT NULL,
    V7 NUMERIC NOT NULL,
    V8 NUMERIC NOT NULL,
    V9 NUMERIC NOT NULL,
    V10 NUMERIC NOT NULL,
    V11 NUMERIC NOT NULL,
    V12 NUMERIC NOT NULL,
    V13 NUMERIC NOT NULL,
    V14 NUMERIC NOT NULL,
    V15 NUMERIC NOT NULL,
    V16 NUMERIC NOT NULL,
    V17 NUMERIC NOT NULL,
    V18 NUMERIC NOT NULL,
    V19 NUMERIC NOT NULL,
    V20 NUMERIC NOT NULL,
    V21 NUMERIC NOT NULL,
    V22 NUMERIC NOT NULL,
    V23 NUMERIC NOT NULL,
    V24 NUMERIC NOT NULL,
    V25 NUMERIC NOT NULL,
    V26 NUMERIC NOT NULL,
    V27 NUMERIC NOT NULL,
    V28 NUMERIC NOT NULL,
    Amount NUMERIC NOT NULL
);

ALTER TABLE public.transactions
ADD COLUMN created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP;


CREATE TABLE IF NOT EXISTS  Fraudulent_Analysis (
    id SERIAL PRIMARY KEY,
    transaction_id INT NOT NULL,
    user_id INT NOT NULL,
    is_fraud BOOLEAN NOT NULL
);