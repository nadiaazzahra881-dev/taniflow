from koneksi import buka_koneksi
import psycopg2
from bantuan import clear, jeda

# =====================================
# 1. DASHBOARD ADMIN
# =====================================

def dashboard():
    clear()
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

    except psycopg2.Error:
        print("Gagal menampilkan dashboard")

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
    
    print("=" * 55)
    print("DATA PETANI")
    print("=" * 55)

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
    clear()
    print("=" * 55)
    print("TAMBAH PETANI")
    print("=" * 55)

    nama = input("  Nama petani: ").strip().title()
    if not nama:
        print("\n  [!] Nama tidak boleh kosong!")
        return
    if not all(huruf.isalpha() or huruf.isspace() for huruf in nama):
        print("\n  [!] Nama hanya boleh mengandung huruf dan spasi!")
        return

    no_telepon = input("  Nomor telepon     : ").strip()
    if not no_telepon:
        print("\n  [!] Nomor telepon tidak boleh kosong!")
        return
    if not no_telepon.isdigit():
        print("\n  [!] Nomor telepon harus berupa angka!")
        return
    if len(no_telepon) < 10 or len(no_telepon) > 13:
            print("\n  [!] Nomor telepon harus terdiri dari 10-13 digit!")
            return

    password = input("  Password          : ")
    if len(password) < 5:
        print("\n  [!] Password minimal 5 karakter!")
        return
    if any(huruf.isspace() for huruf in password):
        print("\n  [!] Password tidak boleh mengandung spasi!")
        return
    
    print("\n-Alamat")
    nama_jalan = input("  Nama jalan        : ").strip()
    nomor_rumah = input("  Nomor rumah       : ").strip()
    rt = input("  RT                : ").strip()
    rw = input("  RW                : ").strip()
    kelurahan = input("  Kelurahan         : ").strip().title()
    kecamatan = input("  Kecamatan         : ").strip().title()
    kota = input("  Kota              : ").strip().title()
    kode_pos = input("  Kode pos          : ").strip()

    if not nama_jalan:
        print("\n  [!] Nama jalan tidak boleh kosong!")
        return
    if not kelurahan or not kecamatan or not kota:
        print("\n  [!] Kelurahan, kecamatan, dan kota wajib diisi!")
        return
    if rt and not rt.isdigit():
        print("\n  [!] RT harus berupa angka!")
        return
    if rw and not rw.isdigit():
        print("\n  [!] RW harus berupa angka!")
        return
    if kode_pos and (not kode_pos.isdigit() or len(kode_pos) != 5):
        print("\n  [!] Kode pos harus terdiri dari 5 digit!")
        return

    clear()

    print("=" * 55)
    print("Konfirmasi tambah data petani")
    print("=" * 55)

    print("\nApakah Anda yakin ingin menambah petani?")
    print("1. [Ya]")
    print("2. [Tidak]")

    konfirmasi = input("Pilih konfirmasi (1/2): ").strip()

    if konfirmasi == "1":
        print("\nData akan disimpan.")

    elif konfirmasi == "2":
        print("\nPenambahan data petani dibatalkan.")
        return

    else:
        print("\n[!] Input tidak valid!")
        return
        
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

    except psycopg2.Error:
        koneksi.rollback()
        print("Gagal menambahkan petani")

    finally:
        cursor.close()
        koneksi.close()


