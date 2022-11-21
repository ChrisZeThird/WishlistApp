# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 18:46:54 2022

@author: ChrisZeThird
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk

import sqlite3 as sql

from DataBase import create_table, distinct, fetch_items, remove_element, remove_list
from Center import center

import os

class WishList():
    
    def __init__(self):
        
        self.directory = os.getcwd() # get current working directory
        
        ## SQL database
        self.db = sql.connect(f'{self.directory}\main.sqlite') # connect to the db file
        self.init_cursor = self.db.cursor()
        self.init_cursor.execute("CREATE TABLE IF NOT EXISTS Wishtable(list_id TEXT, name TEXT, price TEXT, url TEXT)")
        self.init_cursor.close() # we will keep the database open until we quit the app
        
        ## Parameters
        self.wishlist_names = distinct(self.db) # initiate the list of wishlists names
        self.item_names = distinct(self.db,c='name')
        self.bg_colour = "#1C1919" # avoid repetition and easier to remember

        self.logo_path = f'{self.directory}\BoChrisSticker.png'
        
        self.count = 0 # useful parameter for tree view and adding rows
        
        ## Tkinter window
        self.w = 800 # width
        self.h = 800 # height
        self.main_menu = tk.Tk()
        self.main_menu.title("Wishlists explorer")
        self.main_menu.geometry('800x800')
        center(self.main_menu) # centers the window on the screen properly
        
        self.MainFrame()
        
        self.main_menu.mainloop()
        
    """ Utility Methods """
    
    def clearTKlabel(self, label):
        label['text'] = ""
    
    def addtolist(self, L, x):
        if x not in L:
            L.append(x)
    
    def removefromlist(self, L, x):
        if x in L:
            L.remove(x)
            remove_cursor = self.db.cursor()
            remove_cursor.execute("DELETE FROM Wishtable WHERE list_id = name")
            remove_cursor.close()
    
    def get_entry(self, e):
        return e.get()
    
    def closeapp(self):
        self.main_menu.destroy()
        self.db.close()
    
    ## Get selected items in a ListBox
    def selected_item(self, listbox):
        for i in listbox.curselection():
            return listbox.get(i)
    
    def remove_widget(self, frame):
        for widget in frame.winfo_children():
            widget.destroy
    
    def back(self, frame, tree=None):
        if tree is not None:
            tree.delete(*tree.get_children())
        self.remove_widget(frame)
        self.MainFrame()
    
    ## Methods for Tree
    
    def insert_row_tk(self, tree, rows):
        for row in rows:
            if self.count % 2 == 0:
                tree.insert("", tk.END, values=row, tags=('evenrow',))
            else:
                tree.insert("", tk.END, values=row, tags=('oddrow',))
            self.count += 1
    
    def remove_tree(self,tree):
        tree.delete(*tree.get_children())
    
    def remove_all(self, tree, wishlistname):
        self.remove_tree(tree)
        remove_list(self.db, wishlistname)
        self.wishlist_names.remove(wishlistname)
        self.MainFrame()
        
    def remove_row_from_tree(self, tree, list_name):
        ## By default the number of deleted row is one
        rows = tree.selection()
        # curItem = tree.focus()
        # values = tree.item(curItem)['values']

        for item in rows:
            # print(row)
            # print(values[0])
            values = tree.item(item,"values")
            remove_element(self.db, values[0], list_name) # first elements of values is the name of the item
            tree.delete(item)      
            self.count -=1
    
    def addrecord(self, tree, wishlistname, namebox, pricebox, urlbox):
        if self.count % 2 == 0:
            tree.insert(parent='', index='end', iid=self.count, text='', values=(namebox.get(), pricebox.get(), urlbox.get()), tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=self.count, text='', values=(namebox.get(), pricebox.get(), urlbox.get()), tags=('oddrow',))
        create_table(self.db, wishlistname, namebox.get(), pricebox.get(), urlbox.get())
        self.count += 1
        ## Clear the boxes
        namebox.delete(0, tk.END)
        pricebox.delete(0, tk.END)
        urlbox.delete(0, tk.END)
            
    """ Creating the different frames """
    
    def MainFrame(self):
        self.main_frame = tk.Frame(self.main_menu, width=self.w, height=self.h, bg=self.bg_colour)
        self.main_frame.tkraise()
        self.main_frame.grid(row=0, column=0, sticky='nesw')
        self.main_frame.pack_propagate(False) # prevent child from modifying parent

        ## Adding logo to main frame
        self.logo_img = (Image.open(self.logo_path))
        self.resized_img = self.logo_img.resize((150,150))
        self.new_logo_img = ImageTk.PhotoImage(self.resized_img)

        self.logo_widget = tk.Label(self.main_frame, image=self.new_logo_img, bg=self.bg_colour)
        self.logo_widget.image = self.new_logo_img
        self.logo_widget.pack()
        
        ## Adding list box for the names 
        self.theList = tk.Listbox(self.main_frame, selectmode=tk.SINGLE)
        self.theList.pack()
        
        for lists in self.wishlist_names:
            self.theList.insert(0, lists)

        ## Adding "add list" button
        tk.Button(self.main_frame, text="Add Wishlist", font=("TkHeadingFont",15), bg="#28393a",fg="White",cursor="hand2",activebackground="#badee2",activeforeground="black",command=self.NewTableName).pack(pady=2)
        
        # ## Adding "add items" button
        # tk.Button(self.main_frame, text="Add items", font=("TkHeadingFont",15), bg="#28393a",fg="White",cursor="hand2",activebackground="#badee2",activeforeground="black",command=self.NewItemFrame).pack(pady=2)
        
        ## Adding "Modify Wishlist" button
        tk.Button(self.main_frame, text="Modify Wishlist", font=("TkHeadingFont",15), bg="#28393a",fg="White",cursor="hand2",activebackground="#badee2",activeforeground="black",command=self.ModifyListFrame).pack(pady=2)
        
        ## Displays warning if there is no wishlist
        self.label_warning_main = tk.Label(self.main_frame, bg=self.bg_colour, fg="Red").pack(pady=2)
        
        ## Adding exit button
        tk.Button(self.main_frame, text="EXIT", font=("TkHeadingFont",10), bg="#28393a",fg="White",cursor="hand2",activebackground="#badee2",activeforeground="red",command=self.closeapp).pack(pady=2)
        
    
    def NewTableName(self):
        self.add_table_frame = tk.Frame(self.main_menu, width=self.w, height=self.h, bg=self.bg_colour)
        self.add_table_frame.tkraise()
        self.add_table_frame.grid(row=0, column=0, sticky='nesw')
        self.add_table_frame.pack_propagate(False) # prevent child from modifying parent
        
        ## Adding simple label
        tk.Label(self.add_table_frame, text="Add a new Wishlist", bg=self.bg_colour, fg="White", font=("TkMenuFont",14)).pack()
        
        ## Adding entry boxes
        self.list_name_entry = tk.Entry(self.add_table_frame, width=10)
        self.list_name_entry.pack(pady=5)

        add_entry = tk.Button(self.add_table_frame, text='Add', command=lambda: self.addtolist(self.wishlist_names,self.get_entry(self.list_name_entry)))
        add_entry.pack()
        
        ## Adding exit button
        tk.Button(self.add_table_frame, text="BACK", font=("TkHeadingFont",10), bg="#28393a",fg="White",cursor="hand2",activebackground="#badee2",activeforeground="red",command=lambda: self.back(self.add_table_frame)).pack(pady=5)

