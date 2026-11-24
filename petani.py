
from koneksi import buka_koneksi
import psycopg2
from bantuan import clear, jeda

# =====================================
# 1. MENGIRIM DATA HASIL PANEN
# =====================================

def kirim_pengajuan(id_petani):
    clear()
    print("\n========== PENGAJUAN HASIL PANEN ==========")

    koneksi = buka_koneksi()

    if koneksi is None:
        print("\nGagal terhubung ke database!")
        jeda()
        return

    cursor = None

    try:
        cursor = koneksi.cursor()

        # Mengambil daftar produk
        cursor.execute("""
            SELECT id_produk, nama_produk, satuan
            FROM produk
            ORDER BY id_produk
        """)

        data_produk = cursor.fetchall()

        daftar_pengajuan = []

        while True:
            clear()
            print("\n========== PENGAJUAN HASIL PANEN ==========")

            if len(daftar_pengajuan) > 0:
                print("\nDAFTAR PRODUK YANG DIAJUKAN")

                for i, produk in enumerate(daftar_pengajuan, start=1):
                    print(f"{i}. {produk['nama']} - {produk['jumlah']} {produk['satuan']}")

            print("\nPILIH PRODUK")

            for i, produk in enumerate(data_produk, start=1):
                print(f"{i}. {produk[1]} ({produk[2]})")

            pilihan_baru = len(data_produk) + 1

            print(f"{pilihan_baru}. Produk belum tersedia (masukkan dalam catatan)")

            print("\n0. Kembali")

            pilihan = input("\nPilih produk: ").strip()

            if pilihan == "0":
                return

            if not pilihan.isdigit():
                print("\nPilihan tidak valid!")
                jeda()
                continue

            pilihan = int(pilihan)

            if pilihan < 1 or pilihan > pilihan_baru:
                print("\nPilihan tidak tersedia!")
                jeda()
                continue

            # Produk belum tersedia
            if pilihan == pilihan_baru:
                nama = input("\nMasukkan nama produk: ").strip()

                if not nama:
                    print("\nNama produk tidak boleh kosong!")
                    jeda()
                    continue

                satuan = input("Masukkan satuan produk: ").strip()

                if not satuan:
                    print("\nSatuan tidak boleh kosong!")
                    jeda()
                    continue

                id_produk = None

            # Produk sudah tersedia
            else:
                produk = data_produk[pilihan - 1]

                id_produk = produk[0]
                nama = produk[1]
                satuan = produk[2]

            jumlah = input("Jumlah panen: ").strip()

            try:
                jumlah = float(jumlah)

                if jumlah <= 0:
                    print("\nJumlah harus lebih dari 0!")
                    jeda()
                    continue

            except ValueError:
                print("\nJumlah harus berupa angka!")
                jeda()
                continue

            daftar_pengajuan.append({
                "id_produk": id_produk,
                "nama": nama,
                "jumlah": jumlah,
                "satuan": satuan
            })

            print("\nProduk berhasil ditambahkan!")
            jeda()

            while True:
                clear()
                print("\n========== DAFTAR PRODUK ==========")

                for i, produk in enumerate(daftar_pengajuan, start=1):
                    print(f"{i}. {produk['nama']} - {produk['jumlah']} {produk['satuan']}")

                print("\n1. Tambah produk")
                print("2. Hapus produk")
                print("3. Selesai")

                menu = input("\nPilih menu: ").strip()

                if menu == "1":
                    break

                elif menu == "2":
                    if len(daftar_pengajuan) == 0:
                        print("\nBelum ada produk!")
                        jeda()
                        continue

                    nomor = input("Nomor produk yang dihapus: ").strip()

                    if nomor.isdigit():
                        nomor = int(nomor)

                        if 1 <= nomor <= len(daftar_pengajuan):
                            daftar_pengajuan.pop(nomor - 1)
                            print("\nProduk berhasil dihapus!")
                        else:
                            print("\nNomor produk tidak tersedia!")
                    else:
                        print("\nInput harus berupa angka!")

                    jeda()

                elif menu == "3":
                    if len(daftar_pengajuan) == 0:
                        print("\nTambahkan minimal satu produk!")
                        jeda()
                        continue

                    break

                else:
                    print("\nPilihan tidak valid!")
                    jeda()

            if menu == "3":
                break

        # Catatan tambahan
        print("\n========== CATATAN TAMBAHAN ==========")
        catatan_tambahan = input("Catatan (opsional): ").strip()

        # Menyusun daftar produk menjadi catatan
        catatan = "DAFTAR PRODUK YANG DIAJUKAN:\n"

        for produk in daftar_pengajuan:
            if produk["id_produk"] is None:
                catatan += (
                    f"- Produk belum tersedia: {produk['nama']} | "
                    f"Jumlah: {produk['jumlah']} {produk['satuan']}\n"
                )
            else:
                catatan += (
                    f"- {produk['nama']} (ID: {produk['id_produk']}) | "
                    f"Jumlah: {produk['jumlah']} {produk['satuan']}\n"
                )

        if catatan_tambahan:
            catatan += "\nCatatan tambahan: " + catatan_tambahan

        # Mengambil ID pengajuan baru
        cursor.execute("""
            SELECT COALESCE(MAX(id_pengajuan), 0) + 1
            FROM pengajuan_panen
        """)

        id_baru = cursor.fetchone()[0]

        # Mengambil Admin penanggung jawab
        cursor.execute("""
            SELECT id_admin
            FROM admin
            ORDER BY id_admin
            LIMIT 1
        """)

        data_admin = cursor.fetchone()

        if data_admin is None:
            print("\nData Admin belum tersedia!")
            koneksi.rollback()
            jeda()
            return

        id_admin = data_admin[0]

        # Menyimpan pengajuan
        cursor.execute("""
            INSERT INTO pengajuan_panen (
                id_pengajuan,
                tanggal_pengajuan,
                status_pengajuan,
                catatan,
                petani_id_petani,
                admin_id_admin
            )
            VALUES (
                %s, CURRENT_DATE, 'Menunggu',
                %s, %s, %s
            )
        """, (
            id_baru,
            catatan,
            id_petani,
            id_admin
        ))

        koneksi.commit()

        print("\nPengajuan hasil panen berhasil dikirim!")
        print("ID Pengajuan:", id_baru)
        print("Jumlah jenis produk:", len(daftar_pengajuan))
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
