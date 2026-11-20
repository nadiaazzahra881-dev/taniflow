from koneksi import buka_koneksi
import psycopg2


# =====================================
# 1. DASHBOARD ADMIN
# =====================================

def dashboard():
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM petani")
        jumlah_petani = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM produk")
        jumlah_produk = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(stok), 0) FROM produk")
        jumlah_stok = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM hasil_panen")
        jumlah_hasil_panen = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM transaksi")
        jumlah_transaksi = cursor.fetchone()[0]

        print("\n========== DASHBOARD ADMIN ==========")
        print("Jumlah Petani      :", jumlah_petani)
        print("Jumlah Produk      :", jumlah_produk)
        print("Jumlah Stok        :", jumlah_stok)
        print("Jumlah Hasil Panen :", jumlah_hasil_panen)
        print("Jumlah Transaksi   :", jumlah_transaksi)

    except psycopg2.Error as error:
        print("Gagal menampilkan dashboard:", error)

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# 2. KELOLA DATA PETANI
# =====================================

def lihat_petani(cursor):
    cursor.execute("""
        SELECT id_petani, nama_petani, no_telepon,
               nama_jalan, nomor_rumah, rt, rw,
               kelurahan, kecamatan, kota, kode_pos
        FROM petani
        ORDER BY id_petani
    """)

    data = cursor.fetchall()

    print("\n========== DATA PETANI ==========")

    if len(data) == 0:
        print("Belum ada data petani.")

    else:
        for petani in data:
            print("\nID Petani   :", petani[0])
            print("Nama        :", petani[1])
            print("No Telepon  :", petani[2])
            print("Jalan       :", petani[3])
            print("Nomor Rumah :", petani[4])
            print("RT/RW       :", petani[5], "/", petani[6])
            print("Kelurahan   :", petani[7])
            print("Kecamatan   :", petani[8])
            print("Kota        :", petani[9])
            print("Kode Pos    :", petani[10])


def tambah_petani():
    print("\n========== TAMBAH PETANI ==========")

    nama = input("Nama petani: ")
    no_telepon = input("Nomor telepon: ")
    nama_jalan = input("Nama jalan: ")
    nomor_rumah = input("Nomor rumah: ")
    rt = input("RT: ")
    rw = input("RW: ")
    kelurahan = input("Kelurahan: ")
    kecamatan = input("Kecamatan: ")
    kota = input("Kota: ")
    kode_pos = input("Kode pos: ")
    password = input("Password: ")

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT COALESCE(MAX(id_petani), 0) + 1
            FROM petani
        """)

        id_baru = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO petani (
                id_petani, nama_petani, no_telepon,
                nama_jalan, nomor_rumah, rt, rw,
                kelurahan, kecamatan, kota, kode_pos, password
            )
            VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
        """, (
            id_baru, nama, no_telepon,
            nama_jalan, nomor_rumah, rt, rw,
            kelurahan, kecamatan, kota, kode_pos, password
        ))

        koneksi.commit()
        print("Data petani berhasil ditambahkan!")

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Gagal menambahkan petani:", error)

    finally:
        cursor.close()
        koneksi.close()


def ubah_petani():
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        lihat_petani(cursor)

        id_petani = input("\nMasukkan ID petani yang ingin diubah: ")

        cursor.execute("""
            SELECT id_petani
            FROM petani
            WHERE id_petani = %s
        """, (id_petani,))

        if cursor.fetchone() is None:
            print("ID petani tidak ditemukan!")
            return

        print("\nMasukkan data petani yang baru.")

        nama = input("Nama petani: ")
        no_telepon = input("Nomor telepon: ")
        nama_jalan = input("Nama jalan: ")
        nomor_rumah = input("Nomor rumah: ")
        rt = input("RT: ")
        rw = input("RW: ")
        kelurahan = input("Kelurahan: ")
        kecamatan = input("Kecamatan: ")
        kota = input("Kota: ")
        kode_pos = input("Kode pos: ")
        password = input("Password baru: ")

        cursor.execute("""
            UPDATE petani
            SET nama_petani = %s,
                no_telepon = %s,
                nama_jalan = %s,
                nomor_rumah = %s,
                rt = %s,
                rw = %s,
                kelurahan = %s,
                kecamatan = %s,
                kota = %s,
                kode_pos = %s,
                password = %s
            WHERE id_petani = %s
        """, (
            nama, no_telepon, nama_jalan,
            nomor_rumah, rt, rw, kelurahan,
            kecamatan, kota, kode_pos, password, id_petani
        ))

        koneksi.commit()
        print("Data petani berhasil diubah!")

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Gagal mengubah data petani:", error)

    finally:
        cursor.close()
        koneksi.close()


