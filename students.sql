-- Create students table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    meno VARCHAR(50) NOT NULL,
    priezvisko VARCHAR(50) NOT NULL,
    image TEXT
);

-- Seed data
INSERT INTO students (meno, priezvisko, image) VALUES
    ('Peter',    'Hruška',   'https://image.smedata.sk/image/w450-h300/019c46d1-272d-7cf1-91ca-9cf550354985.jpg'),
    ('Jana',     'Malá',     'https://www.odzadu.sk/wp-content/uploads/2025/04/10-znakov-ze-si-dobry-clovek-750x409.jpg'),
    ('Michal',   'Kováč',    'https://www.katolickenoviny.sk/Data/2722/Cache/Images/71904e13.jpeg'),
    ('Lucia',    'Srnková',  'https://40plus.sk/wp-content/uploads/2023/03/co-je-clovek.jpg'),
    ('Marek',    'Vysoký',   'https://img.ihned.cz/attachment.php/370/77563370/OJaDlxyIMthA42kdoPLem76g9Wj8HK5V/EK27-28_59_George_Asimenos03_DNAnexus.jpg'),
    ('Ema',      'Biela',    'https://www.odzadu.sk/wp-content/uploads/2023/10/ak-robis-tychto-5-veci-nie-si-zly-clovek-750x409.jpg'),
    ('Dávid',    'Čierny',   'https://www.spinaker.sk/image/cache/catalog/MAJK%20SPIRIT_NOV%C3%9D%20%C4%8CLOVEK%202.0_CD_BACK_8586018995887-600x551.jpg'),
    ('Simona',   'Veselá',   'https://www.krasaastyl.sk/wp-content/uploads/2020/04/Kedy-je-clovek-stastny.jpg'),
    ('Jakub',    'Dlhý',     'https://www.clovek2.sk/wp-content/uploads/2024/03/Jakub-fyzio-Pezinok-clovek-682x1024.jpeg'),
    ('Katarína', 'Šikovná',  'https://www.odzadu.sk/wp-content/uploads/2023/11/kto-je-naozaj-cestny-clovek-750x409.jpg')
ON CONFLICT DO NOTHING;
