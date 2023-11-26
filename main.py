import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import datetime
import sqlite3


def add_products(id, name, desc, price, stock):
    with open('productsdb/'+id+'.name', 'w+') as f:
        f.write(name)
        f.close()
    with open('productsdb/'+id+'.description', 'w+') as f:
        f.write(desc)
        f.close()
    with open('productsdb/'+id+'.price', 'w+') as f:
        f.write(price)
        f.close()
    with open('productsdb/'+id+'.stock', 'w+') as f:
        f.write(stock)
        f.close()

def history_append(id, name, price):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS history(id TEXT, name TEXT, price TEXT, time TEXT)')
    c.execute("INSERT INTO history(id, name, price, time) VALUES(?, ?, ?, ?)", [id, name, price, datetime.datetime.now()])
    conn.commit()
    c.close()
    conn.close()

def history_fetchid():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS history(id TEXT, name TEXT, price TEXT, time TEXT)')
    c.execute("SELECT id FROM history")
    rows = []
    for row in c.fetchall():
        tempdata = row
        for list in tempdata:
                        rows.append(list)
    c.close()
    conn.close()
    return rows

def history_fetchname():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS history(id TEXT, name TEXT, price TEXT, time TEXT)')
    c.execute("SELECT name FROM history")
    rows = []
    for row in c.fetchall():
        tempdata = row
        for list in tempdata:
                        rows.append(list)
    c.close()
    conn.close()
    return rows

def history_fetchprice():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS history(id TEXT, name TEXT, price TEXT, time TEXT)')
    c.execute("SELECT price FROM history")
    rows = []
    for row in c.fetchall():
        tempdata = row
        for list in tempdata:
                        rows.append(list)
    c.close()
    conn.close()
    return rows

def history_fetchtime():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS history(id TEXT, name TEXT, price TEXT, time TEXT)')
    c.execute("SELECT time FROM history")
    rows = []
    for row in c.fetchall():
        tempdata = row
        for list in tempdata:
                        rows.append(list)
    c.close()
    conn.close()
    return rows

def clear_history():  
    os.remove("history.db")
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS history(id TEXT, name TEXT, price TEXT, time TEXT)')
    conn.commit()
    c.close()
    conn.close()

def del_products(id):
    os.remove('productsdb/'+id+'.name')
    os.remove('productsdb/'+id+'.description')
    os.remove('productsdb/'+id+'.price')
    os.remove('productsdb/'+id+'.stock')

def get_product_info(id):
    name = ""
    desc = ""
    price = 0.0
    stock = 0
    with open('productsdb/'+id+'.name', 'r') as f:
        name = f.read()
        f.close()
    with open('productsdb/'+id+'.description', 'r') as f:
        desc = f.read()
        f.close()
    with open('productsdb/'+id+'.price', 'r') as f:
        price = f.read()
        f.close()
    with open('productsdb/'+id+'.stock', 'r') as f:
        stock = f.read()
        f.close()
    
    return [name, desc, price, stock]

def get_list():
    listdir = os.listdir('productsdb')
    return listdir

def clear():
    listdir = os.listdir('productsdb')
    for product in listdir:
        os.remove('productsdb/'+product)
import pyautogui

window = tk.Tk()
window.title("Ahnaf Retail")
window.geometry("900x600")
window.resizable(0, 0)

from operator import contains
return_cash = 0

tabController = ttk.Notebook(window)
global_shop_list = []
global_name_list = []
global_price_list = []
  
tab1 = ttk.Frame(tabController)
tab2 = ttk.Frame(tabController)
tab3 = ttk.Frame(tabController)
  
tabController.add(tab1, text =' Buy ')
tabController.add(tab2, text =' Products Management ')
tabController.add(tab3, text =' History ')
tabController.pack(expand=1, fill="both")

#====================== DELETE ITEM HANDLE =====================#
def delete_item(event):
    if event.keycode == 46:
        try:
            for item in product_table.get_children():
                product_table.delete(item)
                cash.set("")
                var_id_tab1.set("")
                changes.set("")
                global_price_list = []
                global_price_list = []
                global_name_list = []
                global_shop_list = []
        except:
         messagebox.showerror("Ahnaf Retail", "Error!, Cannot delete item.")
window.bind("<Key>", delete_item)
def clr_item():
    try:
        for item in product_table.get_children():
            product_table.delete(item)
            cash.set("")
            var_id_tab1.set("")
            changes.set("")
            global_price_list = []
            global_name_list = []
            global_shop_list = []
    except:
        messagebox.showerror("Ahnaf Retail", "Error!, Cannot delete item.")

def tabswitch_handle(event):
    curr_tab = event.widget.tab('current')['text']
    if curr_tab == ' History ':
        for item in history_table.get_children():
                history_table.delete(item)
        names = history_fetchname()
        prices = history_fetchprice()
        times = history_fetchtime()
        ids = history_fetchid()
        amount = 0
        for i in history_fetchid():
            amount += 1
        for i in range(amount):
                        history_table.insert(parent='', index='end',text="", values=(ids[i], names[i], prices[i], times[i]))
        amount = 0
