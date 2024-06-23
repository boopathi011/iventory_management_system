import tkinter as tk
import mysql.connector
from tkinter import messagebox

# MySQL Connection
con_o = mysql.connector.connect(host="localhost", user="root", password="", database="inventory")
cur_o = con_o.cursor()

# Functions for `inv` table operations
def add_inventory():
    item_name = item_name_entry.get()
    item_qty = int(item_qty_entry.get())  # Convert to int
    q2 = "INSERT INTO `inv` (`item_name`, `item_quantity`) VALUES (%s, %s)"
    val = (item_name, item_qty)
    cur_o.execute(q2, val)
    con_o.commit()
    messagebox.showinfo("Success", "Item added to inventory")
    item_name_entry.delete(0, tk.END)
    item_qty_entry.delete(0, tk.END)
    calculate_final_quantities()

def update_inventory():
    item_name = item_name_entry.get()
    item_qty = int(item_qty_entry.get())  # Convert to int
    q2 = "UPDATE `inv` SET `item_quantity` = %s WHERE `item_name` = %s"
    val = (item_qty, item_name)
    cur_o.execute(q2, val)
    con_o.commit()
    messagebox.showinfo("Success", "Inventory updated")
    item_name_entry.delete(0, tk.END)
    item_qty_entry.delete(0, tk.END)
    calculate_final_quantities()

def search_inventory():
    search_name = item_name_entry.get()
    q2 = "SELECT `item_name`, `item_quantity` FROM `inv` WHERE `item_name` = %s"
    val = (search_name,)
    cur_o.execute(q2, val)
    result = cur_o.fetchone()
    if result:
        messagebox.showinfo("Inventory", f'{result[0]} - Quantity: {result[1]}')
    else:
        messagebox.showinfo("Inventory", f'{search_name} not found in inventory.')
    item_name_entry.delete(0, tk.END)

def remove_inventory():
    remove_name = item_name_entry.get()
    q2 = "DELETE FROM `inv` WHERE `item_name` = %s"
    val = (remove_name,)
    cur_o.execute(q2, val)
    con_o.commit()
    messagebox.showinfo("Success", "Item removed from inventory")
    item_name_entry.delete(0, tk.END)
    item_qty_entry.delete(0, tk.END)
    calculate_final_quantities()

def show_inventory():
    inventory_list = generate_inventory()
    result_label.config(text="")
    for item in inventory_list:
        result_label.config(text=result_label.cget("text") + f"{item[0]} - {item[1]}\n")

def generate_inventory():
    q2 = "SELECT `item_name`, `item_quantity` FROM `inv`"
    cur_o.execute(q2)
    return cur_o.fetchall()

# Function to add to `inv1` and update `inv` if item exists
def add_inventory1():
    item_name = item_name_entry.get()
    item_qty = int(item_qty_entry.get())  # Convert to int
    
    # Check if item exists in `inv1`
    q_check_inv1 = "SELECT `item_name`, SUM(`item_quantity`) FROM `inv1` WHERE `item_name` = %s GROUP BY `item_name`"
    val_check_inv1 = (item_name,)
    cur_o.execute(q_check_inv1, val_check_inv1)
    result = cur_o.fetchone()
    
    if result:
        # Item exists in `inv1`, update quantity
        current_qty = result[1]
        new_qty = current_qty + item_qty
        q_update_inv1 = "UPDATE `inv1` SET `item_quantity` = %s WHERE `item_name` = %s"
        val_update_inv1 = (new_qty, item_name)
        cur_o.execute(q_update_inv1, val_update_inv1)
        con_o.commit()
    else:
        # Item doesn't exist in `inv1`, insert into `inv1`
        q_insert_inv1 = "INSERT INTO `inv1` (`item_name`, `item_quantity`) VALUES (%s, %s)"
        val_insert_inv1 = (item_name, item_qty)
        cur_o.execute(q_insert_inv1, val_insert_inv1)
        con_o.commit()
    
    messagebox.showinfo("Success", "Item added to additional inventory")
    item_name_entry.delete(0, tk.END)
    item_qty_entry.delete(0, tk.END)
    calculate_final_quantities()

def remove_inventory1():
    remove_name = item_name_entry.get()
    q2 = "DELETE FROM `inv1` WHERE `item_name` = %s"
    val = (remove_name,)
    cur_o.execute(q2, val)
    con_o.commit()
    messagebox.showinfo("Success", "Item removed from additional inventory")
    item_name_entry.delete(0, tk.END)
    item_qty_entry.delete(0, tk.END)
    calculate_final_quantities()