def hapus_petani():
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        lihat_petani(cursor)

        id_petani = input("\nMasukkan ID petani yang ingin dihapus: ")

        cursor.execute("""
            DELETE FROM petani
            WHERE id_petani = %s
        """, (id_petani,))

        if cursor.rowcount > 0:
            koneksi.commit()
            print("Data petani berhasil dihapus!")

        else:
            koneksi.rollback()
            print("ID petani tidak ditemukan!")

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Data petani tidak dapat dihapus.")
        print("Petani mungkin masih memiliki data pengajuan panen.")
        print(error)

    finally:
        cursor.close()
        koneksi.close()


def kelola_petani():
    while True:
        print("\n========== KELOLA DATA PETANI ==========")
        print("1. Tambah Petani")
        print("2. Lihat Petani")
        print("3. Ubah Petani")
        print("4. Hapus Petani")
        print("5. Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_petani()

        elif pilihan == "2":
            koneksi = buka_koneksi()

            if koneksi is not None:
                cursor = koneksi.cursor()
                lihat_petani(cursor)
                cursor.close()
                koneksi.close()

        elif pilihan == "3":
            ubah_petani()

        elif pilihan == "4":
            hapus_petani()

        elif pilihan == "5":
            break

        else:
            print("Pilihan tidak valid!")


# =====================================
# 3. MELIHAT PRODUK
# =====================================

def lihat_produk():
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT p.id_produk, p.nama_produk,
                   k.nama_kategori, p.satuan,
                   p.harga_jual, p.stok
            FROM produk p
            JOIN kategori_produk k
            ON p.kategori_produk_id_kategori = k.id_kategori
            ORDER BY p.id_produk
        """)

        data = cursor.fetchall()

        print("\n========== DATA PRODUK ==========")

        if len(data) == 0:
            print("Belum ada produk.")

        else:
            for produk in data:
                print("\nID Produk :", produk[0])
                print("Nama      :", produk[1])
                print("Kategori  :", produk[2])
                print("Satuan    :", produk[3])
                print("Harga     :", produk[4])
                print("Stok      :", produk[5])

    except psycopg2.Error as error:
        print("Gagal menampilkan produk:", error)

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# 4. MENGELOLA DATA PRODUK
# =====================================

def pilih_kategori(cursor):
    cursor.execute("""
        SELECT id_kategori, nama_kategori
        FROM kategori_produk
        ORDER BY id_kategori
    """)

    data = cursor.fetchall()

    print("\n========== PILIH KATEGORI ==========")

    for kategori in data:
        print(kategori[0], "-", kategori[1])

    return data


def tambah_produk(id_admin):
    print("\n========== TAMBAH PRODUK ==========")

    nama = input("Nama produk: ")
    satuan = input("Satuan produk: ")
    harga = input("Harga jual: ")
    stok = input("Stok awal: ")

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        data_kategori = pilih_kategori(cursor)

        if len(data_kategori) == 0:
            print("Belum ada kategori produk!")
            return

        id_kategori = input("Masukkan ID kategori: ")

        cursor.execute("""
            SELECT COALESCE(MAX(id_produk), 0) + 1
            FROM produk
        """)

        id_baru = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO produk (
                id_produk, nama_produk, satuan,
                harga_jual, stok, admin_id_admin,
                kategori_produk_id_kategori
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            id_baru, nama, satuan, harga,
            stok, id_admin, id_kategori
        ))

        koneksi.commit()
        print("Produk berhasil ditambahkan!")

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Gagal menambahkan produk:", error)

    finally:
        cursor.close()
        koneksi.close()


def ubah_produk():
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT id_produk, nama_produk
            FROM produk
            ORDER BY id_produk
        """)

        data = cursor.fetchall()

        print("\n========== DATA PRODUK ==========")

        for produk in data:
            print(produk[0], "-", produk[1])

        id_produk = input("\nMasukkan ID produk: ")

        cursor.execute("""
            SELECT id_produk
            FROM produk
            WHERE id_produk = %s
        """, (id_produk,))

        if cursor.fetchone() is None:
            print("ID produk tidak ditemukan!")
            return

        nama = input("Nama produk baru: ")
        satuan = input("Satuan baru: ")
        harga = input("Harga jual baru: ")
        stok = input("Stok baru: ")

        data_kategori = pilih_kategori(cursor)

        if len(data_kategori) == 0:
            print("Belum ada kategori produk!")
            return

        id_kategori = input("Masukkan ID kategori baru: ")

        cursor.execute("""
            UPDATE produk
            SET nama_produk = %s,
                satuan = %s,
                harga_jual = %s,
                stok = %s,
                kategori_produk_id_kategori = %s
            WHERE id_produk = %s
        """, (
            nama, satuan, harga, stok,
            id_kategori, id_produk
        ))

        koneksi.commit()
        print("Produk berhasil diubah!")

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Gagal mengubah produk:", error)

    finally:
        cursor.close()
        koneksi.close()


