-- Procedure 1: Insert or Update Contact

CREATE OR REPLACE PROCEDURE upsert_contact(
    p_username VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE username = p_username
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE username = p_username;
    ELSE
        INSERT INTO phonebook(username, phone)
        VALUES (p_username, p_phone);
    END IF;
END;
$$;


-- Procedure 2: Delete Contact

CREATE OR REPLACE PROCEDURE delete_contact(
    p_value VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE username = p_value
       OR phone = p_value;
END;
$$;


-- Procedure 3: Insert Many Contacts

CREATE OR REPLACE PROCEDURE insert_many_contacts(
    usernames TEXT[],
    phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
BEGIN
    IF array_length(usernames, 1) IS DISTINCT FROM array_length(phones, 1) THEN
        RAISE EXCEPTION 'Arrays must have the same length';
    END IF;

    FOR i IN 1..array_length(usernames, 1)
    LOOP

        IF phones[i] ~ '^[0-9]{11}$' THEN

            IF EXISTS (
                SELECT 1
                FROM phonebook
                WHERE username = usernames[i]
            ) THEN

                UPDATE phonebook
                SET phone = phones[i]
                WHERE username = usernames[i];

            ELSE

                INSERT INTO phonebook(username, phone)
                VALUES (usernames[i], phones[i]);

            END IF;

        ELSE

            RAISE NOTICE 'Invalid phone: %, %',
                usernames[i],
                phones[i];

        END IF;

    END LOOP;

END;
$$;