# Function to calculate final quantities and update `final` table
def calculate_final_quantities():
    try:
        # Clear existing entries in `final` table
        q_clear_final = "TRUNCATE TABLE `final`"
        cur_o.execute(q_clear_final)
        con_o.commit()
        
        # Get current quantities from `inv`
        q_get_inv = "SELECT `item_name`, `item_quantity` FROM `inv`"
        cur_o.execute(q_get_inv)
        inv_items = cur_o.fetchall()
        
        # Get current quantities from `inv1`
        q_get_inv1 = "SELECT `item_name`, SUM(`item_quantity`) FROM `inv1` GROUP BY `item_name`"
        cur_o.execute(q_get_inv1)
        inv1_items = cur_o.fetchall()
        
        # Calculate final quantities and insert into `final` table
        for item_inv in inv_items:
            item_name_inv = item_inv[0]
            item_qty_inv = item_inv[1] if item_inv[1] else 0
            
            item_qty_inv1 = 0
            for item_inv1 in inv1_items:
                if item_inv1[0] == item_name_inv:
                    item_qty_inv1 = item_inv1[1]
                    break
            
            final_qty = item_qty_inv - item_qty_inv1
            
            # Insert into `final` table
            q_insert_final = "INSERT INTO `final` (`item_name`, `item_quantity`) VALUES (%s, %s)"
            val_insert_final = (item_name_inv, final_qty)
            cur_o.execute(q_insert_final, val_insert_final)
            con_o.commit()
        
        messagebox.showinfo("Success", "Final quantities updated successfully.")
    
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Function to show inventory from `inv1`
def show_inventory1():
    inventory_list = generate_inventory1()
    result_label.config(text="")
    for item in inventory_list:
        result_label.config(text=result_label.cget("text") + f"{item[0]} - {item[1]}\n")

def generate_inventory1():
    q2 = "SELECT `item_name`, `item_quantity` FROM `inv1`"
    cur_o.execute(q2)
    return cur_o.fetchall()

# Update `final` table on application startup
calculate_final_quantities()

# Tkinter GUI setup
root = tk.Tk()
root.title("Combined Inventory Management")

# Widgets for `inv` operations
item_name_label = tk.Label(root, text="Item Name:")
item_name_label.grid(row=0, column=0, padx=5, pady=5)
item_name_entry = tk.Entry(root)
item_name_entry.grid(row=0, column=1, padx=5, pady=5)
item_qty_label = tk.Label(root, text="Item Quantity:")
item_qty_label.grid(row=1, column=0, padx=5, pady=5)
item_qty_entry = tk.Entry(root)
item_qty_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add to Inventory", command=add_inventory)
update_button = tk.Button(root, text="Update Inventory", command=update_inventory)
search_button = tk.Button(root, text="Search Inventory", command=search_inventory)
remove_button = tk.Button(root, text="Remove from Inventory", command=remove_inventory)
show_inventory_button = tk.Button(root, text="Show Inventory", command=show_inventory)

add_button.grid(row=2, column=0, padx=5, pady=5)
update_button.grid(row=2, column=1, padx=5, pady=5)
search_button.grid(row=3, column=0, padx=5, pady=5)
remove_button.grid(row=3, column=1, padx=5, pady=5)
show_inventory_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Widgets for `inv1` operations
add_label = tk.Label(root, text="Additional Inventory (inv1):")
add_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
add_button1 = tk.Button(root, text="Add to inv1", command=add_inventory1)
add_button1.grid(row=6, column=0, padx=5, pady=5)
remove_button1 = tk.Button(root, text="Remove from inv1", command=remove_inventory1)
remove_button1.grid(row=6, column=1, padx=5, pady=5)
show_inventory_button1 = tk.Button(root, text="Show Inventory (inv1)", command=show_inventory1)
show_inventory_button1.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Display `final` table
final_label = tk.Label(root, text="Final Inventory:")
final_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

def show_final_inventory():
    try:
        q_final = "SELECT `item_name`, `item_quantity` FROM `final`"
        cur_o.execute(q_final)
        final_inventory = cur_o.fetchall()
        
        result_label.config(text="")
        for item in final_inventory:
            result_label.config(text=result_label.cget("text") + f"{item[0]} - Item Quantity: {item[1]}\n")
    
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

show_final_button = tk.Button(root, text="Show Final Inventory", command=show_final_inventory)
show_final_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

result_label = tk.Label(root, text="List")
result_label.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

# Run the main loop
root.mainloop()