def hapus_produk():
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT id_produk, nama_produk
            FROM produk
            ORDER BY id_produk
        """)

        data = cursor.fetchall()

        print("\n========== DATA PRODUK ==========")

        for produk in data:
            print(produk[0], "-", produk[1])

        id_produk = input("\nMasukkan ID produk yang ingin dihapus: ")

        cursor.execute("""
            DELETE FROM produk
            WHERE id_produk = %s
        """, (id_produk,))

        if cursor.rowcount > 0:
            koneksi.commit()
            print("Produk berhasil dihapus!")

        else:
            koneksi.rollback()
            print("ID produk tidak ditemukan!")

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Produk tidak dapat dihapus karena mungkin masih digunakan.")
        print(error)

    finally:
        cursor.close()
        koneksi.close()


def menu_produk(id_admin):
    while True:
        print("\n========== KELOLA PRODUK ==========")
        print("1. Tambah Produk")
        print("2. Ubah Produk")
        print("3. Hapus Produk")
        print("4. Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_produk(id_admin)

        elif pilihan == "2":
            ubah_produk()

        elif pilihan == "3":
            hapus_produk()

        elif pilihan == "4":
            break

        else:
            print("Pilihan tidak valid!")


# =====================================
# 5. MEMERIKSA KETERSEDIAAN STOK
# =====================================

def lihat_stok():
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT id_produk, nama_produk, satuan, stok
            FROM produk
            ORDER BY nama_produk
        """)

        data = cursor.fetchall()

        print("\n========== KETERSEDIAAN STOK ==========")

        for produk in data:
            print("\nID Produk :", produk[0])
            print("Nama      :", produk[1])
            print("Satuan    :", produk[2])
            print("Stok      :", produk[3])

            if produk[3] <= 0:
                print("Status    : Stok habis")
            else:
                print("Status    : Tersedia")

    except psycopg2.Error as error:
        print("Gagal memeriksa stok:", error)

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# 6. MELIHAT DATA HASIL PANEN
# =====================================

