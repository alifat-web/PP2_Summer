-- function 1 Search contacts by pattern
CREATE OR REPLACE FUNCTION search_pattern(p_pattern TEXT)
RETURNS TABLE (
    id INTEGER,
    username VARCHAR(50),
    phone VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        pb.id,
        pb.username,
        pb.phone
    FROM phonebook pb
    WHERE pb.username ILIKE '%' || p_pattern || '%'
       OR pb.phone ILIKE '%' || p_pattern || '%';
END;
$$;


-- get contacts with pagination
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    id INTEGER,
    username VARCHAR(50),
    phone VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        pb.id,
        pb.username,
        pb.phone
    FROM phonebook pb
    ORDER BY pb.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$;