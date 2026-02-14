CREATE OR REPLACE PROCEDURE sp_cumpara_bilet (
    p_user_id IN NUMBER,
    p_tip_bilet_id IN NUMBER,
    p_cantitate IN NUMBER,
    p_pret IN NUMBER
) AS
    v_order_id NUMBER;
    v_capacitate_maxima NUMBER;
    v_bilete_vandute NUMBER;
BEGIN
    -- Verificam capacitatea
    SELECT CantitateTotala INTO v_capacitate_maxima FROM TicketTypes WHERE ID = p_tip_bilet_id;
    SELECT NVL(SUM(Cantitate), 0) INTO v_bilete_vandute FROM OrderItems WHERE ID_TipBilet = p_tip_bilet_id;

    IF (v_bilete_vandute + p_cantitate) > v_capacitate_maxima THEN
        RAISE_APPLICATION_ERROR(-20001, 'Sold Out! Mai sunt doar ' || (v_capacitate_maxima - v_bilete_vandute) || ' bilete.');
    END IF;

    -- Daca e loc, inseram
    INSERT INTO Orders (ID_Utilizator, DataComenzii, StatusComanda, Total)
    VALUES (p_user_id, SYSTIMESTAMP, 'Procesata', p_cantitate * p_pret)
    RETURNING ID INTO v_order_id;

    INSERT INTO OrderItems (ID_Comanda, ID_TipBilet, Cantitate, PretLaCumparare)
    VALUES (v_order_id, p_tip_bilet_id, p_cantitate, p_pret);

    COMMIT;
END sp_cumpara_bilet;
/