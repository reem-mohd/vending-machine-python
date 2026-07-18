# Vending Machine - Client-Server Application

A Python-based vending machine system built for CST1510, simulating a real-world vending machine experience with a client-server architecture.

## Features
- Browse and select from a range of snacks and drinks
- Multiple payment methods (cash and card)
- Cancel purchase option
- Real-time stock updates after each transaction
- Transaction history logged to CSV files

## How It Works
- **server.py** - handles requests from the client, manages stock levels, and processes transactions
- **client.py** - provides the user-facing interface for browsing items, selecting products, and completing payment
- Stock data and transaction logs are stored in CSV files, updated automatically after each purchase

## Tech Stack
- Python
- Socket programming (client-server communication)
- CSV file handling

## How to Run
1. Start the server

2. In a separate terminal, start the client

3. Follow the on-screen prompts to select an item, choose a payment method, and complete or cancel your purchase.
