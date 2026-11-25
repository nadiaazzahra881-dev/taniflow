from koneksi import buka_koneksi
import psycopg2
from bantuan import clear,jeda

# ==========================================
# 1. MELIHAT PRODUK
# ==========================================

def lihat_produk(tunggu=True):
    print("\n========== DAFTAR PRODUK ==========")

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT p.id_produk, p.nama_produk,
                   k.nama_kategori, p.harga_jual,
                   p.satuan
            FROM produk p
            JOIN kategori_produk k
                ON p.kategori_produk_id_kategori = k.id_kategori
            WHERE p.harga_jual > 0
            ORDER BY p.id_produk
        """)

        data = cursor.fetchall()

        if not data:
            print("Belum ada produk.")

        else:
            print("+----+----------------------+----------------+--------------+--------+")
            print("| ID | Nama Produk          | Kategori       | Harga        | Satuan |")
            print("+----+----------------------+----------------+--------------++-------+")

            for produk in data:
                harga = f"Rp {int(produk[3]):,}".replace(",", ".")

                print(f"| {produk[0]:<2} | {produk[1]:<20} | {produk[2]:<14} | {harga:<12} | {produk[4]:<6} |")
            
            print("+----+----------------------+----------------+--------------+---------+")

        if tunggu:
            jeda()

    except psycopg2.Error as error:
        print("Gagal menampilkan produk:", error)

    finally:
        cursor.close()
        koneksi.close()


# ==========================================
# 2. MEMILIH PRODUK DAN MEMBUAT TRANSAKSI
# ==========================================


def tampilkan_keranjang(keranjang):
    print("\n========== KERANJANG BELANJA ==========")

    if len(keranjang) == 0:
        print("Keranjang masih kosong.")
        return 0

    total = 0

    for i, item in enumerate(keranjang, start=1):
        subtotal = item["harga"] * item["jumlah"]
        total += subtotal

        print(
            f"{i}. {item['nama']} | "
            f"{item['jumlah']:g} {item['satuan']} x "
            f"Rp {item['harga']:,.0f} = Rp {subtotal:,.0f}"
        )

    print("-" * 45)
    print(f"Total Harga : Rp {total:,.0f}")

    return total


def beli_produk(id_pembeli):
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()
    keranjang = []

    try:
        while True:
            clear()
            print("\n========== PEMBELIAN PRODUK ==========")

            total_harga = tampilkan_keranjang(keranjang)

            print("\n1. Tambah produk")
            print("2. Hapus produk dari keranjang")
            print("3. Buat transaksi")
            print("0. Batal")

            menu = input("\nPilih menu: ").strip()

            # ---------- TAMBAH PRODUK ----------
            if menu == "1":
                clear()
                lihat_produk(False)

                id_produk = input(
                    "\nMasukkan ID produk (0 = kembali): "
                ).strip()

                if id_produk == "0":
                    continue

                if not id_produk.isdigit():
                    print("\nID produk harus berupa angka!")
                    jeda()
                    continue

                id_produk = int(id_produk)

                cursor.execute("""
                    SELECT nama_produk, harga_jual, stok, satuan
                    FROM produk
                    WHERE id_produk = %s  AND harga_jual > 0
                """, (id_produk,))

                produk = cursor.fetchone()

                if produk is None:
                    print("\nProduk tidak ditemukan.")
                    jeda()
                    continue

                nama_produk = produk[0]
                harga = float(produk[1])
                stok = float(produk[2])
                satuan = produk[3]

                # Jumlah produk yang sama yang sudah ada di keranjang
                sudah_ada = 0
                item_lama = None

                for item in keranjang:
                    if item["id_produk"] == id_produk:
                        sudah_ada = item["jumlah"]
                        item_lama = item

                tersedia = stok - sudah_ada

                if stok <= 0:
                    print("\nMaaf, stok produk sedang habis.")
                    jeda()
                    continue

                if tersedia <= 0:
                    print("\nSeluruh stok produk ini sudah ada di keranjang.")
                    jeda()
                    continue

                print("\nProduk       :", nama_produk)
                print(f"Harga        : Rp {harga:,.0f} / {satuan}")
                print(f"Stok tersedia: {tersedia:g} {satuan}")

                try:
                    jumlah = float(input("\nMasukkan jumlah pembelian: "))
                except ValueError:
                    print("\nJumlah harus berupa angka.")
                    jeda()
                    continue

                if jumlah <= 0:
                    print("\nJumlah pembelian harus lebih dari 0.")
                    jeda()
                    continue

                if jumlah > tersedia:
                    print("\nJumlah pembelian melebihi stok tersedia.")
                    print(f"Stok tersedia: {tersedia:g} {satuan}")
                    jeda()
                    continue

                if item_lama is not None:
                    item_lama["jumlah"] += jumlah
                else:
                    keranjang.append({
                        "id_produk": id_produk,
                        "nama": nama_produk,
                        "harga": harga,
                        "jumlah": jumlah,
                        "satuan": satuan
                    })

                print("\nProduk berhasil ditambahkan ke keranjang!")
                jeda()

            # ---------- HAPUS PRODUK ----------
            elif menu == "2":
                if len(keranjang) == 0:
                    print("\nKeranjang masih kosong.")
                    jeda()
                    continue

                nomor = input("\nNomor produk yang dihapus: ").strip()

                if not nomor.isdigit():
                    print("\nInput harus berupa angka!")
                    jeda()
                    continue

                nomor = int(nomor)

                if nomor < 1 or nomor > len(keranjang):
                    print("\nNomor produk tidak tersedia!")
                    jeda()
                    continue

                keranjang.pop(nomor - 1)
                print("\nProduk berhasil dihapus dari keranjang!")
                jeda()
                continue

            # ---------- BUAT TRANSAKSI ----------
            elif menu == "3":
                if len(keranjang) == 0:
                    print("\nTambahkan minimal satu produk!")
                    jeda()
                    continue

                konfirmasi = input(
                    "\nBuat transaksi ini? (y/n): "
                ).strip().lower()

                if konfirmasi != "y":
                    print("\nTransaksi belum dibuat.")
                    jeda()
                    continue

                # Mengambil ID Admin
                cursor.execute("""
                    SELECT id_admin
                    FROM admin
                    ORDER BY id_admin
                    LIMIT 1
                """)

                admin = cursor.fetchone()

                if admin is None:
                    print("\nBelum ada Admin yang terdaftar.")
                    jeda()
                    return

                id_admin = admin[0]

                # Membuat ID transaksi baru
                cursor.execute("""
                    SELECT COALESCE(MAX(id_transaksi), 0) + 1
                    FROM transaksi
                """)

                id_transaksi = cursor.fetchone()[0]

                # Menyimpan transaksi (satu transaksi untuk semua produk)
                cursor.execute("""
                    INSERT INTO transaksi (
                        id_transaksi,
                        tanggal_transaksi,
                        total_harga,
                        pembeli_id_pembeli,
                        tanggal_pembayaran,
                        metode_pembayaran,
                        status_pembayaran,
                        admin_id_admin
                    )
                    VALUES (
                        %s, CURRENT_DATE, %s, %s,
                        NULL, NULL, 'Belum Dibayar', %s
                    )
                """, (id_transaksi, total_harga, id_pembeli, id_admin))

                # Membuat ID detail transaksi awal
                cursor.execute("""
                    SELECT COALESCE(MAX(id_detail), 0) + 1
                    FROM detail_transaksi
                """)

                id_detail = cursor.fetchone()[0]

                # Menyimpan satu detail untuk setiap produk
                for item in keranjang:
                    cursor.execute("""
                        INSERT INTO detail_transaksi (
                            id_detail,
                            jumlah,
                            harga_satuan,
                            transaksi_id_transaksi,
                            produk_id_produk
                        )
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        id_detail,
                        item["jumlah"],
                        item["harga"],
                        id_transaksi,
                        item["id_produk"]
                    ))

                    id_detail += 1

                koneksi.commit()

                print("\nTransaksi berhasil dibuat!")
                print("ID Transaksi  :", id_transaksi)
                print("Jumlah produk :", len(keranjang))
                print(f"Total Harga   : Rp {total_harga:,.0f}")
                print("Status        : Belum Dibayar")
                print("Silakan lakukan pembayaran.")
                jeda()
                return

            # ---------- BATAL ----------
            elif menu == "0":
                print("\nPembelian dibatalkan.")
                jeda()
                return

            else:
                print("\nPilihan tidak valid!")
                jeda()

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Gagal membuat transaksi:", error)
        jeda()

    finally:
        cursor.close()
        koneksi.close()