def ubah_petani():
    clear()
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        lihat_petani(cursor)

        id_petani = input("\nMasukkan ID petani yang ingin diubah: ")
        if not id_petani:
            print("\n  [!] id_petani tidak boleh kosong!")
            return
        if id_petani.isdigit():
            cursor.execute("""
                SELECT id_petani
                FROM petani
                WHERE id_petani = %s
            """, (id_petani,))

            if cursor.fetchone() is None:
                print("\n  [!] ID petani tidak ditemukan!")
                return

        else:
            print("\n  [!] Input tidak valid!")
            return

        print("\nMasukkan data petani yang baru.")

        nama = input("  Nama petani: ").strip().title()
        if not nama:
            print("\n  [!] Nama tidak boleh kosong!")
            return
        if not all(huruf.isalpha() or huruf.isspace() for huruf in nama):
            print("\n  [!] Nama hanya boleh mengandung huruf dan spasi!")
            return
        if not no_telepon.isdigit():
            print("\n  [!] Nomor telepon harus berupa angka!")
            return
    
        no_telepon = input("  Nomor telepon     : ").strip()
        if not no_telepon:
            print("\n  [!] Nomor telepon tidak boleh kosong!")
            return
        if not no_telepon.isdigit():
            print("\n  [!] Nomor telepon harus berupa angka!")
            return
        if len(no_telepon) < 10 or len(no_telepon) > 13:
                print("\n  [!] Nomor telepon harus terdiri dari 10-13 digit!")
                return
    
        password = input("  Password          : ")
        if len(password) < 5:
            print("\n  [!] Password minimal 5 karakter!")
            return
        if any(huruf.isspace() for huruf in password):
            print("\n  [!] Password tidak boleh mengandung spasi!")
            return
        
        print("\n-Alamat")
        nama_jalan = input("  Nama jalan        : ").strip()
        nomor_rumah = input("  Nomor rumah       : ").strip()
        rt = input("  RT                : ").strip()
        rw = input("  RW                : ").strip()
        kelurahan = input("  Kelurahan         : ").strip().title()
        kecamatan = input("  Kecamatan         : ").strip().title()
        kota = input("  Kota              : ").strip().title()
        kode_pos = input("  Kode pos          : ").strip()
    
        if not nama_jalan:
            print("\n  [!] Nama jalan tidak boleh kosong!")
            return
        if not kelurahan or not kecamatan or not kota:
            print("\n  [!] Kelurahan, kecamatan, dan kota wajib diisi!")
            return
        if rt and not rt.isdigit():
            print("\n  [!] RT harus berupa angka!")
            return
        if rw and not rw.isdigit():
            print("\n  [!] RW harus berupa angka!")
            return
        if kode_pos and (not kode_pos.isdigit() or len(kode_pos) != 5):
            print("\n  [!] Kode pos harus terdiri dari 5 digit!")
            return
        
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

    except psycopg2.Error:
        koneksi.rollback()
        print("Gagal mengubah data petani")

    finally:
        cursor.close()
        koneksi.close()


def hapus_petani():
    clear()
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        lihat_petani(cursor)

        id_petani = input("\nMasukkan ID petani yang ingin dihapus: ")
        if not id_petani:
            print("\n  [!] id_petani tidak boleh kosong!")
            return
        if id_petani.isdigit():
            cursor.execute("""
                DELETE FROM petani
                WHERE id_petani = %s
            """, (id_petani,))
    
            if cursor.rowcount > 0:
                koneksi.commit()
                print("Data petani berhasil dihapus!")
            else:
                koneksi.rollback()
                print("\n  [!] ID petani tidak ditemukan!")
                return

        else:
            koneksi.rollback()
            print("\n  [!] Input tidak valid!")
            return

    except psycopg2.Error:
        koneksi.rollback()
        print("Data petani tidak dapat dihapus.")
        print("Petani mungkin masih memiliki data pengajuan panen.")

    finally:
        cursor.close()
        koneksi.close()


def kelola_petani():
    clear()
    while True:
        clear()
        print("\n========== KELOLA DATA PETANI ==========")
        print("1. Lihat Petani")
        print("2. Tambah Petani")
        print("3. Ubah Petani")
        print("4. Hapus Petani")
        print("5. Kembali")

        pilihan = input("Pilih menu: ")

        if not pilihan:
            print("Pilihan tidak boleh kosong.")
            continue

        elif pilihan == "1":
            koneksi = buka_koneksi()
            
            if koneksi is not None:
                cursor = koneksi.cursor()
                lihat_petani(cursor)
                cursor.close()
                koneksi.close()

        elif pilihan == "2":
            tambah_petani()

        elif pilihan == "3":
            ubah_petani()

        elif pilihan == "4":
            hapus_petani()

        elif pilihan == "5":
            break

        else:
            print("Pilihan tidak valid!")

        jeda()


# =====================================
# 3. MELIHAT PRODUK
# =====================================

def lihat_produk():
    clear()
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

    except psycopg2.Error:
        print("Gagal menampilkan produk:")

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

    data_kategori = cursor.fetchall()

    print("\n========== DAFTAR KATEGORI ==========")

    for kategori in data_kategori:
        print(f"{kategori[0]}. {kategori[1]}")

    return data_kategori


