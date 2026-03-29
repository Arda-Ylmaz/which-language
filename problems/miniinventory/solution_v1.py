"""
mini-inventory v1
Ogrenci: Tunahan Caner YILDIZ (251478112)

Kapsam:
- init komutu calisir
- add komutu calisir
- list komutu calisir
- update komutu calisir
- delete komutu calisir
"""

import sys
import os
DATA_DIR = ".miniinventory"
DATA_FILE = os.path.join(DATA_DIR, "inventory.dat")
CREATED_DATE = "2026-03-15"


def initialize():
    """Sistem klasorunu ve bos veri dosyasini olusturur."""
    if os.path.exists(DATA_DIR):
        return "Already initialized"

    os.mkdir(DATA_DIR)

    file_object = open(DATA_FILE, "w", encoding="utf-8")
    file_object.close()

    return "Initialized empty mini-inventory in .miniinventory/"


def is_initialized():
    return os.path.exists(DATA_DIR) and os.path.exists(DATA_FILE)


def is_valid_quantity(quantity_text):
    """Miktar bilgisinin negatif olmayan bir tam sayi olup olmadigini kontrol eder."""
    return quantity_text.isdigit()


def is_valid_name(name):
    """Urun adinin bos veya sadece bosluk olmadigini kontrol eder."""
    return name.strip() != ""


def read_products():
    """Veri dosyasindaki urunleri sozluk listesi olarak okur."""
    products = []

    if not os.path.exists(DATA_FILE):
        return products

    file_object = open(DATA_FILE, "r", encoding="utf-8")
    lines = file_object.readlines()
    file_object.close()

    for line in lines:
        line = line.strip()
        if line == "":
            continue

        parts = line.split("|")
        if len(parts) != 4:
            continue

        products.append({
            "id": int(parts[0]),
            "name": parts[1],
            "quantity": int(parts[2]),
            "created_date": parts[3],
        })

    return products


def write_products(products):
    """Tum urunleri veri dosyasina yeniden yazar."""
    file_object = open(DATA_FILE, "w", encoding="utf-8")

    for product in products:
        line = (
            str(product["id"])
            + "|"
            + product["name"]
            + "|"
            + str(product["quantity"])
            + "|"
            + product["created_date"]
            + "\n"
        )
        file_object.write(line)

    file_object.close()


def get_next_product_id(products):
    """Bir sonraki kullanilacak urun kimligini dondurur."""
    if len(products) == 0:
        return 1

    max_id = products[0]["id"]
    for product in products:
        if product["id"] > max_id:
            max_id = product["id"]

    return max_id + 1


def add_product(name, quantity_text):
    """Yeni bir urunu veri dosyasina ekler."""
    if not is_initialized():
        return "Not initialized. Run: python solution_v1.py init"

    if not is_valid_name(name):
        return "Invalid product name"

    if not is_valid_quantity(quantity_text):
        return "Invalid quantity"

    products = read_products()

    for product in products:
        if product["name"] == name:
            return "Product already exists"

    product_id = get_next_product_id(products)

    file_object = open(DATA_FILE, "a", encoding="utf-8")
    file_object.write(
        str(product_id) + "|" + name + "|" + quantity_text + "|" + CREATED_DATE + "\n"
    )
    file_object.close()

    return "Added product #" + str(product_id) + ": " + name + " (" + quantity_text + ")"


def list_products():
    """Tum urunleri ekrana basilmaya hazir metin olarak dondurur."""
    if not is_initialized():
        return "Not initialized. Run: python solution_v1.py init"

    products = read_products()

    if len(products) == 0:
        return "No products found."

    output_lines = []
    for product in products:
        output_lines.append(
            "["
            + str(product["id"])
            + "] "
            + product["name"]
            + " - Quantity: "
            + str(product["quantity"])
            + " ("
            + product["created_date"]
            + ")"
        )

    return "\n".join(output_lines)


def update_product(product_id_text, quantity_text):
    """Verilen urunun miktarini gunceller."""
    if not is_initialized():
        return "Not initialized. Run: python solution_v1.py init"

    if not is_valid_quantity(quantity_text):
        return "Invalid quantity"

    if not product_id_text.isdigit():
        return "Product #" + product_id_text + " not found."

    target_id = int(product_id_text)
    products = read_products()

    for product in products:
        if product["id"] == target_id:
            product["quantity"] = int(quantity_text)
            write_products(products)
            return "Product #" + str(target_id) + " updated to quantity " + quantity_text + "."

    return "Product #" + str(target_id) + " not found."


def delete_product(product_id_text):
    """Verilen urunu veri dosyasindan siler."""
    if not is_initialized():
        return "Not initialized. Run: python solution_v1.py init"

    if not product_id_text.isdigit():
        return "Product #" + product_id_text + " not found."

    target_id = int(product_id_text)
    products = read_products()
    updated_products = []

    found = False
    for product in products:
        if product["id"] == target_id:
            found = True
        else:
            updated_products.append(product)

    if not found:
        return "Product #" + str(target_id) + " not found."

    write_products(updated_products)
    return "Deleted product #" + str(target_id) + "."


if len(sys.argv) < 2:
    print("Usage: python solution_v1.py <command> [args]")

elif sys.argv[1] == "init":
    print(initialize())

elif sys.argv[1] == "add":
    if len(sys.argv) < 4:
        print("Usage: python solution_v1.py add <name> <quantity>")
    else:
        print(add_product(sys.argv[2], sys.argv[3]))

elif sys.argv[1] == "list":
    print(list_products())

elif sys.argv[1] == "update":
    if len(sys.argv) < 4:
        print("Usage: python solution_v1.py update <id> <quantity>")
    else:
        print(update_product(sys.argv[2], sys.argv[3]))

elif sys.argv[1] == "delete":
    if len(sys.argv) < 3:
        print("Usage: python solution_v1.py delete <id>")
    else:
        print(delete_product(sys.argv[2]))

else:
    print("Unknown command: " + sys.argv[1])
