import os
import time


# ==========================================
# PENGATUR TAMPILAN
# ==========================================

LEBAR = 80


# ==========================================
# MEMBERSIHKAN TERMINAL
# ==========================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


# ==========================================
# GARIS DAN PEMBATAS
# ==========================================

def garis():
    print("=" * LEBAR)


def garis_tipis():
    print("-" * LEBAR)


def garis_ganda():
    print("═" * LEBAR)


def garis_bintang():
    print("*" * LEBAR)


def garis_titik():
    print("." * LEBAR)


def pemisah():
    print("─" * LEBAR)


# ==========================================
# JUDUL DAN HEADER
# ==========================================

def judul(teks):
    print("\n" + "=" * LEBAR)
    print(teks.center(LEBAR))
    print("=" * LEBAR)


def subjudul(teks):
    print("\n" + "-" * LEBAR)
    print(teks.center(LEBAR))
    print("-" * LEBAR)


def header(teks):
    garis_ganda()
    print(teks.center(LEBAR))
    garis_ganda()


def banner(teks):
    garis()
    print()
    print(teks.center(LEBAR))
    print()
    garis()



def logo():
    clear()

    gambar = [
        "  +------------+",
        "  |     __     |",
        "  |  .-'  `-.  |",
        "  | /  .--.  \\ |",
        "  ||  /    \\  ||",
        "  | \\  \\__/  / |",
        "  |  `-.__.-'  |",
        "  |      ||    |",
        "  +------------+"
    ]

    tulisan = [
        "████████╗ █████╗ ███╗   ██╗██╗███████╗██╗      ██████╗ ██╗    ██╗",
        "╚══██╔══╝██╔══██╗████╗  ██║██║██╔════╝██║     ██╔═══██╗██║    ██║",
        "   ██║   ███████║██╔██╗ ██║██║█████╗  ██║     ██║   ██║██║ █╗ ██║",
        "   ██║   ██╔══██║██║╚██╗██║██║██╔══╝  ██║     ██║   ██║██║███╗██║",
        "   ██║   ██║  ██║██║ ╚████║██║██║     ███████╗╚██████╔╝╚███╔███╔╝",
        "   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝      ╚══════╝ ╚═════╝  ╚══╝╚══╝"
    ]

    print("=" * 100)
    print()

    for i in range(9):
        kiri = gambar[i]
        kanan = tulisan[i] if i < len(tulisan) else ""

        print(f"{kiri:<21}  {kanan}")

    print()
    print(" " * 23 + "Sistem Informasi Pengelolaan Hasil Panen")
    print(" " * 23 + "dan Transaksi Penjualan")
    print()
    print("=" * 100)



# ==========================================
# KOTAK INFORMASI
# ==========================================

def kotak(teks):
    print("+" + "-" * (LEBAR - 2) + "+")
    print("|" + teks.center(LEBAR - 2) + "|")
    print("+" + "-" * (LEBAR - 2) + "+")


def info(label, isi):
    print(f"[{label}] {isi}")


def sukses(teks):
    print(f"\n[✓] {teks}")


def gagal(teks):
    print(f"\n[!] {teks}")


def peringatan(teks):
    print(f"\n[WARNING] {teks}")


def informasi(teks):
    print(f"\n[INFO] {teks}")


# ==========================================
# MENU
# ==========================================

def menu(daftar_menu):
    garis()
    print("MENU PILIHAN".center(LEBAR))
    garis()

    for nomor, nama in daftar_menu:
        print(f"[{nomor}] {nama}")

    garis()


def pilihan(teks="Pilihan Anda"):
    return input(f"\n{teks}: ")


# ==========================================
# TAMPILAN DATA
# ==========================================

def tampil_data(label, isi):
    print(f"{label:<25}: {isi}")


def data_kosong():
    print("\n" + "-" * LEBAR)
    print("BELUM ADA DATA".center(LEBAR))
    print("-" * LEBAR)


def daftar(teks):
    print(f"  > {teks}")


# ==========================================
# JEDA DAN INTERAKSI
# ==========================================

def jeda():
    input("\nTekan Enter untuk melanjutkan...")


def kembali():
    input("\nTekan Enter untuk kembali...")


def loading(teks="Memproses"):
    print(teks, end="", flush=True)

    for i in range(3):
        time.sleep(0.4)
        print(".", end="", flush=True)

    print()


def spasi(jumlah=1):
    print("\n" * jumlah)


# ==========================================
# TAMPILAN KHUSUS
# ==========================================

def footer(teks="TANIFLOW"):
    garis_tipis()
    print(teks.center(LEBAR))
    garis_tipis()


def salam():
    print("\nSelamat datang di TANIFLOW!")


def keluar():
    garis()
    print("TERIMA KASIH TELAH MENGGUNAKAN TANIFLOW".center(LEBAR))
    garis()


def konfirmasi(teks):
    jawab = input(f"\n{teks} (y/n): ").lower().strip()
    return jawab == "y"


def clear():
    os.system("cls")

def jeda():
    input("\nTekan Enter untuk melanjutkan...")