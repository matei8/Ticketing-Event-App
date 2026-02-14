CREATE OR REPLACE PROCEDURE sp_get_remaining_tickets (
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT
            V.Oras,
            E.Titlu,
            TT.NumeTip,
            TT.Pret,
            (TT.CantitateTotala - NVL((SELECT SUM(Cantitate)
                                       FROM OrderItems
                                       WHERE ID_TipBilet = TT.ID), 0)) as BileteRamase
        FROM TicketTypes TT
        JOIN Events E ON TT.ID_Eveniment = E.ID
        JOIN Venues V ON E.ID_Locatie = V.ID
        ORDER BY V.Oras, E.Titlu;
END sp_get_remaining_tickets;
/