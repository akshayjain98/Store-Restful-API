import sqlite3

connection = sqlite3.connect("store.db")
cursor = connection.cursor()

# create user table
create_query = "create table if not exists user_tbl(id integer primary key autoincrement, name text, email text," \
               " password text)"
cursor.execute(create_query)

# create item table
create_query = "create table if not exists item_tbl(id integer primary key autoincrement, name text, price text)"
cursor.execute(create_query)


connection.commit()
connection.close()