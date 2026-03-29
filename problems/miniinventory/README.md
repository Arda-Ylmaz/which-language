# 📦 mini-inventory

A simple command-line inventory management system built in Python.

---

## 🚀 Features

### Version V0
- Initialize inventory system
- Add products with name and quantity
- Store data in a plain text file

### Version V1
- List all products
- Update product quantity
- Delete products
- Improved input validation (duplicate names, invalid names)
- Clear ID generation rules

---

## 🛠️ Usage

python solution_v1.py init
python solution_v1.py add "Pencil" 50
python solution_v1.py list
python solution_v1.py update 1 80
python solution_v1.py delete 1

---

## 📋 V1 Task List

1. Implement list command
2. Implement update command
3. Implement delete command

---

## 🔄 V0 → V1 Summary

In version V1, the system was extended to support full inventory management.

The list, update, and delete commands were implemented, allowing users to view, modify, and remove products. Additionally, validation rules were added to prevent duplicate and invalid product names, and ID generation behavior was clarified to ensure data consistency.

---

## 📁 Data Storage

All data is stored in:

.miniinventory/inventory.dat

Format:
id|name|quantity|created_date
