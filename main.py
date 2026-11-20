from koneksi import buka_koneksi
import psycopg2
from admin import menu_admin
from pembeli import menu_pembeli
from bantuan import clear
# =========================
# FUNGSI LOGIN
# =========================


def login():
    clear()
    print("\n===== LOGIN TANIFLOW =====")

    no_telepon = input("Masukkan nomor telepon: ")
    password = input("Masukkan password: ")

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

            print("\nLogin berhasil!")
            print("Selamat datang,", nama)
            print("Role:", role)

            input("\nTekan Enter untuk melanjutkan...")

            # Mengarahkan pengguna sesuai role
            if role == "Admin":
                menu_admin(id_pengguna)

            elif role == "Petani":
                print("Menu Petani akan dibuka.")

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
    print("\n===== REGISTRASI TANIFLOW =====")
    print("1. Petani")
    print("2. Pembeli")

    pilihan = input("Pilih role: ")

    if pilihan == "1":
        role = "Petani"

    elif pilihan == "2":
        role = "Pembeli"

    else:
        print("Pilihan role tidak tersedia!")
        return

    print("\n===== FORM REGISTRASI", role.upper(), "=====")

    if role == "Petani":
        nama = input("Nama petani: ")
    else:
        nama = input("Nama pembeli: ")

    no_telepon = input("Nomor telepon: ")
    password = input("Password: ")
    konfirmasi_password = input("Konfirmasi password: ")

    if password != konfirmasi_password:
        print("Konfirmasi password tidak cocok!")
        return

    # Mengambil data alamat khusus Petani
    if role == "Petani":
        print("\n===== DATA ALAMAT =====")

        nama_jalan = input("Nama jalan: ")
        nomor_rumah = input("Nomor rumah (boleh kosong): ")
        rt = input("RT (boleh kosong): ")
        rw = input("RW (boleh kosong): ")
        kelurahan = input("Kelurahan: ")
        kecamatan = input("Kecamatan: ")
        kota = input("Kota: ")
        kode_pos = input("Kode pos (boleh kosong): ")

    koneksi = buka_koneksi()

    if koneksi is None:
        return

    cursor = koneksi.cursor()

    try:
        if role == "Petani":

            # Membuat ID petani berikutnya
            cursor.execute("""
                SELECT COALESCE(MAX(id_petani), 0) + 1
                FROM petani
            """)

            id_baru = cursor.fetchone()[0]

            query = """
                INSERT INTO petani (
                    id_petani,
                    nama_petani,
                    no_telepon,
                    nama_jalan,
                    nomor_rumah,
                    rt,
                    rw,
                    kelurahan,
                    kecamatan,
                    kota,
                    kode_pos,
                    password
                )
                VALUES (%s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                id_baru,
                nama,
                no_telepon,
                nama_jalan,
                nomor_rumah,
                rt,
                rw,
                kelurahan,
                kecamatan,
                kota,
                kode_pos,
                password
            ))

        else:

            # Membuat ID pembeli berikutnya
            cursor.execute("""
                SELECT COALESCE(MAX(id_pembeli), 0) + 1
                FROM pembeli
            """)

            id_baru = cursor.fetchone()[0]

            query = """
                INSERT INTO pembeli (
                    id_pembeli,
                    nama_pembeli,
                    no_telepon,
                    password
                )
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(query, (
                id_baru,
                nama,
                no_telepon,
                password
            ))

        koneksi.commit()

        print("\nRegistrasi berhasil!")
        print("ID akun:", id_baru)
        print("Role:", role)
        print("Silakan login menggunakan akun yang sudah dibuat.")

    except psycopg2.IntegrityError:
        koneksi.rollback()
        print("\nNomor telepon sudah terdaftar!")

    except psycopg2.Error as error:
        koneksi.rollback()
        print("\nRegistrasi gagal!")
        print(error)

    finally:
        cursor.close()
        koneksi.close()


# =========================
# MENU UTAMA
# =========================

def main():
    while True:
        clear()
        print("\n========== TANIFLOW ==========")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            login()
            input("\nTekan Enter untuk kembali ke menu utama...")

        elif pilihan == "2":
            registrasi()
            input("\nTekan Enter untuk kembali ke menu utama...")

        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan TaniFlow!")
            break

        else:
            print("Pilihan tidak valid!")
            input("\nTekan Enter untuk kembali ke menu utama...")


# Menjalankan program
main()
