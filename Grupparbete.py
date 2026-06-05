import json
import os

class Medicine:
    def __init__(self, name, manufacturer, price, quantity, expiry_date):
        self.name = name
        self.manufacturer = manufacturer
        self.price = price
        self.quantity = quantity
        self.expiry_date = expiry_date
    
    def to_dict(self):
        return {"name": self.name, "manufacturer": self.manufacturer, "price": self.price, "quantity": self.quantity, "expiry_date": self.expiry_date}
    
    @staticmethod
    def from_dict(data):
        return Medicine(data["name"], data["manufacturer"], data["price"], data["quantity"], data["expiry_date"])

class Pharmacy:
    def __init__(self, filename="medicines.json"):
        self.filename = filename
        self.medicines = {}
        self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    for key, value in data.items():
                        self.medicines[key] = Medicine.from_dict(value)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading data: {e}")
            self.medicines = {}
    
    def save_data(self):
        try:
            with open(self.filename, "w") as file:
                data = {key: med.to_dict() for key, med in self.medicines.items()}
                json.dump(data, file, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")
    
    def add_medicine(self, medicine):
        if medicine.name in self.medicines:
            return False
        self.medicines[medicine.name] = medicine
        self.save_data()
        return True
    
    def remove_medicine(self, name):
        if name in self.medicines:
            del self.medicines[name]
            self.save_data()
            return True
        return False
    
    def update_quantity(self, name, new_quantity):
        if name in self.medicines and new_quantity >= 0:
            self.medicines[name].quantity = new_quantity
            self.save_data()
            return True
        return False
    
    def search_medicine(self, name):
        return self.medicines.get(name, None)
    
    def list_all(self):
        return list(self.medicines.values())

def display_menu():
    print("\n=== APOTEKSHANTERINGSSYSTEM ===")
    print("1. Lägg till medicin")
    print("2. Ta bort medicin")
    print("3. Uppdatera antal")
    print("4. Sök medicin")
    print("5. Visa alla mediciner")
    print("6. Avsluta")
    return input("Välj alternativ (1-6): ")

def add_medicine_interactive(pharmacy):
    try:
        name = input("Medicin namn: ").strip()
        manufacturer = input("Tillverkare: ").strip()
        price = float(input("Pris (SEK): "))
        quantity = int(input("Antal: "))
        expiry_date = input("Utgångsdatum (YYYY-MM-DD): ").strip()
        if not name or not manufacturer:
            raise ValueError("Namn och tillverkare får inte vara tomma")
        medicine = Medicine(name, manufacturer, price, quantity, expiry_date)
        if pharmacy.add_medicine(medicine):
            print(f"{name} har lagts till!")
        else:
            print(f"{name} finns redan i systemet!")
    except ValueError as e:
        print(f"Felaktig inmatning: {e}")
    except Exception as e:
        print(f"Ett oväntat fel inträffade: {e}")

def remove_medicine_interactive(pharmacy):
    name = input("Ange namn på medicin att ta bort: ").strip()
    if pharmacy.remove_medicine(name):
        print(f"{name} har tagits bort!")
    else:
        print(f"{name} hittades inte i systemet!")

def update_quantity_interactive(pharmacy):
    try:
        name = input("Ange namn på medicin: ").strip()
        new_quantity = int(input("Nytt antal: "))
        if pharmacy.update_quantity(name, new_quantity):
            print(f"Antalet för {name} har uppdaterats till {new_quantity}")
        else:
            print(f"{name} hittades inte eller ogiltigt antal!")
    except ValueError:
        print("Ogiltigt antal! Ange ett heltal.")

def search_medicine_interactive(pharmacy):
    name = input("Ange namn på medicin att söka efter: ").strip()
    medicine = pharmacy.search_medicine(name)
    if medicine:
        print(f"\nHittade medicin:")
        print(f"Namn: {medicine.name}")
        print(f"Tillverkare: {medicine.manufacturer}")
        print(f"Pris: {medicine.price} SEK")
        print(f"Antal: {medicine.quantity}")
        print(f"Utgångsdatum: {medicine.expiry_date}")
    else:
        print(f"{name} hittades inte!")

def list_all_medicines(pharmacy):
    medicines = pharmacy.list_all()
    if not medicines:
        print("Inga mediciner i systemet!")
        return
    print("\n=== ALLA MEDICINER ===")
    for i, med in enumerate(medicines, 1):
        print(f"{i}. {med.name} - {med.manufacturer} - {med.price} SEK - {med.quantity} st - Utgår: {med.expiry_date}")

def main():
    pharmacy = Pharmacy()
    while True:
        choice = display_menu()
        if choice == "1":
            add_medicine_interactive(pharmacy)
        elif choice == "2":
            remove_medicine_interactive(pharmacy)
        elif choice == "3":
            update_quantity_interactive(pharmacy)
        elif choice == "4":
            search_medicine_interactive(pharmacy)
        elif choice == "5":
            list_all_medicines(pharmacy)
        elif choice == "6":
            print("Tack för att du använder Apotekssystemet!")
            break
        else:
            print("Ogiltigt val! Välj 1-6.")

if __name__ == "__main__":
    main()