def lihat_hasil_panen():
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT h.id_hasil,
                   pet.nama_petani,
                   p.nama_produk,
                   h.tanggal_penerimaan,
                   h.jumlah_panen,
                   h.harga_beli
            FROM hasil_panen h
            JOIN pengajuan_panen pg
                ON h.pengajuan_panen_id_pengajuan = pg.id_pengajuan
            JOIN petani pet
                ON pg.petani_id_petani = pet.id_petani
            JOIN produk p
                ON h.produk_id_produk = p.id_produk
            ORDER BY h.tanggal_penerimaan DESC
        """)

        data = cursor.fetchall()

        print("\n========== DATA HASIL PANEN ==========")

        if len(data) == 0:
            print("Belum ada data hasil panen.")

        else:
            for hasil in data:
                print("\nID Hasil       :", hasil[0])
                print("Nama Petani    :", hasil[1])
                print("Produk         :", hasil[2])
                print("Tanggal Terima :", hasil[3])
                print("Jumlah Panen   :", hasil[4])
                print("Harga Beli     :", hasil[5])

    except psycopg2.Error as error:
        print("Gagal menampilkan hasil panen:", error)

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# 7. MENCATAT PENERIMAAN HASIL PANEN
# =====================================

def terima_hasil_panen(id_admin):
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT pg.id_pengajuan,
                   pet.nama_petani,
                   pg.jumlah_diajukan,
                   pg.status_pengajuan
            FROM pengajuan_panen pg
            JOIN petani pet
                ON pg.petani_id_petani = pet.id_petani
            WHERE pg.status_pengajuan = 'Disetujui'
              AND NOT EXISTS (
                  SELECT 1
                  FROM hasil_panen h
                  WHERE h.pengajuan_panen_id_pengajuan = pg.id_pengajuan
              )
            ORDER BY pg.id_pengajuan
        """)

        data = cursor.fetchall()

        print("\n========== PENGAJUAN PANEN DISETUJUI ==========")

        if len(data) == 0:
            print("Tidak ada pengajuan yang siap diterima.")
            return

        for pengajuan in data:
            print("\nID Pengajuan :", pengajuan[0])
            print("Nama Petani  :", pengajuan[1])
            print("Jumlah Ajukan:", pengajuan[2])
            print("Status       :", pengajuan[3])

        id_pengajuan = input("\nMasukkan ID pengajuan yang diterima: ")

        cursor.execute("""
            SELECT jumlah_diajukan
            FROM pengajuan_panen
            WHERE id_pengajuan = %s
              AND status_pengajuan = 'Disetujui'
              AND NOT EXISTS (
                  SELECT 1
                  FROM hasil_panen
                  WHERE pengajuan_panen_id_pengajuan = %s
              )
        """, (id_pengajuan, id_pengajuan))

        pengajuan = cursor.fetchone()

        if pengajuan is None:
            print("Pengajuan tidak ditemukan atau sudah diterima!")
            return

        jumlah_diajukan = pengajuan[0]

        cursor.execute("""
            SELECT id_produk, nama_produk, satuan
            FROM produk
            ORDER BY id_produk
        """)

        data_produk = cursor.fetchall()

        print("\n========== DAFTAR PRODUK ==========")

        for produk in data_produk:
            print(produk[0], "-", produk[1], "-", produk[2])

        id_produk = input("Masukkan ID produk hasil panen: ")
        jumlah = input("Jumlah panen yang diterima: ")
        harga_beli = input("Harga beli per satuan: ")

        cursor.execute("""
            SELECT id_produk
            FROM produk
            WHERE id_produk = %s
        """, (id_produk,))

        if cursor.fetchone() is None:
            print("Produk tidak ditemukan!")
            return

        cursor.execute("""
            SELECT COALESCE(MAX(id_hasil), 0) + 1
            FROM hasil_panen
        """)

        id_hasil = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO hasil_panen (
                id_hasil,
                tanggal_penerimaan,
                jumlah_panen,
                harga_beli,
                produk_id_produk,
                pengajuan_panen_id_pengajuan
            )
            VALUES (
                %s, CURRENT_DATE, %s, %s, %s, %s
            )
        """, (
            id_hasil,
            jumlah,
            harga_beli,
            id_produk,
            id_pengajuan
        ))

        cursor.execute("""
            UPDATE produk
            SET stok = stok + %s
            WHERE id_produk = %s
        """, (jumlah, id_produk))

        koneksi.commit()

        print("\nPenerimaan hasil panen berhasil dicatat!")
        print("Jumlah pengajuan:", jumlah_diajukan)
        print("ID hasil panen:", id_hasil)

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Gagal mencatat penerimaan panen:", error)

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# 8. MELIHAT DATA TRANSAKSI
# =====================================

def lihat_transaksi():
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT t.id_transaksi,
                   p.nama_pembeli,
                   t.tanggal_transaksi,
                   t.total_harga,
                   t.status_pembayaran
            FROM transaksi t
            JOIN pembeli p
                ON t.pembeli_id_pembeli = p.id_pembeli
            ORDER BY t.tanggal_transaksi DESC
        """)

        data = cursor.fetchall()

        print("\n========== DATA TRANSAKSI ==========")

        if len(data) == 0:
            print("Belum ada transaksi.")

        else:
            for transaksi in data:
                print("\nID Transaksi :", transaksi[0])
                print("Nama Pembeli :", transaksi[1])
                print("Tanggal      :", transaksi[2])
                print("Total Harga  :", transaksi[3])
                print("Status Bayar :", transaksi[4])

                cursor.execute("""
                    SELECT p.nama_produk,
                           d.jumlah,
                           d.harga_satuan,
                           d.jumlah * d.harga_satuan
                    FROM detail_transaksi d
                    JOIN produk p
                        ON d.produk_id_produk = p.id_produk
                    WHERE d.transaksi_id_transaksi = %s
                """, (transaksi[0],))

                detail = cursor.fetchall()

                print("Detail Produk:")

                for item in detail:
                    print(
                        "-", item[0],
                        "| Jumlah:", item[1],
                        "| Harga:", item[2],
                        "| Subtotal:", item[3]
                    )

    except psycopg2.Error as error:
        print("Gagal menampilkan transaksi:", error)

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# 9. LAPORAN PENJUALAN
# =====================================

