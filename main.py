import csv
import datetime

records_file = "all_orders.csv"
menu_file = "menu.csv"
fields = ["name", "order", "date_time", "cost", "payment_method"]

def main():
    while True:
        action = input("To log a new order, enter \"l\".\n"
                       "To query an existing order, enter \"q\".\n"
                       "To view the menu, press \"m\".\n"
                       "To exit the program, enter \"e\": ").lower().strip()

        if action == "l" or action == "log":
            while True :
                if name := input("Enter customer's name: ").strip():
                    break
                else:
                    print("This field cannot be left empty.")

            while True:
                order_items = input("Enter the items ordered by the customer(separated by , ): ").split(",")
                order_items = [item.strip() for item in order_items if item.strip()]
                lower_order_items = [item.lower() for item in order_items]
                lower_menu_list = [item.lower() for item in view_menu("return_var")]
                intersection_set = set(lower_order_items).intersection(set(lower_menu_list))
                if len(intersection_set) == len(set(lower_order_items)):
                    if len(order_items) != 0:
                        break
                    else:
                        print("This field cannot be left empty.")
                else:
                    not_available = []
                    for i in lower_order_items:
                        if i not in lower_menu_list:
                            not_available.append(i)
                    print(f"The following item(s) are not available in menu:\n"
                          f"{not_available}")

            while True:
                try:
                    cost = float(input("Enter total cost of the order(in rupees): ").strip())
                    break
                except ValueError:
                    print("Enter only numbers.")

            while True:
                payment_method = input("Enter payment method(Cash/Card/UPI): ").strip()
                if payment_method.lower() not in ["cash", "card", "upi"]:
                    print("Invalid payment method.")
                else:
                    break

            while True:
                log_confirm = input("Do you want to log the following order(y/n):\n"
                                    f"Name = {name}, Order = {order_items}, Cost = {cost}, Payment Method = {payment_method}\n").lower().strip()
                if log_confirm == "y" or log_confirm == "yes":
                    log_order(name, order_items, cost, payment_method)
                    print(f"Order of '{name}' logged successfully!\n")
                    break

                elif log_confirm == "n" or log_confirm == "no":
                    print("Cancelled successfully.\n")
                    break

                else:
                    print("Invalid input! Enter \"y\" to confirm or \"n\" to cancel.")

        elif action == "q" or action == "query":
            while True:
                if query := input("Enter name of customer to get order details: ").lower().strip():
                    query_order(query)
                    break

        elif action == "m" or action == "menu":
            view_menu()

        elif action == "e" or action == "exit":
            break

        else:
            print("\nWrong Input! Enter \"l\" to log a new order or \"q\" to query an existing order,\nor \"e\" to exit the program.")



def log_order(name, order_items, cost, payment_method):
    now = datetime.datetime.now()
    current_date_time = now.strftime("%d-%b-%Y %I:%M %p")
    order_dict = {"name":name,
                  "order":order_items,
                  "date_time":current_date_time,
                  "cost":cost,
                  "payment_method":payment_method
                  }
    with open(records_file, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow(order_dict)

def query_order(query):
    with open(records_file) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        query_number = 0
        for row in reader:
            if row["name"].lower() == query:
                print(f"Name: {row['name']}\n"
                f"Order: {row['order']}\n"
                f"Date and time: {row['date_time']}\n"
                f"Cost: {row['cost']} rupees\n"
                f"Payment_method: {row['payment_method']}\n")
                query_number += 1
        print(f"{query_number} entries found.\n")

def view_menu(print_menu=None):
    with open(menu_file) as f:
        reader = csv.DictReader(f, fieldnames=["item", "price"])

        if print_menu is None:
            print("\n")
            for row in reader:
                print(f"{row["item"]} : {row["price"]}")
            print("\n")

        elif print_menu == "return_var":
            menu_items = [row["item"] for row in reader if row["item"] != "item"]
            return menu_items

if __name__ == "__main__":
    main()