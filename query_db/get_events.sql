CREATE OR REPLACE PROCEDURE sp_get_all_events (
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT E.ID, E.Titlu, E.DataEveniment, V.Nume as Locatie, C.NumeCategorie
        FROM Events E
        JOIN Venues V ON E.ID_Locatie = V.ID
        JOIN Categories C ON E.ID_Categorie = C.ID
        ORDER BY E.DataEveniment ASC;
END sp_get_all_events;
/