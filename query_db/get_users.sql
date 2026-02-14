CREATE OR REPLACE PROCEDURE sp_get_users_lookup (
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT ID, Nume || ' (' || Email || ')' as Info
        FROM Users
        ORDER BY Nume;
END sp_get_users_lookup;
/