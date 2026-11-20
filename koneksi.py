import psycopg2

def buka_koneksi():
    try:
        koneksi = psycopg2.connect(
            host="localhost",
            database="taniflow",
            user="postgres",
            password="nara789",
            port="5432"
        )

        return koneksi

    except psycopg2.Error as error:
        print("Koneksi database gagal!")
        print(error)

        return None