## This is useless since now I have a modify wishlist button and method, feels redundent to have also an add item
    # def NewItemFrame(self):
    #     if len(self.wishlist_names) == 0:
    #         self.label_warning_main['text'] = "Add Wishlist before adding Items"
    #         self.main_menu.after(2000, lambda: self.clearTKlabel(self.label_warning_main))
        
    #     else:
    #         self.add_item_frame = tk.Frame(self.main_menu, width=self.w, height=self.h, bg=self.bg_colour)
    #         self.add_item_frame.tkraise()
    #         self.add_item_frame.grid(row=0, column=0, sticky='nesw')
    #         self.add_item_frame.pack_propagate(False) # prevent child from modifying parent
            
    #         ## Adding simple label
    #         tk.Label(self.add_item_frame, text="Add a new item to Wishlists", bg=self.bg_colour, fg="White", font=("TkMenuFont",14)).pack()
            
    #         ## Adding simple label
    #         tk.Label(self.add_item_frame, text="Select a Wishlist", bg=self.bg_colour, fg="White", font=("TkMenuFont",10)).pack()

    #         ## Dropdown menu
    #         self.clicked = tk.StringVar()
    #         self.drop_item = tk.OptionMenu(self.add_item_frame, self.clicked, *self.wishlist_names)
    #         self.drop_item.pack()
            
    #         ## Adding entry boxes with labels
            
    #             # Name
    #         self.item_label = tk.Label(self.add_item_frame, text="Item's Name", bg=self.bg_colour, fg="White", font=("TkMenuFont",10)).pack(pady=1)
    #         self.item_name_entry = tk.Entry(self.add_item_frame, width=10)
    #         self.item_name_entry.pack(pady=2)
            
    #             # Price
    #         self.price_label = tk.Label(self.add_item_frame, text="Item's Price", bg=self.bg_colour, fg="White", font=("TkMenuFont",10)).pack(pady=1)
    #         self.item_price_entry = tk.Entry(self.add_item_frame, width=10)
    #         self.item_price_entry.pack(pady=2)
                
    #             # URL
    #         self.url_label = tk.Label(self.add_item_frame, text="Item's URL", bg=self.bg_colour, fg="White", font=("TkMenuFont",10)).pack(pady=1)
    #         self.item_url_entry = tk.Entry(self.add_item_frame, width=10)
    #         self.item_url_entry.pack(pady=2)

    #         ## Confirm button
    #         add_entry = tk.Button(self.add_item_frame, text='Add', command=lambda: create_table(self.db, self.clicked.get(), self.item_name_entry.get(), self.item_price_entry.get(), self.item_url_entry.get()))
    #         add_entry.pack()
            
    #         ## Adding exit button
    #         tk.Button(self.add_item_frame, text="BACK", font=("TkHeadingFont",10), bg="#28393a",fg="White",cursor="hand2",activebackground="#badee2",activeforeground="red",command=lambda: self.back(self.add_item_frame)).pack(pady=5)            
        
    def ModifyListFrame(self):
        self.wishlist_name = self.selected_item(self.theList)
        (self.main_frame)
        
        ## Creating frame
        self.modify_item_frame = tk.Frame(self.main_menu, width=self.w, height=self.h, bg=self.bg_colour)
        self.modify_item_frame.tkraise()
        self.modify_item_frame.grid(row=0,column=0, sticky='nesw')
        self.modify_item_frame.pack_propagate(False) # prevent child from modifying parent
        
        ## Adding treeview frame
        tree_frame = tk.Frame(self.modify_item_frame, bg=self.bg_colour)
        tree_frame.pack(pady=10)
        
            # Create scrollbar
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        ## Adding treeview
        temp = fetch_items(self.db, self.wishlist_name)
        items = [elmt[1:] for elmt in temp]
        
        ## Add style to treeview 
        style = ttk.Style() 
            
            # Pick a theme
        style.theme_use('clam')
            # Configure treeview colours 
        style.configure("Treeview", background="white", foreground="black",rowheight=20,fieldbackground="white")
    
        style.map('Treeview', background=[('selected', '#E9A003')])
            
            # Create treeview
        tree= ttk.Treeview(tree_frame, column=("column1", "column2", "column3"), show='headings', yscrollcommand=tree_scroll.set) # commits style to the Treeview
        
        
            # Configure scrollbar
        
        tree_scroll.config(command=tree.yview)
        
            # Create striped row tags
        tree.tag_configure('evenrow', background='#EB5937')
        tree.tag_configure('oddrow', background='white')
        
        tree.heading("#1", text="Item's Name")
        tree.heading("#2", text="Price")
        tree.heading("#3", text="Wesbite")

        self.insert_row_tk(tree,items)
        tree.pack()
        
        ## Add new frame for widgets
        widgets_frame = tk.Frame(self.modify_item_frame, bg=self.bg_colour)
        widgets_frame.pack()
        
        ## Adding labels
        name_label = tk.Label(widgets_frame, text="Item's Name", bg=self.bg_colour, fg="White", font=("TkMenuFont",10))
        name_label.grid(row=1,column=0, padx=5, pady=5)
        
        price_label = tk.Label(widgets_frame, text="Item's Price", bg=self.bg_colour, fg="White", font=("TkMenuFont",10))
        price_label.grid(row=1,column=1, padx=5 ,pady=5)
        
        url_label = tk.Label(widgets_frame, text="URL", bg=self.bg_colour, fg="White", font=("TkMenuFont",10))
        url_label.grid(row=1,column=2, padx=5, pady=5)
        
        ## Adding entry boxes
        name_box = tk.Entry(widgets_frame)
        name_box.grid(row=2,column=0, padx=5, pady=5)
        
        price_box = tk.Entry(widgets_frame)
        price_box.grid(row=2,column=1, padx=5, pady=5)
        
        url_box = tk.Entry(widgets_frame)
        url_box.grid(row=2,column=2, padx=5, pady=5)
        
        ## Adding edit button
        add_record = tk.Button(widgets_frame, text="Add Record", font=("TkHeadingFont",10), bg="#28393a",fg="White",cursor="hand2",activebackground="#badee2",activeforeground="red",command=lambda: self.addrecord(tree, self.wishlist_name, name_box, price_box, url_box))         
        add_record.grid(row=3,column=1,pady=10)
        
        ## Adding removing buttons
        remove_button = tk.Button(widgets_frame, text="Remove Selected Item(s)", font=("TkHeadingFont",10), bg="#28393a",fg="White",cursor="hand2",activebackground="#badee2",activeforeground="red",command=lambda: self.remove_row_from_tree(tree, self.wishlist_name))           
        remove_button.grid(row=4,column=1,pady=10)
        
        remove_all_button = tk.Button(widgets_frame, text="Delete wishlist", font=("TkHeadingFont",10), bg="#28393a",fg="White",cursor="hand2",activebackground="#badee2",activeforeground="red",command=lambda: self.remove_all(tree, self.wishlist_name)) 
        remove_all_button.grid(row=5,column=1,pady=10)
        ## Adding exit button
        exit_button = tk.Button(widgets_frame, text="BACK", font=("TkHeadingFont",10), bg="#28393a",fg="White",cursor="hand2",activebackground="#badee2",activeforeground="red",command=lambda: self.back(self.modify_item_frame,tree=tree))           
        exit_button.grid(row=6,column=1)
        
        
        
        
        
        