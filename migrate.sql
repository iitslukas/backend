-- Run this on the existing Render database to add the age column.
-- Open Render dashboard → your PostgreSQL → Shell, then paste this.

ALTER TABLE students ADD COLUMN IF NOT EXISTS vek INT;

UPDATE students SET vek = 17 WHERE meno = 'Peter'    AND priezvisko = 'Hruška';
UPDATE students SET vek = 18 WHERE meno = 'Jana'     AND priezvisko = 'Malá';
UPDATE students SET vek = 16 WHERE meno = 'Michal'   AND priezvisko = 'Kováč';
UPDATE students SET vek = 19 WHERE meno = 'Lucia'    AND priezvisko = 'Srnková';
UPDATE students SET vek = 17 WHERE meno = 'Marek'    AND priezvisko = 'Vysoký';
UPDATE students SET vek = 16 WHERE meno = 'Ema'      AND priezvisko = 'Biela';
UPDATE students SET vek = 18 WHERE meno = 'Dávid'    AND priezvisko = 'Čierny';
UPDATE students SET vek = 17 WHERE meno = 'Simona'   AND priezvisko = 'Veselá';
UPDATE students SET vek = 19 WHERE meno = 'Jakub'    AND priezvisko = 'Dlhý';
UPDATE students SET vek = 16 WHERE meno = 'Katarína' AND priezvisko = 'Šikovná';