# ==========================================
# 3. MELAKUKAN PEMBAYARAN
# ==========================================

def bayar_transaksi(id_pembeli):
    clear()
    print("\n========== PEMBAYARAN ==========")

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT id_transaksi, total_harga
            FROM transaksi
            WHERE pembeli_id_pembeli = %s
              AND status_pembayaran = 'Belum Dibayar'
        """, (id_pembeli,))

        data = cursor.fetchall()

        if not data:
            print("Tidak ada transaksi yang menunggu pembayaran.")
            jeda()
            return

        print("\nDaftar Transaksi Belum Dibayar:")

        for transaksi in data:
            print("\nID Transaksi :", transaksi[0])
            print("Total Harga  : Rp", transaksi[1])

        id_transaksi = input("\nMasukkan ID transaksi yang ingin dibayar: ")

        cursor.execute("""
            SELECT total_harga
            FROM transaksi
            WHERE id_transaksi = %s
              AND pembeli_id_pembeli = %s
              AND status_pembayaran = 'Belum Dibayar'
        """, (id_transaksi, id_pembeli))

        transaksi = cursor.fetchone()

        if transaksi is None:
            print("Transaksi tidak ditemukan atau sudah dibayar.")
            jeda()
            return

        total_harga = float(transaksi[0])

        # Memeriksa kembali stok produk
        cursor.execute("""
            SELECT d.produk_id_produk,
                   d.jumlah,
                   p.nama_produk,
                   p.stok
            FROM detail_transaksi d
            JOIN produk p
                ON d.produk_id_produk = p.id_produk
            WHERE d.transaksi_id_transaksi = %s
            FOR UPDATE OF p
        """, (id_transaksi,))

        detail = cursor.fetchall()

        stok_cukup = True

        for barang in detail:
            if float(barang[1]) > float(barang[3]):
                print("\nStok", barang[2], "tidak mencukupi.")
                stok_cukup = False

        if not stok_cukup:
            koneksi.rollback()
            print("Pembayaran belum dapat dilakukan.")
            jeda()
            return

        print("\nTotal yang harus dibayar: Rp", total_harga)
        print("\nPilih metode pembayaran:")
        print("1. Tunai")
        print("2. Transfer")

        pilihan = input("Pilih metode pembayaran: ")

        if pilihan == "1":
            metode = "Tunai"

        elif pilihan == "2":
            metode = "Transfer"

        else:
            print("Pilihan metode pembayaran tidak valid.")
            koneksi.rollback()
            jeda()
            return

        konfirmasi = input("\nKonfirmasi pembayaran? (y/n): ")

        if konfirmasi.lower() != "y":
            koneksi.rollback()
            print("Pembayaran dibatalkan.")
            jeda()
            return

        # Mengurangi stok produk setelah pembayaran
        for barang in detail:
            cursor.execute("""
                UPDATE produk
                SET stok = stok - %s
                WHERE id_produk = %s
            """, (barang[1], barang[0]))

        # Memperbarui status transaksi
        cursor.execute("""
            UPDATE transaksi
            SET metode_pembayaran = %s,
                status_pembayaran = 'Diproses'
            WHERE id_transaksi = %s
              AND pembeli_id_pembeli = %s
        """, (metode, id_transaksi, id_pembeli))

        koneksi.commit()

        print("\nPembayaran berhasil dikonfirmasi!")
        print("ID Transaksi :", id_transaksi)
        print("Total Bayar  : Rp", total_harga)
        print("Metode       :", metode)
        print("Status       : Diproses")
        print("Menunggu konfirmasi Admin.")

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Pembayaran gagal:", error)

    finally:
        cursor.close()
        koneksi.close()


# ==========================================
# 4. MEMERIKSA KETERSEDIAAN STOK
# ==========================================

def periksa_stok(tunggu=True):
    clear()
    print("\n========== STOK PRODUK ==========")

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT p.id_produk, p.nama_produk,
                   k.nama_kategori, p.stok, p.satuan
            FROM produk p
            JOIN kategori_produk k
                ON p.kategori_produk_id_kategori = k.id_kategori
            WHERE p.harga_jual > 0
            ORDER BY p.id_produk
        """)

        data = cursor.fetchall()

        if not data:
            print("Belum ada produk.")
        else:
            print("+----+----------------------+----------------+----------+--------+---------------+")
            print("| ID | Nama Produk          | Kategori       | Stok     | Satuan | Keterangan    |")
            print("+----+----------------------+----------------+----------+--------+---------------+")

            for produk in data:
                jumlah_stok = float(produk[3])
                stok = f"{jumlah_stok:g}"

                if jumlah_stok <= 0:
                    keterangan = "Stok Habis"
                elif jumlah_stok <= 10:
                    keterangan = "Menipis"
                else:
                    keterangan = "Tersedia"

                print(f"| {produk[0]:<2} | {produk[1]:<20} | {produk[2]:<14} | {stok:<8} | {produk[4]:<6} | {keterangan:<13} |")

            
        print("+----+----------------------+----------------+--------------+----------+---------+")

        if tunggu:
            jeda()

    except psycopg2.Error as error:
        print("Gagal menampilkan produk:", error)

    finally:
        cursor.close()
        koneksi.close()


