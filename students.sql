-- Create students table
CREATE TABLE IF NOT EXISTS students (
    id         SERIAL PRIMARY KEY,
    meno       VARCHAR(50) NOT NULL,
    priezvisko VARCHAR(50) NOT NULL,
    image      TEXT,
    vek        INT
);

-- Seed data
INSERT INTO students (meno, priezvisko, image, vek) VALUES
    ('Peter',    'Hruška',   'https://image.smedata.sk/image/w450-h300/019c46d1-272d-7cf1-91ca-9cf550354985.jpg',                                                                    17),
    ('Jana',     'Malá',     'https://www.odzadu.sk/wp-content/uploads/2025/04/10-znakov-ze-si-dobry-clovek-750x409.jpg',                                                            18),
    ('Michal',   'Kováč',    'https://www.katolickenoviny.sk/Data/2722/Cache/Images/71904e13.jpeg',                                                                                   16),
    ('Lucia',    'Srnková',  'https://40plus.sk/wp-content/uploads/2023/03/co-je-clovek.jpg',                                                                                        19),
    ('Marek',    'Vysoký',   'https://img.ihned.cz/attachment.php/370/77563370/OJaDlxyIMthA42kdoPLem76g9Wj8HK5V/EK27-28_59_George_Asimenos03_DNAnexus.jpg',                         17),
    ('Ema',      'Biela',    'https://www.odzadu.sk/wp-content/uploads/2023/10/ak-robis-tychto-5-veci-nie-si-zly-clovek-750x409.jpg',                                               16),
    ('Dávid',    'Čierny',   'https://www.spinaker.sk/image/cache/catalog/MAJK%20SPIRIT_NOV%C3%9D%20%C4%8CLOVEK%202.0_CD_BACK_8586018995887-600x551.jpg',                           18),
    ('Simona',   'Veselá',   'https://www.krasaastyl.sk/wp-content/uploads/2020/04/Kedy-je-clovek-stastny.jpg',                                                                     17),
    ('Jakub',    'Dlhý',     'https://www.clovek2.sk/wp-content/uploads/2024/03/Jakub-fyzio-Pezinok-clovek-682x1024.jpeg',                                                          19),
    ('Katarína', 'Šikovná',  'https://www.odzadu.sk/wp-content/uploads/2023/11/kto-je-naozaj-cestny-clovek-750x409.jpg',                                                            16)
ON CONFLICT DO NOTHING;
