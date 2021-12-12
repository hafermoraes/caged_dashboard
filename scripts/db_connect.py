#!/usr/bin/python3
import sqlite3

def sql_connection():
    try:
        conn = sqlite3.connect('../data/caged.db')
        return conn
    except Error:
        print(Error)