# ==========================================
# 5. MELIHAT RIWAYAT TRANSAKSI
# ==========================================

def riwayat_transaksi(id_pembeli):
    clear()
    print("\n========== RIWAYAT TRANSAKSI ==========")

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT id_transaksi, tanggal_transaksi,
                   total_harga, tanggal_pembayaran,
                   metode_pembayaran, status_pembayaran
            FROM transaksi
            WHERE pembeli_id_pembeli = %s
            ORDER BY id_transaksi ASC
        """, (id_pembeli,))

        data = cursor.fetchall()

        if not data:
            print("Belum ada riwayat transaksi.")
            jeda()
            return

        else:
            for transaksi in data:
                print("\nID Transaksi      :", transaksi[0])
                print("Tanggal Transaksi :", transaksi[1])
                print("Total Harga       : Rp", transaksi[2])
                print("Tanggal Pembayaran:", transaksi[3])
                print("Metode Pembayaran :", transaksi[4])
                print("Status Pembayaran :", transaksi[5])

                cursor.execute("""
                    SELECT p.nama_produk, d.jumlah,
                           d.harga_satuan
                    FROM detail_transaksi d
                    JOIN produk p
                        ON d.produk_id_produk = p.id_produk
                    WHERE d.transaksi_id_transaksi = %s
                """, (transaksi[0],))

                detail = cursor.fetchall()

                print("Produk yang dibeli:")

                for barang in detail:
                    print(
                        "-", barang[0],
                        "| Jumlah:", barang[1],
                        "| Harga: Rp", barang[2]
                    )

    except psycopg2.Error as error:
        print("Gagal menampilkan riwayat:", error)

    finally:
        cursor.close()
        koneksi.close()
    jeda()

# ==========================================
# 6. MENU PEMBELI
# ==========================================

def menu_pembeli(id_pembeli):
    while True:
        clear()
        print("\n========== MENU PEMBELI ==========")
        print("1. Melihat Produk")
        print("2. Memilih Produk")
        print("3. Memeriksa Ketersediaan Stok")
        print("4. Melakukan Pembayaran")
        print("5. Melihat Riwayat Transaksi")
        print("6. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            lihat_produk()

        elif pilihan == "2":
            beli_produk(id_pembeli)

        elif pilihan == "3":
            periksa_stok()

        elif pilihan == "4":
            bayar_transaksi(id_pembeli)
            jeda()

        elif pilihan == "5":
            riwayat_transaksi(id_pembeli)

        elif pilihan == "6":
            print("\nLogout berhasil.")
            break

        else:
            print("Pilihan tidak valid.")
            jeda()