def tambah_produk(id_admin):
    clear()
    print("\n========== TAMBAH PRODUK ==========")

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        data_kategori = pilih_kategori(cursor)

        if len(data_kategori) == 0:
            print("Belum ada kategori produk!")
            return

        id_kategori = input("\nPilih ID kategori: ").strip()

        if not id_kategori:
            print("ID kategori tidak boleh kosong.")
            return
        if id_kategori.isdigit():
            id_kategori = int(id_kategori)

            if not any(kategori[0] == id_kategori for kategori in data_kategori):
                print("\n[!] ID kategori tidak ditemukan!")
                return
        
        else:
            print("\n[!] Input tidak valid!")
            return

        # NAMA PRODUK
        nama = input("Nama produk: ").strip().title()

        if not nama:
            print("Nama produk tidak boleh kosong.")
            return
        
        if not nama or not any(huruf.isalnum() for huruf in nama):
            print("\n[!] Input tidak valid!")
            return

        # PILIH SATUAN
        print("Pilih satuan produk:")
        print("1. Kg")
        print("2. Sisir")
        print("3. Ikat")
        print("4. Buah")
        print("5. Karung")

        pilihan = input("Pilih satuan (1-6): ").strip()

        if not pilihan:
            print("ID kategori tidak boleh kosong.")
        if pilihan == "1":
            satuan = "Kg"
        elif pilihan == "2":
            satuan = "Sisir"
        elif pilihan == "3":
            satuan = "Ikat"
        elif pilihan == "5":
            satuan = "Buah"
        elif pilihan == "5":
            satuan = "Karung"
        else:
            print("\n[!] Input tidak valid!")
            return

        # HARGA JUAL
        harga = input("Harga jual: ").strip()

        if not harga.isdigit() or int(harga) <= 0:
            print("\n[!] Input harga tidak valid!")
            return

        # STOK AWAL
        stok = input("Stok awal: ").strip()

        if not stok.isdigit():
            print("\n[!] Input stok tidak valid!")
            return

        # MEMBUAT ID PRODUK
        cursor.execute("""
            SELECT COALESCE(MAX(id_produk), 0) + 1
            FROM produk
        """)

        id_baru = cursor.fetchone()[0]

        # MENYIMPAN PRODUK
        cursor.execute("""
            INSERT INTO produk (
                id_produk, nama_produk, satuan,
                harga_jual, stok, admin_id_admin,
                kategori_produk_id_kategori
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            id_baru, nama, satuan, int(harga),
            int(stok), id_admin, id_kategori
        ))

        koneksi.commit()
        print("\nProduk berhasil ditambahkan!")
        jeda()

    except psycopg2.Error:
        koneksi.rollback()
        print("\n[!] Gagal menambahkan produk!")
        jeda()

    finally:
        cursor.close()
        koneksi.close()


def ubah_produk(id_admin):
    clear()
    print("\n========== UBAH PRODUK ==========")

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        # MENAMPILKAN DATA PRODUK
        lihat_produk(cursor)

        id_produk = input("\nMasukkan ID produk yang ingin diubah: ").strip()

        if not id_produk:
            print("ID produk tidak boleh kosong.")
            return
        if id_produk.isdigit():
            cursor.execute("""
                SELECT id_produk
                FROM produk
                WHERE id_produk = %s
            """, (id_produk,))

            if cursor.fetchone() is None:
                print("\n[!] ID produk tidak ditemukan!")
                return
        else:
            print("\n[!] Input tidak valid!")
            return

        # MENAMPILKAN KATEGORI
        data_kategori = pilih_kategori(cursor)

        if len(data_kategori) == 0:
            print("Belum ada kategori produk!")
            return

        print("\nMasukkan data produk yang baru.")

        # NAMA PRODUK
        nama = input("Nama produk: ").strip().title()

        if not nama:
                    print("nama tidak boleh kosong.")
                    return
        if not nama or not any(huruf.isalnum() for huruf in nama):
            print("\n[!] Input tidak valid!")
            return

        # PILIH SATUAN
        print("\nPilih satuan produk:")
        print("1. Kg")
        print("2. sisir")
        print("3. Ikat")
        print("4. Buah")
        print("5. Karung")

        pilihan = input("Pilih satuan (1-5): ").strip()

        if not pilihan:
            print("Pilihan tidak boleh kosong.")
        if pilihan == "1":
            satuan = "Kg"
        elif pilihan == "2":
            satuan = "Sisir"
        elif pilihan == "3":
            satuan = "Ikat"
        elif pilihan == "4":
            satuan = "Buah"
        elif pilihan == "5":
            satuan = "Karung"
        else:
            print("\n[!] Input tidak valid!")
            return

        # HARGA JUAL
        harga = input("Harga jual: ").strip()

        if not harga:
            print("harga tidak boleh kosong.")
            return
        if not harga.isdigit() or int(harga) <= 0:
            print("\n[!] Input harga tidak valid!")
            return

        # STOK
        stok = input("Stok produk: ").strip()

        if not stok:
            print("stok tidak boleh kosong")
            return
        if not stok.isdigit():
            print("\n[!] Input stok tidak valid!")
            return

        # ID KATEGORI
        id_kategori = input("Masukkan ID kategori: ").strip()

        if not id_kategori:
            print("id_kategori tidak boleh kosong.")
            return

        if id_kategori.isdigit():
            id_kategori = int(id_kategori)

            if not any(kategori[0] == id_kategori for kategori in data_kategori):
                print("\n[!] ID kategori tidak ditemukan!")
                return

        else:
            print("\n[!] Input tidak valid!")
            return

        # UPDATE PRODUK
        cursor.execute("""
            UPDATE produk
            SET nama_produk = %s,
                satuan = %s,
                harga_jual = %s,
                stok = %s,
                admin_id_admin = %s,
                kategori_produk_id_kategori = %s
            WHERE id_produk = %s
        """, (
            nama, satuan, int(harga), int(stok),
            id_admin, id_kategori, id_produk
        ))

        koneksi.commit()
        print("\nProduk berhasil diubah!")
        jeda()

    except psycopg2.Error:
        koneksi.rollback()
        print("\n[!] Data produk tidak dapat diubah!")
        jeda()

    finally:
        cursor.close()
        koneksi.close()

def hapus_produk():
    clear()
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

        id_produk = input("\nMasukkan ID produk yang ingin dihapus: ").strip()

        if not id_produk:
            print("ID produk tidak boleh kosong.")
            return

        if id_produk.isdigit():
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

        else:
            koneksi.rollback()
            print("[!] Input tidak valid!")
            return

    except psycopg2.Error:
        koneksi.rollback()
        print("Produk tidak dapat dihapus karena mungkin masih digunakan.")

    finally:
        cursor.close()
        koneksi.close()

def menu_produk(id_admin):
    while True:
        clear()
        print("\n========== KELOLA PRODUK ==========")
        print("1. Tambah Produk")
        print("2. Ubah Produk")
        print("3. Hapus Produk")
        print("4. Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_produk(id_admin)

        elif pilihan == "2":
            ubah_produk(id_admin)

        elif pilihan == "3":
            hapus_produk()

        elif pilihan == "4":
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# =====================================
# 5. MEMERIKSA KETERSEDIAAN STOK
# =====================================

def lihat_stok():
    clear()
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

    except psycopg2.Error:
        print("Gagal memeriksa stok")

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# 6. MELIHAT DATA HASIL PANEN
# =====================================

def lihat_hasil_panen():
    clear()
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
            ORDER BY h.tanggal_penerimaan ASC
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

    except psycopg2.Error:
        print("Gagal menampilkan hasil panen")

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# 7. MENCATAT PENERIMAAN HASIL PANEN
# =====================================

def terima_hasil_panen(id_admin):
    clear()
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
        """, (id_pengajuan,))
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

    except psycopg2.Error:
        koneksi.rollback()
        print("Gagal mencatat penerimaan panen")

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# 8. MELIHAT DATA TRANSAKSI
# =====================================

