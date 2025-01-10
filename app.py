import requests

BASE_URL = "http://localhost:8080"

def menu():
    """Display the main menu."""
    print("\nMedical Inventory REST API Client")
    print("1. Manage Medicines")
    print("2. Manage Suppliers")
    print("3. Manage Stock")
    print("4. Manage Sales")
    print("5. Exit")

def manage_medicines():
    """Manage Medicines via REST API."""
    while True:
        print("\nManage Medicines")
        print("1. Add Medicine")
        print("2. View Medicines")
        print("3. View Medicine by ID")
        print("4. Update Medicine")
        print("5. Delete Medicine")
        print("6. Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_medicine()
        elif choice == "2":
            view_medicines()
        elif choice == "3":
            view_medicine_by_id()
        elif choice == "4":
            update_medicine()
        elif choice == "5":
            delete_medicine()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")

def add_medicine():
    """Add a new medicine using the API."""
    medicine_id = input("Enter Medicine ID: ")
    name = input("Enter Medicine Name: ")
    category = input("Enter Category: ")
    unit_price = input("Enter Unit Price: ")

    data = {
        "MedicineID": medicine_id,
        "MedicineName": name,
        "Category": category,
        "UnitPrice": unit_price
    }

    response = requests.post(f"{BASE_URL}/medicines", json=data)
    if response.status_code == 200:
        print("Medicine added successfully.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def view_medicines():
    """View all medicines using the API."""
    response = requests.get(f"{BASE_URL}/medicines")
    if response.status_code == 200:
        medicines = response.json()
        for medicine in medicines:
            print(medicine)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def view_medicine_by_id():
    """View a specific medicine by ID using the API."""
    medicine_id = input("Enter Medicine ID: ")
    response = requests.get(f"{BASE_URL}/medicines/{medicine_id}")
    if response.status_code == 200:
        medicine = response.json()
        print(medicine)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def update_medicine():
    """Update a medicine using the API."""
    medicine_id = input("Enter Medicine ID to update: ")
    name = input("Enter new Medicine Name: ")
    category = input("Enter new Category: ")
    unit_price = input("Enter new Unit Price: ")

    data = {
        "MedicineName": name,
        "Category": category,
        "UnitPrice": unit_price
    }

    response = requests.put(f"{BASE_URL}/medicines/{medicine_id}", json=data)
    if response.status_code == 200:
        print("Medicine updated successfully.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def delete_medicine():
    """Delete a medicine using the API."""
    medicine_id = input("Enter Medicine ID to delete: ")
    response = requests.delete(f"{BASE_URL}/medicines/{medicine_id}")
    if response.status_code == 200:
        print("Medicine deleted successfully.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main():
    """Main application loop."""
    while True:
        menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            manage_medicines()
        elif choice == "2":
            print("Supplier management is under development.")
        elif choice == "3":
            print("Stock management is under development.")
        elif choice == "4":
            print("Sales management is under development.")
        elif choice == "5":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
