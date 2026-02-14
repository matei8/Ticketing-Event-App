CREATE OR REPLACE PROCEDURE sp_raport_organizatori_soldout (
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT O.NumeCompanie, E.Titlu, SUM(OI.Cantitate) as BileteVandute
        FROM Organizers O
        JOIN Events E ON O.ID = E.ID_Organizator
        JOIN TicketTypes TT ON E.ID = TT.ID_Eveniment
        JOIN OrderItems OI ON TT.ID = OI.ID_TipBilet
        JOIN Orders Ord ON OI.ID_Comanda = Ord.ID
        WHERE Ord.StatusComanda = 'Procesata'
        GROUP BY O.NumeCompanie, E.Titlu, TT.CantitateTotala
        HAVING SUM(OI.Cantitate) >= TT.CantitateTotala;
END sp_raport_organizatori_soldout;
/