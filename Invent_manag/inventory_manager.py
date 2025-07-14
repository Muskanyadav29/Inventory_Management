import csv
import os

INVENTORY_FILE = "inventory.csv"
FIELDNAMES = ['product_id', 'name', 'category', 'price', 'quantity']
LOW_STOCK_THRESHOLD = 5

def login():
    print(" Login")
    username = input("Enter username (admin/staff): ").strip().lower()
    if username not in ['admin', 'staff']:
        print(" Invalid user. Defaulting to staff.")
        username = 'staff'
    return username

def read_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return []
    with open(INVENTORY_FILE, mode='r', newline='') as file:
        return list(csv.DictReader(file))

def write_inventory(products):
    with open(INVENTORY_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for product in products:
            writer.writerow(product)

def get_product_by_id(products, pid):
    return next((p for p in products if p['product_id'] == pid), None)

def get_product_by_name(products, name):
    return next((p for p in products if p['name'].lower() == name.lower()), None)


def add_product():
    products = read_inventory()
    product_id = input("Enter Product ID: ").strip()
    if get_product_by_id(products, product_id):
        print(" Product ID already exists.")
        return

    name = input("Enter Product Name: ").strip()
    category = input("Enter Category (e.g., electronics, groceries): ").strip()

    try:
        price = float(input("Enter Price: "))
        quantity = int(input("Enter Quantity: "))
    except ValueError:
        print(" Invalid price or quantity.")
        return

    new_product = {
        'product_id': product_id,
        'name': name,
        'category': category,
        'price': f"{price:.2f}",
        'quantity': str(quantity)
    }

    products.append(new_product)
    write_inventory(products)
    print(" Product added successfully!")

def update_quantity():
    products = read_inventory()
    product_id = input("Enter Product ID to update: ").strip()
    product = get_product_by_id(products, product_id)
    if not product:
        print(" Product not found.")
        return

    try:
        change = int(input("Enter quantity change (+/-): "))
    except ValueError:
        print(" Invalid number.")
        return

    new_quantity = int(product['quantity']) + change
    if new_quantity < 0:
        print(" Quantity cannot be negative.")
        return

    product['quantity'] = str(new_quantity)
    write_inventory(products)
    print(" Quantity updated successfully!")

def delete_product(user):
    if user != 'admin':
        print(" Only admin can delete products.")
        return

    products = read_inventory()
    product_id = input("Enter Product ID to delete: ").strip()
    updated = [p for p in products if p['product_id'] != product_id]

    if len(products) == len(updated):
        print(" Product not found.")
    else:
        write_inventory(updated)
        print(" Product deleted successfully!")

def view_inventory():
    products = read_inventory()
    if not products:
        print("📦 Inventory is empty.")
        return

    print("\n Inventory List:")
    print("{:<10} {:<20} {:<15} {:<10} {:<10}".format("ID", "Name", "Category", "Price", "Qty"))
    print("-" * 70)

    for p in products:
        stock = int(p['quantity'])
        warning = " LOW" if stock < LOW_STOCK_THRESHOLD else ""
        print("{:<10} {:<20} {:<15} ₹{:<9} {:<5}{}".format(
            p['product_id'], p['name'], p['category'], p['price'], p['quantity'], warning
        ))

def search_product():
    products = read_inventory()
    print("\n Search Options:")
    print("1. By Product ID")
    print("2. By Name")
    print("3. By Category")
    choice = input("Choose option (1-3): ").strip()

    if choice == '1':
        pid = input("Enter Product ID: ").strip()
        product = get_product_by_id(products, pid)
        display_product(product)
    elif choice == '2':
        name = input("Enter Product Name: ").strip()
        product = get_product_by_name(products, name)
        display_product(product)
    elif choice == '3':
        category = input("Enter category: ").strip().lower()
        filtered = [p for p in products if p['category'].lower() == category]
        if filtered:
            for p in filtered:
                display_product(p)
        else:
            print(" No products in this category.")
    else:
        print(" Invalid choice.")

def display_product(product):
    if product:
        print("\n Product Found:")
        print(f"ID: {product['product_id']}")
        print(f"Name: {product['name']}")
        print(f"Category: {product['category']}")
        print(f"Price: ₹{product['price']}")
        print(f"Quantity: {product['quantity']}")
    else:
        print(" Product not found.")

def sort_inventory():
    products = read_inventory()
    if not products:
        print("Inventory is empty.")
        return

    print("\n Sort By:")
    print("1. Name")
    print("2. Price")
    print("3. Quantity")
    choice = input("Choose sort option (1-3): ").strip()

    if choice == '1':
        sorted_items = sorted(products, key=lambda x: x['name'].lower())
    elif choice == '2':
        sorted_items = sorted(products, key=lambda x: float(x['price']))
    elif choice == '3':
        sorted_items = sorted(products, key=lambda x: int(x['quantity']))
    else:
        print(" Invalid choice.")
        return

    print("\n Sorted Inventory:")
    print("{:<10} {:<20} {:<15} {:<10} {:<10}".format("ID", "Name", "Category", "Price", "Qty"))
    print("-" * 70)
    for p in sorted_items:
        print("{:<10} {:<20} {:<15} ₹{:<9} {:<10}".format(
            p['product_id'], p['name'], p['category'], p['price'], p['quantity']
        ))


def main():
    user = login()
    while True:
        print(f"\n Inventory Management ({user.upper()}):")
        print("1. Add New Product")
        print("2. Update Product Quantity")
        if user == 'admin':
            print("3. Delete Product")
        print("4. View Inventory")
        print("5. Search Product")
        print("6. Sort Inventory")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_product()
        elif choice == '2':
            update_quantity()
        elif choice == '3' and user == 'admin':
            delete_product(user)
        elif choice == '4':
            view_inventory()
        elif choice == '5':
            search_product()
        elif choice == '6':
            sort_inventory()
        elif choice == '7':
            print(" Exiting... Goodbye!")
            break
        else:
            print(" Invalid choice or permission denied.")

if __name__ == "__main__":
    main()
