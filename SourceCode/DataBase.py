# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 11:25:42 2022

@author: ChrisZeThird
"""
# import sqlite3 as sql

""" Methods """

def create_table(db, list_name, item_name, item_price, item_url):
    cursor = db.cursor()
    cursor.execute('INSERT INTO Wishtable VALUES (?,?,?,?)',(list_name, item_name, item_price, item_url))
    db.commit()
    cursor.close()

def distinct(db,c='list_id'):
    cursor = db.cursor()
    cursor.execute(f"SELECT DISTINCT {c} FROM Wishtable ORDER BY {c}")

    data=cursor.fetchall()
    COLUMN = 0
    
    all_lists = [elt[COLUMN] for elt in data]
    # print(all_lists)
    cursor.close()
    return all_lists

def remove_element(db, item_name, list_name):
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM Wishtable WHERE list_id = '{list_name}' AND name = '{item_name}'")
    db.commit()
    cursor.close()

def remove_list(db, list_name):
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM Wishtable WHERE list_id = '{list_name}'")
    db.commit()
    cursor.close()
    
    
def fetch_items(db, list_name):
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM Wishtable WHERE list_id = "{list_name}"')
    items = cursor.fetchall()
    cursor.close()
    return items
    