tabController.bind('<<NotebookTabChanged>>', tabswitch_handle)
#====================== TEXT CHANGE HANDLE =====================#
def on_text_change(*args):
    id = var_id_tab1.get()
    if id == "":
        var_warn_tab1.set("")
    else:
        try:
            temp_test_val = int(id)
            if len(id) > 9:
                try:
                    info = get_product_info(id)
                    global_price_list.append(info[2])
                    product_table.insert(parent='', index='end',text="", values=(id, info[0], info[1], info[2]+".RP"))
                    del_products(id)
                    global_shop_list.append(id)
                    global_name_list.append(info[0])
                except:
                    if id == "0012510372":
                        pay()
                        end_transaction()
                    elif id == "0011901406":
                        clr_item()
                    else:
                        var_warn_tab1.set("Product ID Not Found")
                var_id_tab1.set("")
            else:
                var_warn_tab1.set("")
        except:
            var_warn_tab1.set("Invalid Product ID")

def pay():
    money_amount = cash.get()
    try:
        cashint = int(money_amount)
        total = 0
        for item in global_price_list:
            temps = int(item)
            total = total + temps
        return_cash = cashint - int(total)
        changes.set(return_cash)
    except:
        messagebox.showerror("Ahnaf Retail", "Invalid cash amount.")
    var_id_tab1.set("")
def end_transaction():
    if global_shop_list == []:
        messagebox.showerror("Ahnaf Retail", "Invalid Transaction.")
    else:
        counts = 0
        for item in global_shop_list:
            counts =+ 1
        for i in range(counts):
            history_append(global_shop_list[i], global_name_list[i], global_price_list[i])
        counts == 0
        for item in product_table.get_children():
            product_table.delete(item)
        cash.set("")
        var_id_tab1.set("")
        changes.set("")
        messagebox.showinfo("Ahnaf Retail", "Transaction Success.")
#=========================== TAB 1 =============================#
var_warn_tab1 = StringVar()
warninglbl = ttk.Label(tab1, textvariable=var_warn_tab1, foreground="#ee3838").grid(row=3, column=0, padx=120, pady=0)
ttk.Label(tab1, text="").grid(row=0, column=0, padx=50, ipady=0)
ttk.Label(tab1, text="Product ID : ").grid(row=1, column=0, padx=45, ipady=0)
var_id_tab1 = StringVar()
entryid = ttk.Entry(tab1, width=50, textvariable=var_id_tab1)
entryid.focus()
entryid.grid(row=2, column=0, padx=0, pady=10)
var_id_tab1.trace("w", on_text_change)
product_table = ttk.Treeview(tab1)
product_table['columns'] = ("ID", "Name", "Description", "Price")
product_table.column("#0", anchor=W, width=0)
product_table.column("ID", anchor=CENTER, width=120)
product_table.column("Name", anchor=W, width=200)
product_table.column("Description", anchor=W, width=250)
product_table.column("Price", anchor=W, width=120)
product_table.heading("#0", text="", anchor=W)
product_table.heading("ID", text="ID", anchor=CENTER)
product_table.heading("Name", text="Name", anchor=W)
product_table.heading("Description", text="Description", anchor=W)
product_table.heading("Price", text="Price", anchor=W)
product_table.grid(row=4, column=0, padx=40, pady=10)
ttk.Label(tab1, text="Cash : ").grid(row=6, column=0, padx=40, pady=15, sticky=W)
cash = StringVar()
ttk.Entry(tab1, width=30, textvariable=cash).grid(row=6, column=0, pady=15, padx=5)
ttk.Label(tab1, text="Changes : ").grid(row=7, column=0, padx=40, pady=10, sticky=W)
changes = StringVar()
ttk.Entry(tab1, width=30, textvariable=changes, state=DISABLED).grid(row=7, column=0, pady=10, padx=5)
ttk.Button(tab1, text="Clear", width="10", command=clr_item).grid(row=2, column=0, padx=80, pady=0, sticky=E)
ttk.Button(tab1, text="Pay", width="10", command=pay).grid(row=2, column=0, padx=0, pady=0, sticky=E)
ttk.Button(tab1, text="Finish Transaction", width="35", command=end_transaction).grid(row=8, column=0, padx=0, pady=0, sticky=E)
#===============================================================#
#------------------------- Title Start -------------------------#
ttk.Label(tab2, text=" - Product Input - ", font='Helvetica 18 bold').grid(row=0, column=1, padx=80, pady=10)
#-------------------------- Title End --------------------------#
#---------------------- Product Input Start --------------------#
ttk.Label(tab2, text="Product Name : ").grid(row=1, column=0, padx=50, pady=10) # Product Name Label
prod_name = StringVar()  # Product Name Variable
ttk.Entry(tab2, width=50, textvariable=prod_name).grid(row=1, column=1, pady=5, padx=2) # Product Name Entry
ttk.Label(tab2, text="Description : ").grid(row=2, column=0, padx=50, pady=10) # Description Label
desc = StringVar() # Description Variable
ttk.Entry(tab2, width=50, textvariable=desc).grid(row=2, column=1, pady=5, padx=2) # Description Entry
ttk.Label(tab2, text="Price : ").grid(row=3, column=0, padx=50, pady=10) # Description Label
price = StringVar() # Price Variable
ttk.Entry(tab2, width=50, textvariable=price).grid(row=3, column=1, pady=5, padx=2) # Price Entry
ttk.Label(tab2, text="Product ID : ").grid(row=4, column=0, padx=50, pady=20) # Product ID Label
prod_id = StringVar() # Product ID Variable
entry1 = ttk.Entry(tab2, width=50, textvariable=prod_id).grid(row=4, column=1, pady=25, padx=2) # Product ID Entry
keep_values = StringVar() # Keep Values Check Variable
ttk.Label(tab2, text="Keep Values : ").grid(row=5, column=0, padx=50, pady=10) # Product ID Label
ttk.Checkbutton(tab2, variable=keep_values,).grid(row=5, column=1, pady=5, padx=2, sticky=W) # Keep Values Checkbox
#---------------------- Product Input End ---------------------#
def delete_product(*args):
    if len(id_del.get()) > 9:
        try:
            temp = int(id_del.get())
            del_products(id_del.get())
            id_del.set("")
        except:
            id_del.set("")
            messagebox.showerror("Ahnaf Retail", "Error! Invalid Product ID")
    else:
        pass

