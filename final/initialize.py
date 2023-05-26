#!/usr/bin/env python3
from os import chdir
chdir(r"C:\Users\felix\Desktop\ENS\Cours\L3\BDD\Projet_BDD\Code Projet\final")

# connect to the database
from config import config
import psycopg2
from datetime import date

params = config()
conn = psycopg2.connect(**params)
conn.autocommit = True

class AdminButton:

    def __init__(self) :
        self.init_users()
        self.init_topics()
        self.init_loc()
        self.init_internships()
        self.init_marks()
        print("Everything has been initialised")


    def init_users(self):


        cursor = conn.cursor()
        query = """DROP TABLE IF EXISTS users CASCADE;
            CREATE TABLE users (
            user_id serial PRIMARY KEY,
            fname varchar(150),
            lname varchar(150),
            email varchar(100) UNIQUE NOT NULL,
            password varchar(50) NOT NULL,
            role varchar(20) NOT NULL
            );"""

        cursor.execute(query)

        query_add_me = """
            INSERT INTO users(fname, email, password, role) VALUES(%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """
        records_to_insert = [("moi", "moi@moi.moi", "moiaussi","student"),
                             ("admin", "admin@admin.admin", "admin","student"),
                             ("pasmoi", "pasmoi@gmail.com", "toujourspasmoi", "researcher"),
                             ("pasmoi2", "pasmoi2@gmail.com", "toujourspasmoi", "researcher")]

        for record_to_insert in records_to_insert :
            cursor.execute(query_add_me, record_to_insert)
        cursor.close()

    def init_loc(self) :
        cursor = conn.cursor()
        query = """DROP TABLE IF EXISTS loc CASCADE;
            CREATE TABLE loc (
            country varchar(100),
            city varchar(100),
            date_start INT NOT NULL,
            date_end INT DEFAULT NULL,
            lab varchar(250),
            r_id INT REFERENCES users(user_id)
            );"""

        cursor.execute(query)

        query_add_topic = """
            INSERT INTO loc(country, city, date_start, date_end, lab, r_id) VALUES(%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """
        records_to_insert = [("Fronçe", "Gif-sur-Yvette", int("2022" + "09"+"12"), int("2024" + "12"+"12"), "lmf", 3),
                        ("Allemagne", "Munich",
int(str(date.today().year) + str(date.today().month)+ str(date.today().day)), None, "", 3),
                        ("PASFronçe", "Gif-sur-Yvette", int("2022" + "09"+"12"), int("2024" + "12"+"12"), "", 4)]

        for record_to_insert in records_to_insert :
            cursor.execute(query_add_topic, record_to_insert)
        cursor.close()

    def init_topics(self):
        cursor = conn.cursor()
        query = """DROP TABLE IF EXISTS topics CASCADE;
            CREATE TABLE topics (
            topic_id serial PRIMARY KEY,
            title varchar(250) UNIQUE NOT NULL
            );"""

        cursor.execute(query)

        query_add_topic = """
            INSERT INTO topics(title) VALUES(%s)
            ON CONFLICT DO NOTHING
            """
        records_to_insert = [("BDD",),
                        ("pasBDD",)]

        for record_to_insert in records_to_insert :
            cursor.execute(query_add_topic, record_to_insert)
        cursor.close()

    def init_internships(self) :
        cursor = conn.cursor()
        query = """DROP TABLE IF EXISTS internships CASCADE;
            CREATE TABLE internships (
            int_id serial PRIMARY KEY,
            title varchar(500) UNIQUE NOT NULL,
            descr varchar(1200) NOT NULL,
            r_id INT REFERENCES users(user_id),
            url varchar(250)
            );"""

        cursor.execute(query)

        query_add_topic = """
            INSERT INTO internships(title, descr, r_id, url) VALUES(%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """
        records_to_insert = [("projet BDD", "A project to practice BDD and enjoy as much as possible life in order to get enough ects :) please give me the points", 3, "https://admin.dptinfo.ens-cachan.fr/accueil.php"),
                        ("pas projet BDD", "un projet qui n'a absolument rien à voir avec le précédent, ici personne ne valide son année, c'est maaaaaal !", 4, "")]

        for record_to_insert in records_to_insert :
            cursor.execute(query_add_topic, record_to_insert)



        # now we bind with topic
        query2 = """DROP TABLE IF EXISTS i_tops CASCADE;
            CREATE TABLE i_tops (
            i_id INT REFERENCES internships(int_id),
            t_id INT REFERENCES topics(topic_id),
            PRIMARY KEY (i_id,t_id)
            );"""

        cursor.execute(query2)

        query_add_topic2 = """
            INSERT INTO i_tops(i_id, t_id) VALUES(%s, %s)
            ON CONFLICT DO NOTHING
            """
        records_to_insert2 = [(1,1),(2,2)]

        for record_to_insert in records_to_insert2 :
            cursor.execute(query_add_topic2, record_to_insert)


        cursor.close()

    def init_marks(self) :
        cursor = conn.cursor()
        query = """DROP TABLE IF EXISTS marks;
            CREATE TABLE marks (
            r_id INT REFERENCES users(user_id) NOT NULL,
            s_id INT REFERENCES users(user_id) NOT NULL,
            mark INT NOT NULL,
            UNIQUE (r_id, s_id)
            );"""

        cursor.execute(query)

        query_add_topic = """
            INSERT INTO marks(s_id, r_id, mark) VALUES(%s, %s, %s)
            ON CONFLICT DO NOTHING
            """
        records_to_insert = [(1,3,10), (1,4,9), (2,3,0),(2,4,3)]

        for record_to_insert in records_to_insert :
            cursor.execute(query_add_topic, record_to_insert)
        cursor.close()


if __name__ == "__main__" :
    AdminButton()
    cursor = conn.cursor()

    cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    print (cursor.fetchall())
    print()

    cursor.execute("SELECT * from users;")
    print(cursor.fetchall())
    print()
    cursor.execute("SELECT * from loc;")
    print(cursor.fetchall())
    print()
    cursor.execute("SELECT lab from loc;")
    print(cursor.fetchall())
    print()

    cursor.execute("SELECT r_id, AVG(mark) from marks GROUP BY r_id;")
    print(cursor.fetchall())
    print()

