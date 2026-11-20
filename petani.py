
from koneksi import buka_koneksi
import psycopg2


# =====================================
# 1. MENGIRIM DATA HASIL PANEN
# =====================================

def kirim_pengajuan(id_petani):
    print("\n========== PENGAJUAN HASIL PANEN ==========")

    jumlah = input("Jumlah panen yang diajukan: ")
    catatan = input("Catatan tambahan: ")

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT COALESCE(MAX(id_pengajuan), 0) + 1
            FROM pengajuan_panen
        """)

        id_baru = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO pengajuan_panen (
                id_pengajuan,
                tanggal_pengajuan,
                jumlah_diajukan,
                status_pengajuan,
                catatan,
                petani_id_petani,
                admin_id_admin
            )
            VALUES (
                %s, CURRENT_DATE, %s, 'Menunggu',
                %s, %s, NULL
            )
        """, (
            id_baru,
            jumlah,
            catatan,
            id_petani
        ))

        koneksi.commit()

        print("\nPengajuan hasil panen berhasil dikirim!")
        print("ID Pengajuan:", id_baru)

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Gagal mengirim pengajuan:", error)

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# 2. MELIHAT DATA HASIL PANEN
# =====================================

def lihat_hasil_panen(id_petani):
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT h.id_hasil,
                   p.nama_produk,
                   h.tanggal_penerimaan,
                   h.jumlah_panen,
                   h.harga_beli
            FROM hasil_panen h
            JOIN pengajuan_panen pg
                ON h.pengajuan_panen_id_pengajuan = pg.id_pengajuan
            JOIN produk p
                ON h.produk_id_produk = p.id_produk
            WHERE pg.petani_id_petani = %s
            ORDER BY h.tanggal_penerimaan DESC
        """, (id_petani,))

        data = cursor.fetchall()

        print("\n========== DATA HASIL PANEN ==========")

        if len(data) == 0:
            print("Belum ada hasil panen yang diterima.")

        else:
            for hasil in data:
                print("\nID Hasil       :", hasil[0])
                print("Nama Produk    :", hasil[1])
                print("Tanggal Terima :", hasil[2])
                print("Jumlah Panen   :", hasil[3])
                print("Harga Beli     :", hasil[4])

    except psycopg2.Error as error:
        print("Gagal menampilkan hasil panen:", error)

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# 3. MELIHAT RIWAYAT PENGAJUAN PANEN
# =====================================

def riwayat_pengajuan(id_petani):
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT id_pengajuan,
                   tanggal_pengajuan,
                   jumlah_diajukan,
                   status_pengajuan,
                   catatan
            FROM pengajuan_panen
            WHERE petani_id_petani = %s
            ORDER BY tanggal_pengajuan DESC
        """, (id_petani,))

        data = cursor.fetchall()

        print("\n========== RIWAYAT PENGAJUAN PANEN ==========")

        if len(data) == 0:
            print("Belum ada riwayat pengajuan.")

        else:
            for pengajuan in data:
                print("\nID Pengajuan :", pengajuan[0])
                print("Tanggal      :", pengajuan[1])
                print("Jumlah       :", pengajuan[2])
                print("Status       :", pengajuan[3])
                print("Catatan      :", pengajuan[4])

    except psycopg2.Error as error:
        print("Gagal menampilkan riwayat:", error)

    finally:
        cursor.close()
        koneksi.close()


# =====================================
# MENU UTAMA PETANI
# =====================================

def menu_petani(id_petani):
    while True:
        print("\n========== MENU PETANI ==========")
        print("1. Mengirim Data Hasil Panen")
        print("2. Melihat Data Hasil Panen")
        print("3. Melihat Riwayat Penyerahan Hasil Panen")
        print("4. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            kirim_pengajuan(id_petani)

        elif pilihan == "2":
            lihat_hasil_panen(id_petani)

        elif pilihan == "3":
            riwayat_pengajuan(id_petani)

        elif pilihan == "4":
            print("Anda berhasil logout.")
            break

        else:
            print("Pilihan tidak valid!")
