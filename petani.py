
from koneksi import buka_koneksi
import psycopg2
from bantuan import clear, jeda

# =====================================
# 1. MENGIRIM DATA HASIL PANEN
# =====================================


def kirim_pengajuan(id_petani):
    clear()
    print("\n========== PENGAJUAN HASIL PANEN ==========")

    jumlah = input("Jumlah panen yang diajukan: ").strip()

    if not jumlah:
        print("\nJumlah panen tidak boleh kosong!")
        jeda()
        return

    if not jumlah.isdigit():
        print("\nJumlah panen harus berupa angka bulat!")
        jeda()
        return

    jumlah = int(jumlah)

    if not jumlah:
        print("\nJumlah tidak boleh kosong")

    if jumlah <= 0:
        print("\nJumlah panen harus lebih dari 0")
        jeda()
        return

    print("\nPilih satuan hasil panen:")
    print("1. Kg")
    print("2. Ikat")
    print("3. Sisir")
    print("4. Buah")

    pilihan_satuan = input("Pilih satuan: ").strip()

    satuan = {
        "1": "Kg",
        "2": "Ikat",
        "3": "Sisir",
        "4": "Buah"
    }
    if pilihan_satuan not in satuan:
        print("\nPilihan satuan tidak valid atau belum dipilih!")
        jeda()
        return
    
    satuan_panen = satuan[pilihan_satuan]

    catatan = input("Catatan tambahan (opsional): ").strip()

    koneksi = buka_koneksi()

    if koneksi is None:
        print("\nGagal terhubung ke database!")
        jeda()
        return

    cursor = None

    try:
        cursor = koneksi.cursor()

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
                satuan,
                status_pengajuan,
                catatan,
                petani_id_petani,
                admin_id_admin
            )
            VALUES (
                %s, CURRENT_DATE, %s,  %s, 'Menunggu',
                %s, %s, NULL
            )
        """, (
            id_baru,
            jumlah,
            satuan_panen,
            catatan if catatan else None,
            id_petani
        ))

        koneksi.commit()

        print("\nPengajuan hasil panen berhasil dikirim!")
        print("ID Pengajuan:", id_baru)
        print("Jumlah diajukan:", jumlah, satuan_panen)
        print("Status: Menunggu")

    except psycopg2.Error:
        koneksi.rollback()
        print("\nGagal mengirim pengajuan!")
        print("Terjadi kesalahan pada database.")

    finally:
        if cursor is not None:
            cursor.close()
        koneksi.close()

    jeda()



# =====================================
# 2. MELIHAT DATA HASIL PANEN
# =====================================

def lihat_hasil_panen(id_petani):
    clear()
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
            ORDER BY h.tanggal_penerimaan ASC
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

    jeda()


# =====================================
# 3. MELIHAT RIWAYAT PENGAJUAN PANEN
# =====================================

def riwayat_pengajuan(id_petani):
    clear()
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
            ORDER BY tanggal_pengajuan ASC
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

    jeda()


# =====================================
# MENU UTAMA PETANI
# =====================================

def menu_petani(id_petani):
    while True:
        clear()
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

    jeda()
