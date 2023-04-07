import sqlite3

conn = sqlite3.connect("books.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE BOOK (
id integer PRIMARY KEY,
author TEXT NOT NULL,
language TEXT NOT NULL,
title TEXT NOT NULL
)"""
cursor.execute(sql_query)