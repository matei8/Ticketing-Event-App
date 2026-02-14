CREATE OR REPLACE PROCEDURE sp_raport_vanzari_oras (
    p_oras IN VARCHAR2,
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT C.NumeCategorie, SUM(OI.Cantitate * OI.PretLaCumparare) as VenitTotal
        FROM Categories C
        JOIN Events E ON C.ID = E.ID_Categorie
        JOIN Venues V ON E.ID_Locatie = V.ID
        JOIN TicketTypes TT ON E.ID = TT.ID_Eveniment
        JOIN OrderItems OI ON TT.ID = OI.ID_TipBilet
        WHERE V.Oras = p_oras
        GROUP BY C.NumeCategorie;
END sp_raport_vanzari_oras;
/