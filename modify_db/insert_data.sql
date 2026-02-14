-- CURATARE TOTALA
DELETE FROM OrderItems;
DELETE FROM TicketTypes;
DELETE FROM Orders;
DELETE FROM Events;
DELETE FROM Categories;
DELETE FROM Venues;
DELETE FROM Organizers;
DELETE FROM Users;
COMMIT;

-- 1. UTILIZATORI
INSERT INTO Users (ID, Nume, Email, ParolaHash) VALUES (1, 'Ion Popescu', 'ion.popescu@gmail.com', 'h1');
INSERT INTO Users (ID, Nume, Email, ParolaHash) VALUES (2, 'Maria Ionescu', 'maria.i@yahoo.com', 'h2');
INSERT INTO Users (ID, Nume, Email, ParolaHash) VALUES (3, 'Andrei Vlad', 'vlad.andrei@outlook.com', 'h3');
INSERT INTO Users (ID, Nume, Email, ParolaHash) VALUES (4, 'Elena Radu', 'elena_r@gmail.com', 'h4');
INSERT INTO Users (ID, Nume, Email, ParolaHash) VALUES (5, 'Mihai Enache', 'mihai_e@info.ro', 'h5');

-- 2. CATEGORII
INSERT INTO Categories (ID, NumeCategorie) VALUES (1, 'Muzica');
INSERT INTO Categories (ID, NumeCategorie) VALUES (2, 'Teatru');
INSERT INTO Categories (ID, NumeCategorie) VALUES (3, 'Tehnologie');
INSERT INTO Categories (ID, NumeCategorie) VALUES (4, 'Sport');

-- 3. ORGANIZATORI
INSERT INTO Organizers (ID, NumeCompanie, CUI, ContactEmail) VALUES (1, 'Emagic Entertainment', 'RO1', 'office@emagic.ro');
INSERT INTO Organizers (ID, NumeCompanie, CUI, ContactEmail) VALUES (2, 'ARTmania Events', 'RO2', 'contact@artmania.ro');
INSERT INTO Organizers (ID, NumeCompanie, CUI, ContactEmail) VALUES (3, 'Events & More', 'RO3', 'office@events.ro');

-- 4. LOCATII
INSERT INTO Venues (ID, Nume, Adresa, Oras, CapacitateMaxima) VALUES (1, 'Arena Nationala', 'Bucuresti', 'Bucuresti', 55000);
INSERT INTO Venues (ID, Nume, Adresa, Oras, CapacitateMaxima) VALUES (2, 'Sala Polivalenta Cluj', 'Cluj', 'Cluj-Napoca', 10000);
INSERT INTO Venues (ID, Nume, Adresa, Oras, CapacitateMaxima) VALUES (3, 'Iulius Congress Hall', 'Timisoara', 'Timisoara', 2000);
INSERT INTO Venues (ID, Nume, Adresa, Oras, CapacitateMaxima) VALUES (4, 'Teatrul National Iasi', 'Iasi', 'Iasi', 800);
INSERT INTO Venues (ID, Nume, Adresa, Oras, CapacitateMaxima) VALUES (5, 'Centrul Cultural Brasov', 'Brasov', 'Brasov', 1500);
INSERT INTO Venues (ID, Nume, Adresa, Oras, CapacitateMaxima) VALUES (6, 'Faleza Constanta', 'Constanta', 'Constanta', 5000);

-- 5. EVENIMENTE
BEGIN
  FOR v_id IN 1..6 LOOP
    FOR cat_id IN 1..4 LOOP
      INSERT INTO Events (ID, Titlu, Descriere, DataEveniment, ID_Locatie, ID_Organizator, ID_Categorie)
      VALUES (
        (v_id - 1) * 4 + cat_id,
        'Eveniment ' || cat_id || ' in ' || v_id,
        'Descriere eveniment',
        SYSTIMESTAMP + INTERVAL '30' DAY,
        v_id,
        MOD(cat_id, 3) + 1,
        cat_id
      );
    END LOOP;
  END LOOP;
END;
/

BEGIN
    FOR rec IN (
        SELECT E.ID, C.NumeCategorie, V.Oras
        FROM Events E
        JOIN Categories C ON E.ID_Categorie = C.ID
        JOIN Venues V ON E.ID_Locatie = V.ID
    )
    LOOP
        UPDATE Events
        SET Titlu = rec.NumeCategorie || ' în ' || rec.Oras
        WHERE ID = rec.ID;
    END LOOP;
    COMMIT;
END;
/

-- 6. TIPURI DE BILETE
BEGIN
  FOR e_id IN 1..24 LOOP
    INSERT INTO TicketTypes (ID, ID_Eveniment, NumeTip, Pret, CantitateTotala)
    VALUES (e_id, e_id, 'Standard', 100 + MOD(e_id, 5) * 50, 500);
  END LOOP;
END;
/

-- 7. SIMULARE VANZARI PENTRU RAPOARTE
INSERT INTO Orders (ID, ID_Utilizator, Total) VALUES (1, 1, 1000);
INSERT INTO OrderItems (ID_Comanda, ID_TipBilet, Cantitate, PretLaCumparare) VALUES (1, 1, 2, 150); -- Bucuresti Muzica
INSERT INTO OrderItems (ID_Comanda, ID_TipBilet, Cantitate, PretLaCumparare) VALUES (1, 2, 2, 100); -- Bucuresti Teatru
INSERT INTO OrderItems (ID_Comanda, ID_TipBilet, Cantitate, PretLaCumparare) VALUES (1, 3, 2, 200); -- Bucuresti Tech

INSERT INTO Orders (ID, ID_Utilizator, Total) VALUES (2, 2, 500);
INSERT INTO OrderItems (ID_Comanda, ID_TipBilet, Cantitate, PretLaCumparare) VALUES (2, 5, 2, 150); -- Cluj Muzica
INSERT INTO OrderItems (ID_Comanda, ID_TipBilet, Cantitate, PretLaCumparare) VALUES (2, 13, 2, 100); -- Iasi Muzica

COMMIT;