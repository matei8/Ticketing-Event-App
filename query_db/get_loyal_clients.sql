CREATE OR REPLACE PROCEDURE sp_raport_utilizatori_loiali (
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT U.Nume, U.Email, COUNT(DISTINCT E.ID_Categorie) as CategoriiDiferite, SUM(O.Total) as TotalCheltuit
        FROM Users U
        JOIN Orders O ON U.ID = O.ID_Utilizator
        JOIN OrderItems OI ON O.ID = OI.ID_Comanda
        JOIN TicketTypes TT ON OI.ID_TipBilet = TT.ID
        JOIN Events E ON TT.ID_Eveniment = E.ID
        JOIN Categories C ON E.ID_Categorie = C.ID
        WHERE O.StatusComanda = 'Procesata'
        GROUP BY U.Nume, U.Email
        HAVING COUNT(DISTINCT E.ID_Categorie) >= 3;
END sp_raport_utilizatori_loiali;
/