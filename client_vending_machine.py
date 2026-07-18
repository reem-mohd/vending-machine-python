#REEM MOHAMMED M00982216

#import modules/libraries
import tkinter as tk  
import csv
from tkinter import messagebox, simpledialog 
from datetime import datetime  
import matplotlib.pyplot as plt

class VendingMachineGUI: #Define a class for the Vending Machine GUI
    def __init__(self, root):  
        self.root = root  #Set the root window
        self.root.title("Vending Machine")  
        self.root.configure(bg='pink')  
        self.show_graph_button = tk.Button(root, text="Show Stock Graph", command=self.show_stock_graph, bg='white', font=("Helvetica", 14))
        #Button to show stock graph
        self.show_graph_button.grid(row=4, column=1, padx=10, pady=5)


        #Read items from CSV file and initialize selected items dictionary
        self.items_list = self.read_items_from_csv("products.csv")
        self.selected_items = {}  

        #Create and place GUI elements (labels, listboxes, buttons)
        self.available_label = tk.Label(root, text="Available Items:", bg='pink', font=("Helvetica", 16))  #Label for available items
        self.available_label.grid(row=0, column=0, padx=10, pady=5) 

        self.available_listbox = tk.Listbox(root, width=40, height=15, bg='white', font=("Helvetica", 14))  #Listbox for available items
        self.available_listbox.grid(row=1, column=0, padx=10, pady=5) 
        self.update_available_items()  

        self.selected_label = tk.Label(root, text="Selected Items:", bg='pink', font=("Helvetica", 16))  
        self.selected_label.grid(row=0, column=1, padx=10, pady=5)  

        self.selected_listbox = tk.Listbox(root, width=40, height=15, bg='white', font=("Helvetica", 14))  
        self.selected_listbox.grid(row=1, column=1, padx=10, pady=5)  

        self.select_button = tk.Button(root, text="Select Item", command=self.select_item, bg='white', font=("Helvetica", 14))  
        self.select_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)  

        self.pay_cash_button = tk.Button(root, text="Pay by Cash", command=self.pay_by_cash, bg='white', font=("Helvetica", 14))  #Button for cash payment
        self.pay_cash_button.grid(row=3, column=0, padx=10, pady=5)  

        self.pay_card_button = tk.Button(root, text="Pay by Card", command=self.pay_by_card, bg='white', font=("Helvetica", 14))  #Button for card payment
        self.pay_card_button.grid(row=3, column=1, padx=10, pady=5)  

        self.cancel_button = tk.Button(root, text="Cancel Purchase", command=self.cancel_purchase, bg='white', font=("Helvetica", 14))
        #Button to cancel purchase
        self.cancel_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)  

    def read_items_from_csv(self, filename): #Method to read items from CSV file
        items_list = []  
        with open(filename, newline='') as csvfile:  
            reader = csv.reader(csvfile)  
            next(reader)  
            for row in reader:  
                items_list.append({"code": row[0], "name": row[1], "price": float(row[2]), "stock": int(row[3])})  #Append item data to the list
        return items_list  

    def update_available_items(self): #Method to update available items in the listbox
        self.available_listbox.delete(0, tk.END)  #Clear the contents of listbox
        for item in self.items_list:  
            self.available_listbox.insert(tk.END, f"{item['name']} - ${item['price']} - Quantity: {item['stock']}")  

    def show_stock_graph(self):  #Method to generate and display the stock graph
        #Extract product names and stock levels
        product_names = [item['name'] for item in self.items_list]
        stock_levels = [item['stock'] for item in self.items_list]

        #Create a bar chart (Product_names on x-axis and stock on y-axis)
        plt.bar(product_names, stock_levels)
        plt.xlabel('Products')
        plt.ylabel('Stock Level')
        plt.title('Stock Levels of Products')
        #Horizontal alignment
        plt.xticks(rotation=45, ha='right')  #Rotate x axis for better visibility

        #Display the graph
        plt.tight_layout()  #Adjust layout 
        plt.show()

    def select_item(self): #Method to select an item
        selected_index = self.available_listbox.curselection()  
        if not selected_index: 
            messagebox.showwarning("Warning", "Please select an item.")  
            return  #Return from the method
        selected_item = self.items_list[selected_index[0]]  
        if selected_item['stock'] > 0: 
            selected_item['stock'] -= 1
            if selected_item['code'] in self.selected_items:
                self.selected_items[selected_item['code']]['quantity']+=1
            else:
                self.selected_items[selected_item['code']]={
                    'name':selected_item['name'],
                    'price':selected_item['price'],
                    'quantity': 1
                }                                  
            self.update_available_items()   
            self.update_selected_items()  #Update the selected items in the listbox
        else:  #If the selected item is out of stock
            messagebox.showwarning("Warning", "Selected item is out of stock.")  

    def update_selected_items(self): #Method to update selected items in the listbox
        self.selected_listbox.delete(0, tk.END)  
        for item_code, item_data in self.selected_items.items(): 
            self.selected_listbox.insert(
                tk.END, f"{item_data['name']} - ${item_data['price']} - Quantity: {item_data['quantity']}"
        )

    def pay_by_cash(self): #Method to handle cash payment
        total_price = sum(item['price'] * item['quantity'] for item in self.selected_items.values()) #Calculate the total price of selected items
        amount_paid = simpledialog.askfloat("Cash Payment", f"Total Price: ${total_price:.2f}\nEnter amount paid:")  
        if amount_paid is not None:  
            if amount_paid >= total_price:  
                change = amount_paid - total_price  #Calculate the change
                messagebox.showinfo("Payment", f"Payment successful. Change: ${change:.2f}")  
                self.write_to_csv() 
                self.update_stock_levels() 
                self.thank_you()  
            else:  #If amount paid is insufficient
                messagebox.showerror("Error", "Insufficient payment.") 

    def pay_by_card(self): #Method to handle card payment
        total_price = sum(item['price'] * item['quantity'] for item in self.selected_items.values())
        messagebox.showinfo("Payment", "Payment successful.")  
        self.write_to_csv()  
        self.update_stock_levels()  
        self.thank_you()  #Display thank you message

    def cancel_purchase(self): #Method to cancel purchase
        messagebox.showinfo("Apology", "We apologize for any inconvenience caused.")  #Show apology message
        self.selected_items.clear()  
        self.update_selected_items()  

    def thank_you(self): #Method to display thank you message and clear selected items
        messagebox.showinfo("Thank You", "Thank you for shopping with us!")  
        self.selected_items.clear() 
        self.update_selected_items()  

    def write_to_csv(self):
        total_price = sum(
            item['price'] * item['quantity'] for item in self.selected_items.values()
        )
        with open('transactions.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Date", "Time", "Item", "Price", "Quantity", "Total Price"])
        timestamp = datetime.now()
        date = timestamp.strftime("%d/%m/%Y")
        time = timestamp.strftime("%H:%M:%S")
        for item_code, item_data in self.selected_items.items():
            # Write the quantity of each selected item
            writer.writerow([
                date, time, item_data['name'], item_data['price'],
                item_data['quantity'], item_data['price'] * item_data['quantity']
            ])
        total_price_row = ["", "", "Total Price", f"${total_price:.2f}"]
        writer.writerow(total_price_row)
    print("Transaction saved to: transactions.csv")


def main(): #Main function to create and run the GUI entry point for running gui
    root = tk.Tk()  #
    root.title("Vending Machine")  
    root.configure(bg='pink')  
    vending_machine_gui = VendingMachineGUI(root)  #Create instance of VendingMachineGUI class with root window as an argument
    root.mainloop()  #Run the main event loop

if __name__ == "__main__": 
    main()  #Call the main function 
