from koneksi import buka_koneksi
import psycopg2
from bantuan import clear

# ==========================================
# 1. MELIHAT PRODUK
# ==========================================

def lihat_produk():
    clear()
    print("\n========== DAFTAR PRODUK ==========")

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT p.id_produk, p.nama_produk,
                   k.nama_kategori, p.harga_jual,
                   p.stok, p.satuan
            FROM produk p
            JOIN kategori_produk k
                ON p.kategori_produk_id_kategori = k.id_kategori
            ORDER BY p.id_produk
        """)

        data = cursor.fetchall()

        if not data:
            print("Belum ada produk.")

        else:
            for produk in data:
                print("\nID Produk   :", produk[0])
                print("Nama Produk :", produk[1])
                print("Kategori    :", produk[2])
                print("Harga       : Rp", produk[3])
                print("Stok        :", produk[4], produk[5])

                if produk[4] > 0:
                    print("Keterangan  : Tersedia")
                else:
                    print("Keterangan  : Stok Habis")

    except psycopg2.Error as error:
        print("Gagal menampilkan produk:", error)

    finally:
        cursor.close()
        koneksi.close()


# ==========================================
# 2. MEMILIH PRODUK DAN MEMBUAT TRANSAKSI
# ==========================================

def beli_produk(id_pembeli):
    clear()
    print("\n========== PEMBELIAN PRODUK ==========")

    lihat_produk()

    id_produk = input("\nMasukkan ID produk yang ingin dibeli: ")

    try:
        jumlah = float(input("Masukkan jumlah pembelian: "))

        if jumlah <= 0:
            print("Jumlah pembelian harus lebih dari 0.")
            return

    except ValueError:
        print("Jumlah harus berupa angka.")
        return

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        cursor.execute("""
            SELECT nama_produk, harga_jual, stok
            FROM produk
            WHERE id_produk = %s
        """, (id_produk,))

        produk = cursor.fetchone()

        if produk is None:
            print("Produk tidak ditemukan.")
            return

        nama_produk = produk[0]
        harga = float(produk[1])
        stok = float(produk[2])

        if stok <= 0:
            print("Maaf, stok produk sedang habis.")
            return

        if jumlah > stok:
            print("Jumlah pembelian melebihi stok tersedia.")
            print("Stok tersedia:", stok)
            return

        total_harga = harga * jumlah

        print("\n========== RINCIAN PEMBELIAN ==========")
        print("Nama Produk :", nama_produk)
        print("Harga       : Rp", harga)
        print("Jumlah      :", jumlah)
        print("Total Harga : Rp", total_harga)

        konfirmasi = input("\nBuat transaksi ini? (y/n): ")

        if konfirmasi.lower() != "y":
            print("Pembelian dibatalkan.")
            return

        # Membuat ID transaksi baru
        cursor.execute("""
            SELECT COALESCE(MAX(id_transaksi), 0) + 1
            FROM transaksi
        """)

        id_transaksi = cursor.fetchone()[0]

        # Membuat ID detail transaksi baru
        cursor.execute("""
            SELECT COALESCE(MAX(id_detail), 0) + 1
            FROM detail_transaksi
        """)

        id_detail = cursor.fetchone()[0]

        # Menyimpan transaksi
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
                NULL, NULL, 'Belum Dibayar', NULL
            )
        """, (id_transaksi, total_harga, id_pembeli))

        # Menyimpan detail transaksi
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
            jumlah,
            harga,
            id_transaksi,
            id_produk
        ))

        koneksi.commit()

        print("\nTransaksi berhasil dibuat!")
        print("ID Transaksi :", id_transaksi)
        print("Total Harga  : Rp", total_harga)
        print("Status       : Belum Dibayar")
        print("Silakan lakukan pembayaran.")

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Gagal membuat transaksi:", error)

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
            return

        konfirmasi = input("\nKonfirmasi pembayaran? (y/n): ")

        if konfirmasi.lower() != "y":
            koneksi.rollback()
            print("Pembayaran dibatalkan.")
            return

        # Mengurangi stok produk setelah pembayaran
        for barang in detail:
            cursor.execute("""
                UPDATE produk
                SET stok = stok - %s
                WHERE id_produk = %s
            """, (barang[1], barang[0]))

        # Memperbarui status pembayaran
        cursor.execute("""
            UPDATE transaksi
            SET tanggal_pembayaran = CURRENT_DATE,
                metode_pembayaran = %s,
                status_pembayaran = 'Sudah Dibayar'
            WHERE id_transaksi = %s
              AND pembeli_id_pembeli = %s
        """, (metode, id_transaksi, id_pembeli))

        koneksi.commit()

        print("\nPembayaran berhasil!")
        print("ID Transaksi :", id_transaksi)
        print("Total Bayar  : Rp", total_harga)
        print("Metode       :", metode)
        print("Status       : Sudah Dibayar")
        print("Stok produk berhasil diperbarui.")

    except psycopg2.Error as error:
        koneksi.rollback()
        print("Pembayaran gagal:", error)

    finally:
        cursor.close()
        koneksi.close()


# ==========================================
# 4. MEMERIKSA KETERSEDIAAN STOK
# ==========================================

def periksa_stok():
    clear()
    print("\n========== KETERSEDIAAN STOK ==========")

    lihat_produk()


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
            ORDER BY id_transaksi DESC
        """, (id_pembeli,))

        data = cursor.fetchall()

        if not data:
            print("Belum ada riwayat transaksi.")

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

        elif pilihan == "5":
            riwayat_transaksi(id_pembeli)

        elif pilihan == "6":
            print("\nLogout berhasil.")
            break

        else:
            print("Pilihan tidak valid.")