def lihat_transaksi():
    clear()
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
            ORDER BY t.tanggal_transaksi ASC
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
# 9. KONFIRMASI PEMBAYARAN
# =====================================

def konfirmasi_pembayaran(id_admin):
    clear()
    print("\n========== KONFIRMASI PEMBAYARAN ==========")

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        # Menampilkan transaksi yang menunggu konfirmasi
        cursor.execute("""
            SELECT id_transaksi, tanggal_transaksi,
                   total_harga, metode_pembayaran
            FROM transaksi
            WHERE status_pembayaran = 'Diproses'
              AND admin_id_admin = %s
            ORDER BY id_transaksi
        """, (id_admin,))

        data = cursor.fetchall()

        if len(data) == 0:
            print("Tidak ada transaksi yang menunggu konfirmasi.")
            return

        for transaksi in data:
            print("\nID Transaksi :", transaksi[0])
            print("Tanggal      :", transaksi[1])
            print("Total Harga  : Rp", transaksi[2])
            print("Metode       :", transaksi[3])

        id_transaksi = input("\nMasukkan ID transaksi: ")

        # Mengambil detail transaksi dan memeriksa stok
        cursor.execute("""
            SELECT d.produk_id_produk,
                   d.jumlah,
                   p.nama_produk,
                   p.stok
            FROM detail_transaksi d
            JOIN produk p
                ON d.produk_id_produk = p.id_produk
            JOIN transaksi t
                ON d.transaksi_id_transaksi = t.id_transaksi
            WHERE d.transaksi_id_transaksi = %s
              AND t.status_pembayaran = 'Diproses'
              AND t.admin_id_admin = %s
            FOR UPDATE OF p
        """, (id_transaksi, id_admin))

        detail = cursor.fetchall()

        if len(detail) == 0:
            print("Transaksi tidak ditemukan atau tidak bisa dikonfirmasi.")
            koneksi.rollback()
            return

        # Memeriksa ketersediaan stok
        stok_cukup = True

        for barang in detail:
            if float(barang[1]) > float(barang[3]):
                print("\nStok", barang[2], "tidak mencukupi.")
                stok_cukup = False

        if not stok_cukup:
            print("Pembayaran belum dapat dikonfirmasi.")
            koneksi.rollback()
            return

        # Meminta konfirmasi Admin

        konfirmasi = input("\nApakah pembayaran sudah diterima? (y/n): ").strip().lower()

        if not konfirmasi:
            print("[!] Konfirmasi tidak boleh kosong.")
            return

        if konfirmasi == "y":
            pass

        elif konfirmasi == "n":
            koneksi.rollback()
            print("Konfirmasi pembayaran dibatalkan.")
            return

        else:
            print("[!] Pilihan tidak valid! Mohon pilih y/n.")
            return
    
        # Mengurangi stok produk
        for barang in detail:
            cursor.execute("""
                UPDATE produk
                SET stok = stok - %s
                WHERE id_produk = %s
            """, (barang[1], barang[0]))

        # Mengubah status pembayaran
        cursor.execute("""
            UPDATE transaksi
            SET tanggal_pembayaran = CURRENT_DATE,
                status_pembayaran = 'Sudah Dibayar'
            WHERE id_transaksi = %s
              AND admin_id_admin = %s
              AND status_pembayaran = 'Diproses'
        """, (id_transaksi, id_admin))

        koneksi.commit()

        print("\nPembayaran berhasil dikonfirmasi!")
        print("ID Transaksi :", id_transaksi)
        print("Status       : Sudah Dibayar")
        print("Stok produk berhasil dikurangi.")

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Gagal mengonfirmasi pembayaran:", error)

    finally:
        cursor.close()
        koneksi.close()

# =====================================
# 10. LAPORAN PENJUALAN
# =====================================

def laporan_penjualan():
    clear()
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
            ORDER BY DATE(tanggal_transaksi) ASC
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

    except psycopg2.Error:
        print("Gagal menampilkan laporan")

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# MENU UTAMA ADMIN
# =====================================

def menu_admin(id_admin):
    while True:
        clear()
        print("\n========== MENU ADMIN ==========")
        print("1. Dashboard")
        print("2. Kelola Data Petani")
        print("3. Melihat Produk")
        print("4. Mengelola Data Produk")
        print("5. Memeriksa Ketersediaan Stok")
        print("6. Melihat Data Hasil Panen")
        print("7. Mencatat Penerimaan Hasil Panen")
        print("8. Melihat Data Transaksi")
        print("9. Konfirmasi Pembayaran")
        print("10. Melihat Laporan Penjualan")
        print("11. Logout")

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
            konfirmasi_pembayaran(id_admin)

        elif pilihan == "10":
            laporan_penjualan()

        elif pilihan == "11":
            print("Anda berhasil logout.")
            break

        else:
            print("Pilihan tidak valid!")

        jeda()
