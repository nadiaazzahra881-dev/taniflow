import os
import time
from pyfiglet import Figlet
from colorama import Fore, Style


LEBAR= 63
# ==========================================
# PENGATUR TAMPILAN
# ==========================================

def tampilkan_judul():
    judul = Figlet(font="BIG")

    logo =[
        "   .-(   )-.   ",
    "(   \\ *| /   )*",
    " *`-. \\|/ .-'* ",
    "     *\\|/*     ",
    "       |       "
    ]

    tulisan = judul.renderText("TaniFlow").splitlines()

    garis()

    for kiri, kanan in zip(logo, tulisan):
        print(Fore.GREEN + kiri + "  " + kanan + Style.RESET_ALL)

    print("SISTEM PENGELOLAAN HASIL PANEN DAN PENJUALAN PRODUK PERTANIAN ")
    garis()

def subbab(judul):
    garis()
    print(Fore.GREEN + judul.center(60) + Style.RESET_ALL)
    garis()

# ==========================================
# MEMBERSIHKAN TERMINAL
# ==========================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")
    print("\033[3J", end="")


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
# JEDA DAN INTERAKSI
# ==========================================

def jeda():
    input("\nTekan Enter untuk melanjutkan...")


def kembali():
    input("\nTekan Enter untuk kembali...")


# ==========================================
# TAMPILAN KHUSUS
# ==========================================


def salam():
    print("\nSelamat datang di TANIFLOW!")


def keluar():
    garis()
    print("TERIMA KASIH TELAH MENGGUNAKAN TANIFLOW".center(LEBAR))
    garis()

def jeda():
    input("\nTekan Enter untuk melanjutkan...")