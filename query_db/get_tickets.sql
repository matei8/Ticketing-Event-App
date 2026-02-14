CREATE OR REPLACE PROCEDURE sp_get_tickets_lookup (
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT TT.ID, E.Titlu || ' - ' || TT.NumeTip || ' (' || TT.Pret || ' RON)' as Info
        FROM TicketTypes TT
        JOIN Events E ON TT.ID_Eveniment = E.ID
        ORDER BY E.Titlu;
END sp_get_tickets_lookup;
/