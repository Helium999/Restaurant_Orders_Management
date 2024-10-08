import csv
import datetime

filename = "all_orders.csv"
fields = ["name", "order", "date_time", "cost", "payment_method"]

def main():
    i = 1
    while i == 1:
        action = input("Do you want to log new order or query an existing order(l/q)?\n"
                       "To exit the program, enter \"e\": ")

        if action == "l" or action == "log":
            name = input("Enter customer's name: ").strip()
            order_items = input("Enter the items ordered by the customer(separated by , ): ").split(",")
            order_items = [item.strip() for item in order_items]
            cost = input("Enter total cost of the order(in rupees): ").strip()
            payment_method = input("Enter payment method(Cash/Card/UPI): ")

            while True:
                log_confirm = input("Do you want to log the following order(y/n):\n"
                                    f"Name = {name}, Order = {order_items}, Cost = {cost}, Payment Method = {payment_method}\n")
                if log_confirm == "y" or log_confirm == "yes":
                    now = datetime.datetime.now()
                    current_date_time = now.strftime("%d-%m-%Y %H:%M %p")
                    log_order(name, order_items, current_date_time, cost, payment_method)
                    print(f"Order of {name} logged successfully!")
                    i == 0
                    break

                elif log_confirm == "n" or log_confirm == "no":
                    break

                else:
                    print("Invalid input! Enter \"y\" to confirm or \"n\" to cancel.")

        elif action == "q" or action == "query":
            query = input("Enter name of customer to get order details: ")

            query_order(query)

        elif action == "e" or action == "exit":
            break

        else:
            print("Wrong Input! Enter \"l\" to log a new order or \"q\" to query an existing order,\nor \"e\" to exit the program.")



def log_order(name, order_items, current_date_time, cost, payment_method):
    order_dict = {"name":name,
                  "order":order_items,
                  "date_time":current_date_time,
                  "cost":cost,
                  "payment_method":payment_method
                  }
    with open(filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow(order_dict)

def query_order(query):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        query_number = 0
        for row in reader:
            if row["name"] == query:
                print(f"Name: {row['name']}\n"
                f"Order: {row['order']}\n"
                f"Date and time: {row['date_time']}\n"
                f"Cost: {row['cost']} rupees\n"
                f"Payment_method: {row['payment_method']}\n")
                query_number += 1
        print(f"{query_number} entries found.\n")

if __name__ == "__main__":
    main()