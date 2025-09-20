import tkinter as tk
from tkinter import messagebox
import sqlite3
import uuid

# --- Database setup ---
conn = sqlite3.connect('wallet.db')
c = conn.cursor()

# Create transactions table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS transactions
             (id TEXT, type TEXT, amount REAL, to_addr TEXT, from_addr TEXT)''')
conn.commit()

# --- Wallet Setup ---
wallet_address = str(uuid.uuid4())[:8]  # simple random wallet address
balance = 1000  # starting balance for demo
print(f"Your wallet address: {wallet_address}")
print(f"Starting balance: {balance}")
def send_crypto(to_addr, amount):
    global balance
    if amount <= 0:
        print("Amount must be positive")
        return
    if amount > balance:
        print("Insufficient balance")
        return
    balance -= amount
    c.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)",
              (str(uuid.uuid4()), 'Sent', amount, to_addr, wallet_address))
    conn.commit()
    print(f"Sent {amount} coins to {to_addr}. New balance: {balance}")

def receive_crypto(amount):
    global balance
    if amount <= 0:
        print("Amount must be positive")
        return
    balance += amount
    c.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)",
              (str(uuid.uuid4()), 'Received', amount, wallet_address, 'External'))
    conn.commit()
    print(f"Received {amount} coins. New balance: {balance}")
send_crypto("ABC123", 200)
receive_crypto(500)
def show_transactions():
    c.execute("SELECT type, amount, to_addr, from_addr FROM transactions")
    rows = c.fetchall()
    for row in rows:
        print(f"{row[0]} {row[1]} | To: {row[2]} | From: {row[3]}")
show_transactions()
root = tk.Tk()
root.title("Crypto Wallet Prototype")

# Balance Label
balance_label = tk.Label(root, text=f"Balance: {balance}")
balance_label.pack()

# Send Section
tk.Label(root, text="Send Crypto").pack()
send_to = tk.Entry(root)
send_to.pack()
send_amount = tk.Entry(root)
send_amount.pack()

def send_button_click():
    send_crypto(send_to.get(), float(send_amount.get()))
    balance_label.config(text=f"Balance: {balance}")

tk.Button(root, text="Send", command=send_button_click).pack()

# Receive Section
tk.Label(root, text="Receive Crypto").pack()
receive_amount = tk.Entry(root)
receive_amount.pack()

def receive_button_click():
    receive_crypto(float(receive_amount.get()))
    balance_label.config(text=f"Balance: {balance}")

tk.Button(root, text="Receive", command=receive_button_click).pack()

# Transaction History Section
def show_txn_gui():
    c.execute("SELECT type, amount, to_addr, from_addr FROM transactions")
    rows = c.fetchall()
    txn_text = ""
    for row in rows:
        txn_text += f"{row[0]} {row[1]} | To: {row[2]} | From: {row[3]}\n"
    messagebox.showinfo("Transactions", txn_text)

tk.Button(root, text="Show Transactions", command=show_txn_gui).pack()

root.mainloop()

