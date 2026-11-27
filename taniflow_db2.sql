CREATE TABLE Petani(
id_petani INTEGER PRIMARY KEY,
nama_petani VARCHAR(100) NOT NULL,
no_telepon VARCHAR(15) NOT NULL UNIQUE,
nama_jalan VARCHAR(100) NOT NULL,
nomor_rumah VARCHAR(10),
rt VARCHAR(3),
rw VARCHAR(3),
kelurahan VARCHAR(50) NOT NULL,
kecamatan VARCHAR(50) NOT NULL,
kota VARCHAR(50) NOT NULL,
kode_pos VARCHAR(10),
password VARCHAR(255) NOT NULL
);

CREATE TABLE Pembeli(
id_pembeli INTEGER PRIMARY KEY,
nama_pembeli VARCHAR(100) NOT NULL,
no_telepon VARCHAR(15) NOT NULL UNIQUE,
password VARCHAR(255) NOT NULL
);

CREATE TABLE Admin(
id_Admin INTEGER PRIMARY KEY,
no_telepon VARCHAR(15) NOT NULL UNIQUE,
password VARCHAR(255) NOT NULL,
nama_admin VARCHAR(100) NOT NULL
);

CREATE TABLE Kategori_Produk(
id_kategori INTEGER PRIMARY KEY,
nama_kategori VARCHAR(50) NOT NULL,
deskripsi TEXT
);

CREATE TABLE Produk(
id_produk INTEGER PRIMARY KEY,
nama_produk VARCHAR(100) NOT NULL,
satuan VARCHAR(20) NOT NULL,
harga_jual NUMERIC(10,2) NOT NULL,
stok NUMERIC(10,2) NOT NULL,
Admin_id_Admin INTEGER NOT NULL,
Kategori_Produk_id_kategori INTEGER NOT NULL,
FOREIGN KEY (Admin_id_Admin)
    REFERENCES Admin(id_admin),
FOREIGN KEY (Kategori_Produk_id_kategori)
    REFERENCES Kategori_Produk(id_kategori)
);

CREATE TYPE status_pengajuan_enum AS ENUM (
    'Menunggu',
    'Disetujui',
    'Ditolak',
    'Diterima'
);

CREATE TABLE pengajuan_panen (
    id_pengajuan INTEGER PRIMARY KEY,
    tanggal_pengajuan DATE NOT NULL,
    status_pengajuan status_pengajuan_enum NOT NULL,
    catatan TEXT,
    petani_id_petani INTEGER NOT NULL,
    admin_id_admin INTEGER NOT NULL,

    FOREIGN KEY (petani_id_petani)
        REFERENCES petani(id_petani),

    FOREIGN KEY (admin_id_admin)
        REFERENCES admin(id_admin)
);

CREATE TABLE hasil_panen (
id_hasil INTEGER PRIMARY KEY,
tanggal_penerimaan DATE NOT NULL,
jumlah_panen NUMERIC(10,2) NOT NULL,
harga_beli NUMERIC(10,2) NOT NULL,
produk_id_produk INTEGER NOT NULL,
pengajuan_panen_id_pengajuan INTEGER NOT NULL,
FOREIGN KEY (produk_id_produk)
    REFERENCES produk(id_produk),
FOREIGN KEY (pengajuan_panen_id_pengajuan)
    REFERENCES pengajuan_panen(id_pengajuan)
);

CREATE TYPE metode_pembayaran_enum AS ENUM (
    'Tunai',
    'Transfer'
);

CREATE TYPE status_pembayaran_enum AS ENUM (
    'Belum Dibayar',
    'Diproses',
    'Sudah Dibayar',
    'Dibatalkan'
);

CREATE TABLE transaksi (
id_transaksi INTEGER PRIMARY KEY,
tanggal_transaksi DATE NOT NULL,
total_harga NUMERIC(12,2) NOT NULL,
pembeli_id_pembeli INTEGER NOT NULL,
tanggal_pembayaran DATE,
metode_pembayaran metode_pembayaran_enum,
status_pembayaran status_pembayaran_enum NOT NULL,
admin_id_admin INTEGER NOT NULL, 
FOREIGN KEY (pembeli_id_pembeli)
    REFERENCES pembeli(id_pembeli),
FOREIGN KEY (admin_id_admin)
    REFERENCES admin(id_admin)
);

