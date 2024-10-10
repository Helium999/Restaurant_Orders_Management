import csv
import datetime

records_file = "all_orders.csv"
menu_file = "menu.csv"
fields_records = ["name", "order", "date_time", "cost", "payment_method"]
fields_menu = ["item", "price"]

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
                menu_items = list(set([i["item"] for i in view_menu() if i["item"] != "item"]))
                order_items = input("Enter the items ordered by the customer(separated by , ): ").split(",")
                order_items = list(set([item.strip() for item in order_items if item.strip()]))
                lower_order_items = [item.lower() for item in order_items]
                lower_menu_list = [item.lower() for item in menu_items]
                intersection_set = set(lower_order_items).intersection(set(lower_menu_list))

                if len(intersection_set) == len(lower_order_items):
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
                payment_method = input("Enter payment method(Cash/Card/UPI): ").strip()

                if payment_method.lower() not in ["cash", "card", "upi"]:
                    print("Invalid payment method.")
                else:
                    break

            while True:
                log_confirm = input("Do you want to log the following order(y/n):\n"
                                    f"Name = {name}, Order = {order_items}, Cost = {calc_cost(order_items)}, Payment Method = {payment_method}\n").lower().strip()

                if log_confirm == "y" or log_confirm == "yes":
                    log_order(name, order_items, calc_cost(order_items), payment_method)
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
                    query_number = 0

                    for i in view_records():
                        if i["name"].lower() == query:
                            print(f"Name: {i['name']}\n"
                                  f"Order: {i['order']}\n"
                                  f"Date and time: {i['date_time']}\n"
                                  f"Cost: {i['cost']} rupees\n"
                                  f"Payment_method: {i['payment_method']}\n")
                            query_number += 1

                    print(f"{query_number} entries found.\n")
                    break

        elif action == "m" or action == "menu":
            print("\n")
            for i in view_menu():
                print(f"{i["item"]} : {i["price"]}")
            print("\n")

        elif action == "e" or action == "exit":
            break

        else:
            print("\nWrong Input! Enter \"l\" to log a new order or \"q\" to query an existing order,\n"
                  "or \"e\" to exit the program.")

def log_order(name, order_items, order_cost, payment_method):
    now = datetime.datetime.now()
    current_date_time = now.strftime("%d-%b-%Y %I:%M %p")
    order_dict = {"name":name,
                  "order":order_items,
                  "date_time":current_date_time,
                  "cost":order_cost,
                  "payment_method":payment_method
                  }

    with open(records_file, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields_records)
        writer.writerow(order_dict)

def view_records():
    with open(records_file) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fields_records)
        records = [row for row in reader]

    return records

def view_menu():
    with open(menu_file) as f:
        reader = csv.DictReader(f, fieldnames=fields_menu)
        menu = [row for row in reader]

    return menu

def calc_cost(order_items):
    total_cost = 0
    for i in order_items:
        for j in view_menu():
            if j["item"].lower() == i.lower():
                total_cost += float(j["price"])

    return total_cost

if __name__ == "__main__":
    main()
