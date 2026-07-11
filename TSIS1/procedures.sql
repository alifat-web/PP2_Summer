-- ===========================================
-- Procedure 1: Add Phone

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    contactid INTEGER;
BEGIN

    SELECT id
    INTO contactid
    FROM contacts
    WHERE username = p_contact_name;

    IF contactid IS NULL THEN
        RAISE NOTICE 'Contact not found.';
        RETURN;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES(contactid, p_phone, p_type);

END;
$$;


-- ===========================================
-- Procedure 2: Move Contact To Group

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    groupid INTEGER;
BEGIN

    SELECT id
    INTO groupid
    FROM groups
    WHERE name = p_group_name;

    IF groupid IS NULL THEN

        INSERT INTO groups(name)
        VALUES(p_group_name);

        SELECT id
        INTO groupid
        FROM groups
        WHERE name = p_group_name;

    END IF;

    UPDATE contacts
    SET group_id = groupid
    WHERE username = p_contact_name;

END;
$$;


-- ===========================================
-- Function: Search Contacts

CREATE OR REPLACE FUNCTION search_contacts(
    p_query TEXT
)

RETURNS TABLE(
    username VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)

LANGUAGE plpgsql

AS
$$

BEGIN

RETURN QUERY

SELECT
    c.username,
    c.email,
    c.birthday,
    g.name,
    p.phone,
    p.type

FROM contacts c

LEFT JOIN groups g
ON c.group_id = g.id

LEFT JOIN phones p
ON c.id = p.contact_id

WHERE

c.username ILIKE '%' || p_query || '%'

OR

c.email ILIKE '%' || p_query || '%'

OR

p.phone ILIKE '%' || p_query || '%';

END;
$$;