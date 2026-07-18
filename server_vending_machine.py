#REEM MOHAMMED M00982216

#import modules
import socket 
import csv  
from datetime import datetime
import os

class VendingMachineServer: #Define a class for the Vending Machine Server
    def __init__(self):
        #Load items from the CSV file and create the transactions file
        self.load_items_from_file()
        self.create_transactions_file()

    
    def load_items_from_file(self): #Define a method to load items from the CSV file
        try:
            #Open and read the product.csv file to load items into memory
            with open("product.csv", "r", newline='') as file:
                reader = csv.reader(file)  
                next(reader)  
                self.items = {}  
                for row in reader:
                    name, price, quantity = row
                    self.items[name] = {"price": float(price), "quantity": int(quantity)}
        except FileNotFoundError:
            print("Error: product.csv not found. Exiting.")
            exit()

    def save_items_to_file(self): #Define a method to save items back to the CSV file
        #Open the product.csv file for writing
        with open("product.csv", "w", newline='') as file:
            writer = csv.writer(file)  
            writer.writerow(["Name", "Price", "Quantity"])  
            for name, item_info in self.items.items():
                writer.writerow([name, item_info['price'], item_info['quantity']])

    def create_transactions_file(self): #Define a method to create the transactions file
        #Check if the transactions.csv file exists, if not, create it
        if not os.path.isfile("transactions.csv"):
            with open("transactions.csv", 'w', newline='') as file:
                fieldnames = ['Timestamp', 'Product', 'Quantity', 'Amount', 'Payment Method']
                writer = csv.DictWriter(file, fieldnames=fieldnames)  
                writer.writeheader()  

    def purchase_item(self, item_info): #Define a method to process a purchase request for an item
        #Split the item_info string to extract item name and quantity
        name, quantity = item_info.split(":")
        if name in self.items:
            if int(quantity) <= 0:
                return "Invalid quantity."
            elif int(quantity) > self.items[name]["quantity"]:
                return f"Insufficient stock for {name}. Available stock: {self.items[name]['quantity']}"
            else:
                self.items[name]["quantity"] -= int(quantity)
                self.save_items_to_file()  
                return f"Successfully purchased {quantity} {name}(s)!"
        else:
            #Return an error message if the item name is not found
            return "Item not found."

    def display_items(self): #Define a method to return a string representation of available items
        return self.items

    def store_transaction(self, transaction): #Define a method to store a transaction in the transactions.csv file
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y,%H:%M:%S")
        transaction_data = transaction.split(":")
        with open("transactions.csv", "a", newline='') as file:
            writer = csv.writer(file)  
            writer.writerow([current_time, transaction_data[0], transaction_data[1], float(transaction_data[2]), int(transaction_data[3])])

def main(): #Define the main function
    # Set up the server socket
    host = '127.0.0.1' 
    port = 65432 

    # Create a TCP/IP socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    server.bind((host, port))  
    server.listen(1) #1 maximum number of queued connections

    print("Starting Vending Machine server.")

    # Accept and handle incoming connections
    while True:
        conn, addr = server.accept()  
        print(f"Connected to {addr}")

        # Create an instance of the VendingMachineServer class
        vending_machine = VendingMachineServer()

        # Receive and process data from the client
        while True:
            data = conn.recv(1024).decode()  
            if not data:
                break

            if data == "DISPLAY":
                items = vending_machine.display_items()
                response = "\n".join([f"{name}: ${item['price']} ({item['quantity']} left)" for name, item in items.items()])
                conn.sendall(response.encode())
            else:
                response = vending_machine.purchase_item(data)
                vending_machine.store_transaction(data)  
                # Send the response to the client
                conn.sendall(response.encode())

        # Close the connection with the client
        conn.close()

if __name__ == "__main__":
    # Call the main function
    main()