def laporan_penjualan():
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT DATE(tanggal_transaksi),
                   COUNT(id_transaksi),
                   COALESCE(SUM(total_harga), 0)
            FROM transaksi
            GROUP BY DATE(tanggal_transaksi)
            ORDER BY DATE(tanggal_transaksi) DESC
        """)

        data = cursor.fetchall()

        print("\n========== LAPORAN PENJUALAN ==========")

        if len(data) == 0:
            print("Belum ada data penjualan.")

        else:
            total_transaksi = 0
            total_penjualan = 0

            for laporan in data:
                print("\nTanggal       :", laporan[0])
                print("Jumlah Transaksi:", laporan[1])
                print("Total Penjualan :", laporan[2])

                total_transaksi = total_transaksi + laporan[1]
                total_penjualan = total_penjualan + laporan[2]

            print("\n========== TOTAL KESELURUHAN ==========")
            print("Jumlah Transaksi :", total_transaksi)
            print("Total Penjualan  :", total_penjualan)

    except psycopg2.Error as error:
        print("Gagal menampilkan laporan:", error)

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# MENU UTAMA ADMIN
# =====================================

def menu_admin(id_admin):
    while True:
        print("\n========== MENU ADMIN ==========")
        print("1. Dashboard")
        print("2. Kelola Data Petani")
        print("3. Melihat Produk")
        print("4. Mengelola Data Produk")
        print("5. Memeriksa Ketersediaan Stok")
        print("6. Melihat Data Hasil Panen")
        print("7. Mencatat Penerimaan Hasil Panen")
        print("8. Melihat Data Transaksi")
        print("9. Melihat Laporan Penjualan")
        print("10. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            dashboard()

        elif pilihan == "2":
            kelola_petani()

        elif pilihan == "3":
            lihat_produk()

        elif pilihan == "4":
            menu_produk(id_admin)

        elif pilihan == "5":
            lihat_stok()

        elif pilihan == "6":
            lihat_hasil_panen()

        elif pilihan == "7":
            terima_hasil_panen(id_admin)

        elif pilihan == "8":
            lihat_transaksi()

        elif pilihan == "9":
            laporan_penjualan()

        elif pilihan == "10":
            print("Anda berhasil logout.")
            break

        else:
            print("Pilihan tidak valid!")