CREATE TABLE detail_transaksi (
id_detail INTEGER PRIMARY KEY,
jumlah NUMERIC(10,2) NOT NULl,
harga_satuan NUMERIC(10,2) NOT NULL,
transaksi_id_transaksi INTEGER NOT NULL,
produk_id_produk INTEGER NOT NULL,
FOREIGN KEY (transaksi_id_transaksi)
    REFERENCES transaksi(id_transaksi),
FOREIGN KEY (produk_id_produk)
    REFERENCES produk(id_produk)
);

-- 1. ADMIN
INSERT INTO admin
(id_admin, no_telepon, password, nama_admin)
VALUES
(1, '085733509529', 'admin1', 'Nadia Azzahra'),
(2, '089516057776', 'admin2', 'Azzahra Baqiyatush Shaliha'),
(3, '082132616767', 'admin3', 'Muhammad Fashlul Islam');


-- 2. PETANI
INSERT INTO petani
(id_petani, nama_petani, no_telepon, nama_jalan, nomor_rumah,
rt, rw, kelurahan, kecamatan, kota, kode_pos, password)
VALUES
(1, 'Budi Santoso', '081234561001', 'Jl. Melati', '10', '001', '002', 'Sumberrejo', 'Ambulu', 'Jember', '68172', 'petani001'),
(2, 'Slamet Riyadi', '081234561002', 'Jl. Mawar', '12', '002', '001', 'Tegalsari', 'Ambulu', 'Jember', '68172', 'petani002'),
(3, 'Wati Lestari', '081234561003', 'Jl. Kenanga', '15', '003', '002', 'Karanganyar', 'Ambulu', 'Jember', '68172', 'petani003'),
(4, 'Suyanto', '081234561004', 'Jl. Anggrek', '08', '001', '003', 'Andongsari', 'Ambulu', 'Jember', '68172', 'petani004'),
(5, 'Siti Aminah', '081234561005', 'Jl. Flamboyan', '21', '002', '003', 'Pontang', 'Ambulu', 'Jember', '68172', 'petani005'),
(6, 'Agus Setiawan', '081234561006', 'Jl. Durian', '17', '003', '001', 'Sabrang', 'Ambulu', 'Jember', '68172', 'petani006'),
(7, 'Joko Susilo', '081234561007', 'Jl. Mangga', '09', '001', '001', 'Tanjungrejo', 'Wuluhan', 'Jember', '68162', 'petani007'),
(8, 'Dewi Anggraini', '081234561008', 'Jl. Pepaya', '14', '002', '002', 'Kesilir', 'Wuluhan', 'Jember', '68162', 'petani008');


-- 3. PEMBELI
INSERT INTO pembeli
(id_pembeli, nama_pembeli, no_telepon, password)
VALUES
(1, 'Novita Anggraeni', '082330147438', 'pembeli001'),
(2, 'Maya Putri', '081234562002', 'pembeli002'),
(3, 'Rizky Firmansyah', '081234562003', 'pembeli003'),
(4, 'Lina Marlina', '081234562004', 'pembeli004'),
(5, 'Fajar Nugroho', '081234562005', 'pembeli005'),
(6, 'Dina Safitri', '081234562006', 'pembeli006'),
(7, 'Rudi Hartono', '081234562007', 'pembeli007'),
(8, 'Nadia Permata', '081234562008', 'pembeli008');


-- 4. KATEGORI PRODUK
INSERT INTO kategori_produk
(id_kategori, nama_kategori, deskripsi)
VALUES
(1, 'Sayuran', 'Produk hasil panen berupa sayuran'),
(2, 'Buah-buahan', 'Produk hasil panen berupa buah'),
(3, 'Umbi-umbian', 'Produk hasil panen berupa umbi'),
(4, 'Biji-bijian', 'Produk hasil panen berupa biji-bijian'),
(5, 'Rempah-rempah', 'Produk hasil panen berupa rempah');


