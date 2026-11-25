
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
            SELECT p.id_produk, p.nama_produk, p.satuan,
                   k.nama_kategori
            FROM produk p
            JOIN kategori_produk k
                ON p.kategori_produk_id_kategori = k.id_kategori
            ORDER BY p.id_produk
        """)

        data_produk = cursor.fetchall()

        # Mengambil daftar kategori
        cursor.execute("""
            SELECT id_kategori, nama_kategori
            FROM kategori_produk
            ORDER BY id_kategori
        """)

        data_kategori = cursor.fetchall()

        if len(data_kategori) == 0:
            print("\nKategori produk belum tersedia!")
            jeda()
            return

        daftar_pengajuan = []

        while True:
            clear()
            print("\n========== PENGAJUAN HASIL PANEN ==========")

            if len(daftar_pengajuan) > 0:
                print("\nDAFTAR PRODUK YANG DIAJUKAN")

                for i, produk in enumerate(daftar_pengajuan, start=1):
                    print(
                        f"{i}. {produk['nama']} - "
                        f"{produk['jumlah']} {produk['satuan']}"
                    )

            print("\nPILIH PRODUK")

            for i, produk in enumerate(data_produk, start=1):
                print(
                    f"{i}. {produk[1]} "
                    f"({produk[2]}) - {produk[3]}"
                )

            pilihan_baru = len(data_produk) + 1

            print(f"{pilihan_baru}. Produk belum tersedia")

            print("\n0. Kembali ke menu")

            pilihan = input("\nPilih produk: ").strip()

            if pilihan == "0":
                return

            if not pilihan.isdigit():
                print("\nPilihan tidak valid!")
                jeda()
                return

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

                # Memilih kategori
                print("\n========== PILIH KATEGORI ==========")

                for i, kategori in enumerate(data_kategori, start=1):
                    print(f"{i}. {kategori[1]}")

                pilih_kategori = input(
                    "\nPilih kategori: "
                ).strip()

                if not pilih_kategori.isdigit():
                    print("\nPilihan kategori tidak valid!")
                    jeda()
                    continue

                pilih_kategori = int(pilih_kategori)

                if pilih_kategori < 1 or pilih_kategori > len(data_kategori):
                    print("\nKategori tidak tersedia!")
                    jeda()
                    continue

                id_kategori = data_kategori[pilih_kategori - 1][0]
                nama_kategori = data_kategori[pilih_kategori - 1][1]

                print("\nPilih satuan produk:")
                print("1. Kg")
                print("2. Sisir")
                print("3. Ikat")
                print("4. Buah")
                print("5. Karung")

                pilihan_satuan = input("Pilih satuan (1-5): ").strip()

                if not satuan:
                    print("\nSatuan tidak boleh kosong!")
                    jeda()
                    continue
                elif pilihan_satuan == "1":
                    satuan = "Kg"
                elif pilihan_satuan == "2":
                    satuan = "Sisir"
                elif pilihan_satuan == "3":
                    satuan = "Ikat"
                elif pilihan_satuan == "4":
                    satuan = "Buah"
                elif pilihan_satuan == "5":
                    satuan = "Karung"
                else:
                    print("\nPilihan satuan tidak valid!")
                    jeda()
                    return

                id_produk = None

            # Produk sudah tersedia
            else:
                produk = data_produk[pilihan - 1]

                id_produk = produk[0]
                nama = produk[1]
                satuan = produk[2]
                id_kategori = None
                nama_kategori = produk[3]

            # Memasukkan jumlah panen
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
                "satuan": satuan,
                "id_kategori": id_kategori,
                "nama_kategori": nama_kategori
            })

            print("\nProduk berhasil ditambahkan!")
            jeda()

            while True:
                clear()
                print("\n========== DAFTAR PRODUK ==========")

                for i, produk in enumerate(daftar_pengajuan, start=1):
                    print(
                        f"{i}. {produk['nama']} - "
                        f"{produk['jumlah']} {produk['satuan']}"
                    )

                print("\n1. Tambah produk")
                print("2. Hapus produk")
                print("3. Selesai")

                menu = input("\nPilih menu: ").strip()

                if menu == "1":
                    break

                elif menu == "2":

                    nomor = input(
                        "Nomor produk yang dihapus: "
                    ).strip()

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
        catatan = input("Catatan (opsional): ").strip()

               # Mengambil ID pengajuan baru
        cursor.execute("""
            SELECT COALESCE(MAX(id_pengajuan), 0) + 1
            FROM pengajuan_panen
        """)

        id_pengajuan = cursor.fetchone()[0]

        # Mengambil ID admin terkecil sebagai admin awal
        cursor.execute("""
            SELECT id_admin
            FROM admin
            ORDER BY id_admin
            LIMIT 1
        """)

        data_admin = cursor.fetchone()

        if data_admin is None:
            raise Exception("Data Admin belum tersedia!")

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
            id_pengajuan,
            catatan if catatan else None,
            id_petani,
            id_admin
        ))

        # Menyimpan produk dan hasil panen
        for produk in daftar_pengajuan:

            id_produk = produk["id_produk"]

            # Membuat produk baru secara otomatis
            if id_produk is None:

                cursor.execute("""
                    SELECT COALESCE(MAX(id_produk), 0) + 1
                    FROM produk
                """)

                id_produk = cursor.fetchone()[0]

                # Mengambil ID admin terkecil
                cursor.execute("""
                    SELECT id_admin
                    FROM admin
                    ORDER BY id_admin
                    LIMIT 1
                """)

                data_admin = cursor.fetchone()

                if data_admin is None:
                    raise Exception("Data Admin belum tersedia!")

                id_admin = data_admin[0]

                cursor.execute("""
                    INSERT INTO produk (
                        id_produk,
                        nama_produk,
                        satuan,
                        harga_jual,
                        stok,
                        admin_id_admin,
                        kategori_produk_id_kategori
                    )
                    VALUES (%s, %s, %s, 0, 0, %s, %s)
                """, (
                    id_produk,
                    produk["nama"],
                    produk["satuan"],
                    id_admin,
                    produk["id_kategori"]
                ))

            # Mengambil ID hasil panen baru
            cursor.execute("""
                SELECT COALESCE(MAX(id_hasil), 0) + 1
                FROM hasil_panen
            """)

            id_hasil = cursor.fetchone()[0]

            # Menyimpan rincian hasil panen
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
                    %s, CURRENT_DATE, %s, 0, %s, %s
                )
            """, (
                id_hasil,
                produk["jumlah"],
                id_produk,
                id_pengajuan
            ))

        koneksi.commit()

        print("\nPengajuan hasil panen berhasil dikirim!")
        print("ID Pengajuan:", id_pengajuan)
        print("Jumlah jenis produk:", len(daftar_pengajuan))
        print("Status: Menunggu")

    except psycopg2.Error as e:
        koneksi.rollback()

        print("\nGagal mengirim pengajuan!")
        print("Detail:", e)

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
            AND pg.status_pengajuan = 'Diterima'
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
            SELECT pg.id_pengajuan,
                   pg.tanggal_pengajuan,
                   COALESCE(SUM(h.jumlah_panen), 0),
                   pg.status_pengajuan,
                   pg.catatan
            FROM pengajuan_panen pg
            LEFT JOIN hasil_panen h
                ON pg.id_pengajuan = h.pengajuan_panen_id_pengajuan
            WHERE pg.petani_id_petani = %s
            GROUP BY pg.id_pengajuan
            ORDER BY pg.tanggal_pengajuan ASC
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
