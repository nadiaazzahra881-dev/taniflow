from koneksi import buka_koneksi
import psycopg2
from admin import menu_admin
from pembeli import menu_pembeli
from bantuan import clear,jeda, tampilkan_judul,garis,keluar, garis_ganda, garis_tipis,garis_titik
from petani import menu_petani

# =========================
# FUNGSI LOGIN
# =========================


def login():
    clear()
    tampilkan_judul()
    print("                        LOGIN AKUN")
    garis_tipis()
    print("Silakan masukkan informasi akun Anda:")

    no_telepon = input("\n  Nomor telepon     : ").strip()
    
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
    
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        query = """
            SELECT id_admin, nama_admin, 'Admin' AS role
            FROM admin
            WHERE no_telepon = %s AND password = %s

            UNION ALL

            SELECT id_petani, nama_petani, 'Petani' AS role
            FROM petani
            WHERE no_telepon = %s AND password = %s

            UNION ALL

            SELECT id_pembeli, nama_pembeli, 'Pembeli' AS role
            FROM pembeli
            WHERE no_telepon = %s AND password = %s
        """

        cursor.execute(query, (
            no_telepon, password,
            no_telepon, password,
            no_telepon, password
        ))

        data = cursor.fetchall()

        if len(data) == 1:
            id_pengguna = data[0][0]
            nama = data[0][1]
            role = data[0][2]

            print()
            garis_ganda()
            print("Login berhasil!")
            print("Selamat datang,", nama)
            print("Role:", role)
            garis_ganda()

            input("\nTekan Enter untuk melanjutkan...")

            # Mengarahkan pengguna sesuai role
            if role == "Admin":
                menu_admin(id_pengguna)

            elif role == "Petani":
                menu_petani(id_pengguna)

            elif role == "Pembeli":
                menu_pembeli(id_pengguna)

        elif len(data) > 1:
            print("\nNomor telepon terdaftar pada lebih dari satu role.")
            print("Silakan periksa kembali data akun.")

        else:
            print("\nNomor telepon atau password salah!")

    except psycopg2.Error as error:
        print("Terjadi kesalahan:", error)

    finally:
        cursor.close()
        koneksi.close()


# =========================
# FUNGSI REGISTRASI
# =========================

def registrasi():
    clear()

    tampilkan_judul()
    print("                    REGISTRASI AKUN")
    garis_tipis()
    print("  Silakan pilih jenis akun yang ingin dibuat.")
    print()
    print("  [1] Petani")
    print("  [2] Pembeli")
    print("-" * 55)

    pilihan = input("  Pilih role [1/2] : ").strip()

    if pilihan == "1":
        role = "Petani"

    elif pilihan == "2":
        role = "Pembeli"

    elif not pilihan:
        print("\n  [!] Role tidak boleh kosong!")
        return

    else:
        print("\n  [!] Pilihan role tidak tersedia!")
        return

    clear()

    tampilkan_judul()
    print("                 FORM REGISTRASI", role.upper())
    garis_tipis()
    print("Silakan lengkapi data akun berikut:")

    # DATA AKUN
    if role == "Petani":
        nama = input("\n  Nama petani       : ").strip().title()
    else:
        nama = input("\n  Nama pembeli      : ").strip().title()

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

    # DATA ALAMAT PETANI
    if role == "Petani":

        nama_jalan = input("  Nama jalan        : ").strip()
        if not nama_jalan:
            print("\n  [!] Nama jalan tidak boleh kosong!")
            return
        
        nomor_rumah = input("  Nomor rumah       : ").strip()

        rt = input("  RT                : ").strip()
        if rt and not rt.isdigit():
            print("\n  [!] RT harus berupa angka!")
            return
        
        rw = input("  RW                : ").strip()
        if rw and not rw.isdigit():
            print("\n  [!] RW harus berupa angka!")
            return

        kelurahan = input("  Kelurahan         : ").strip().title() 
        kecamatan = input("  Kecamatan         : ").strip().title()
        kota = input("  Kota              : ").strip().title()
        kode_pos = input("  Kode pos          : ").strip()

        if not kelurahan or not kecamatan or not kota:
            print("\n  [!] Kelurahan, kecamatan, dan kota wajib diisi!")
            return

        if rw and not rw.isdigit():
            print("\n  [!] RW harus berupa angka!")
            return

        if kode_pos and (not kode_pos.isdigit() or len(kode_pos) != 5):
            print("\n  [!] Kode pos harus terdiri dari 5 digit!")
            return

    # KONEKSI DATABASE
    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        if role == "Petani":

            cursor.execute("""
                SELECT COALESCE(MAX(id_petani), 0) + 1
                FROM petani
            """)

            id_baru = cursor.fetchone()[0]

            query = """
                INSERT INTO petani (
                    id_petani, nama_petani, no_telepon,
                    nama_jalan, nomor_rumah, rt, rw,
                    kelurahan, kecamatan, kota, kode_pos, password
                )
                VALUES (%s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                id_baru, nama, no_telepon,
                nama_jalan, nomor_rumah, rt, rw,
                kelurahan, kecamatan, kota, kode_pos, password
            ))

        else:

            cursor.execute("""
                SELECT COALESCE(MAX(id_pembeli), 0) + 1
                FROM pembeli
            """)

            id_baru = cursor.fetchone()[0]

            query = """
                INSERT INTO pembeli (
                    id_pembeli, nama_pembeli, no_telepon, password
                )
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(query, (
                id_baru, nama, no_telepon, password
            ))

        koneksi.commit()

        clear()

        tampilkan_judul()
        print()
        garis_ganda()
        print("                    REGISTRASI BERHASIL!")
        print("                 Akun telah berhasil dibuat")
        garis_ganda()
        print()
        print("  ID Akun       :", id_baru)
        print("  Nama          :", nama)
        print("  Role          :", role)
        print("  No. Telepon   :", no_telepon)
        print()
        print("-" * 55)
        print("  Silakan login menggunakan akun Anda.")
        print("=" * 55)

    except psycopg2.IntegrityError as error:
        koneksi.rollback()

        print("\n" + "=" * 55)
        print("                 REGISTRASI GAGAL")
        print("-" * 55)

        if error.pgcode == "23505":
            print("  [!] Nomor telepon sudah terdaftar!")

        elif error.pgcode == "23502":
            print("  [!] Ada data wajib yang belum diisi!")

        elif error.pgcode == "23503":
            print("  [!] Data tidak sesuai dengan data terkait!")

        else:
            print("  [!] Data tidak memenuhi ketentuan database.")

        print("=" * 55)

    except psycopg2.Error:
        koneksi.rollback()

        print("\n" + "=" * 55)
        print("                 REGISTRASI GAGAL")
        print("-" * 55)
        print("  [!] Terjadi kesalahan pada database.")
        print("  Silakan coba kembali nanti.")
        print("=" * 55)

    finally:
        if cursor is not None:
            cursor.close()

        koneksi.close()
        
# =========================
# MENU UTAMA
# =========================

def main():
    while True:
        clear()

        tampilkan_judul()

        # DATA AKUN
        
        garis_tipis()
        
        print("\n1. Login")
        print("2. Registrasi")
        print("3. Keluar")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            login()
            input("\nTekan Enter untuk kembali ke menu utama...")

        elif pilihan == "2":
            registrasi()
            input("\nTekan Enter untuk kembali ke menu utama...")

        elif pilihan == "3":
            keluar()
            return

        else:
            print("Pilihan tidak valid")
            input("\nTekan Enter untuk kembali ke menu utama...")      


# Menjalankan program
while True:
    main()
    input("\nTekan Enter untuk memulai kembali TaniFlow...")