def clear_product():
    confirm = messagebox.askyesno("Ahnaf Retail", "Clear Database Confirmation ?\nThis action is irreversable.")
    if confirm == True:
        clear()
    else:
        pass
def clear_values():
    prod_name.set("")
    desc.set("")
    price.set("")
#--------------------- Product Delete Start -------------------#
ttk.Label(tab2, text=" - Delete Product - ", font='Helvetica 18 bold').grid(row=6, column=1, padx=80, pady=20)
ttk.Label(tab2, text="Product ID : ").grid(row=7, column=0, padx=50, pady=10) # Description Label
id_del = StringVar() # Description Variable
ttk.Entry(tab2, width=50, textvariable=id_del).grid(row=7, column=1, pady=5, padx=2) # Description Entry
id_del.trace("w", delete_product)
ttk.Button(tab2, text="Clear Database", command=clear_product).grid(row=8, column=1, padx=55, pady=30, sticky=W)
ttk.Button(tab2, text="Clear Values", command=clear_values).grid(row=8, column=1, padx=160, pady=30, sticky=W)
#---------------=------ Product Delete End --------------------#
#--------------------- Database Input Start -------------------#
def input_product(*args):
    if len(prod_id.get()) > 9:
        try:
            tempvar = int(prod_id.get())
            if prod_name.get() == "":
                messagebox.showwarning("Ahnaf Retail", "Please input name!")
                prod_id.set("")
            elif desc.get() == "":
                messagebox.showwarning("Ahnaf Retail", "Please input description!")
                prod_id.set("")
            elif price.get() == "":
                messagebox.showwarning("Ahnaf Retail", "Please input price!")
                prod_id.set("")
            else:
                try:
                    add_products(prod_id.get(), prod_name.get(), desc.get(), price.get(), "")
                    if keep_values.get() == "1":
                        prod_id.set("")
                    else:
                        prod_name.set("")
                        desc.set("")
                        price.set("")
                        prod_id.set("")
                except:
                    prod_id.set("")
                    messagebox.showerror("Ahnaf Retail", "Error! Cannot save data")
        except:
            prod_id.set("")
            messagebox.showerror("Ahnaf Retail", "Error! Invalid Product ID")
#---------------------- Database Input End --------------------#
#-------------------- Database Trigger Start ------------------#
prod_id.trace("w", input_product)
#price.trace("w", input_product)
#--------------------- Database Trigger End -------------------#
#========================== TAB 3 =============================#
ttk.Label(tab3, text="Transaction History : ").grid(row=0, column=0, padx=50, pady=30)
history_table = ttk.Treeview(tab3)
history_table['columns'] = ("ID", "Name", "Price", "Time")
history_table.column("#0", anchor=W, width=0)
history_table.column("ID", anchor=CENTER, width=120)
history_table.column("Name", anchor=W, width=200)
history_table.column("Price", anchor=W, width=150)
history_table.column("Time", anchor=W, width=240)
history_table.heading("#0", text="", anchor=W)
history_table.heading("ID", text="ID", anchor=CENTER)
history_table.heading("Name", text="Name", anchor=W)
history_table.heading("Price", text="Price", anchor=W)
history_table.heading("Time", text="Time", anchor=W)
history_table.grid(row=2, column=0, padx=90, pady=10)
names = history_fetchname()
prices = history_fetchprice()
times = history_fetchtime()
ids = history_fetchid()
amount = 0
for i in history_fetchid():
    amount += 1
for i in range(amount):
                history_table.insert(parent='', index='end',text="", values=(ids[i], names[i], prices[i], times[i]))
amount = 0
ttk.Button(tab3, text="Clear History", command=clear_history).grid(row=3, column=0, padx=90, pady=10, sticky=W)
#===============================================================#


window.mainloop()