-- 5. PRODUK
INSERT INTO produk
(id_produk, nama_produk, satuan, harga_jual, stok, admin_id_admin, kategori_produk_id_kategori)
VALUES
(1, 'Bayam', 'Ikat', 3000, 100, 1, 1),
(2, 'Kangkung', 'Ikat', 2500, 120, 1, 1),
(3, 'Sawi Hijau', 'Kg', 6000, 80, 1, 1),
(4, 'Wortel', 'Kg', 10000, 75, 2, 1),
(5, 'Tomat', 'Kg', 8000, 90, 2, 1),
(6, 'Cabai Merah', 'Kg', 30000, 50, 2, 1),
(7, 'Kentang', 'Kg', 14000, 100, 3, 3),
(8, 'Singkong', 'Kg', 5000, 110, 3, 3);


-- 6. PENGAJUAN PANEN
INSERT INTO pengajuan_panen
(id_pengajuan, tanggal_pengajuan, status_pengajuan,
catatan, petani_id_petani, admin_id_admin)
VALUES
(1, '2026-11-01', 'Disetujui', 'Pengajuan panen bayam', 1, 1),
(2, '2026-11-02', 'Diterima', 'Pengajuan panen kangkung', 2, 1),
(3, '2026-11-03', 'Disetujui', 'Pengajuan panen tomat', 3, 2),
(4, '2026-11-04', 'Diterima', 'Pengajuan panen wortel', 4, 2),
(5, '2026-11-05', 'Menunggu', 'Pengajuan panen cabai merah', 5, 1),
(6, '2026-11-06', 'Disetujui', 'Pengajuan panen kentang', 6, 3),
(7, '2026-11-07', 'Diterima', 'Pengajuan panen singkong', 7, 3),
(8, '2026-11-08', 'Ditolak', 'Kualitas hasil panen belum sesuai', 8, 1);


-- 7. HASIL PANEN
INSERT INTO hasil_panen
(id_hasil, tanggal_penerimaan, jumlah_panen, harga_beli,
produk_id_produk, pengajuan_panen_id_pengajuan)
VALUES
(1, '2026-11-03', 48, 2000, 1, 1),
(2, '2026-11-04', 40, 1500, 2, 2),
(3, '2026-11-05', 58, 6000, 5, 3),
(4, '2026-11-06', 35, 7500, 4, 4),
(5, '2026-11-08', 68, 10000, 7, 6),
(6, '2026-11-09', 54, 3500, 8, 7);


-- 8. TRANSAKSI
INSERT INTO transaksi
(id_transaksi, tanggal_transaksi, total_harga, pembeli_id_pembeli,
tanggal_pembayaran, metode_pembayaran, status_pembayaran, admin_id_admin)
VALUES
(1, '2026-11-05', 15000, 1, '2026-11-05', 'Tunai', 'Sudah Dibayar', 1),
(2, '2026-11-06', 20000, 2, '2026-11-06', 'Transfer', 'Sudah Dibayar', 1),
(3, '2026-11-07', 24000, 3, '2026-11-07', 'Tunai', 'Sudah Dibayar', 2),
(4, '2026-11-08', 28000, 4, NULL, 'Transfer', 'Belum Dibayar', 2),
(5, '2026-11-09', 36000, 5, '2026-11-09', 'Tunai', 'Sudah Dibayar', 2),
(6, '2026-11-10', 14000, 6, '2026-11-10', 'Transfer', 'Sudah Dibayar', 3),
(7, '2026-11-11', 25000, 7, NULL, 'Transfer', 'Diproses', 3),
(8, '2026-11-12', 18000, 8, '2026-11-12', 'Tunai', 'Sudah Dibayar', 1);


-- 9. DETAIL TRANSAKSI
INSERT INTO detail_transaksi
(id_detail, jumlah, harga_satuan, transaksi_id_transaksi, produk_id_produk)
VALUES
(1, 5, 3000, 1, 1),
(2, 8, 2500, 2, 2),
(3, 4, 6000, 3, 3),
(4, 2, 10000, 4, 4),
(5, 1, 8000, 4, 5),
(6, 3, 12000, 5, 7),
(7, 2, 7000, 6, 3),
(8, 1, 25000, 7, 6),
(9, 1, 18000, 8, 5);

SELECT * FROM hasil_panen;
TRUNCATE TABLE petani RESTART IDENTITY CASCADE;
SELECT * FROM petani WHERE id_petani = 1;

SELECT * FROM petani;

TRUNCATE TABLE
detail_transaksi,
transaksi,
hasil_panen,
pengajuan_panen,
produk,
kategori_produk,
pembeli,
petani,
admin
RESTART IDENTITY CASCADE;