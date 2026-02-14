CREATE OR REPLACE PROCEDURE sp_get_distinct_cities (
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT DISTINCT Oras FROM Venues ORDER BY Oras;
END sp_get_distinct_cities;
/