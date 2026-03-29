"""
mini-inventory v1 test senaryolari
Ogrenci: Tunahan Caner YILDIZ (251478112)
Proje: mini-inventory
"""

import subprocess
import os
import shutil


def run_cmd(args):
    """Komutu calistirir ve stdout sonucunu dondurur."""
    result = subprocess.run(
        ["python", "solution_v1.py"] + args,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def setup_function():
    """Her testten once temiz bir baslangic ortami hazirlar."""
    if os.path.exists(".miniinventory"):
        shutil.rmtree(".miniinventory")


# --- init testleri ---

def test_init_creates_directory():
    output = run_cmd(["init"])
    assert os.path.exists(".miniinventory")
    assert os.path.exists(".miniinventory/inventory.dat")
    assert "Initialized empty mini-inventory" in output


def test_init_already_exists():
    run_cmd(["init"])
    output = run_cmd(["init"])
    assert "Already initialized" in output


# --- add testleri ---

def test_add_single_product():
    run_cmd(["init"])
    output = run_cmd(["add", "Pencil", "50"])
    assert "Added product #1: Pencil (50)" in output


def test_add_second_product():
    run_cmd(["init"])
    run_cmd(["add", "Pencil", "50"])
    output = run_cmd(["add", "Notebook", "20"])
    assert "Added product #2: Notebook (20)" in output


def test_add_before_init():
    output = run_cmd(["add", "Pencil", "50"])
    assert "Not initialized. Run: python solution_v1.py init" in output


def test_add_invalid_quantity():
    run_cmd(["init"])
    output = run_cmd(["add", "Pencil", "-5"])
    assert "Invalid quantity" in output


def test_add_invalid_name():
    run_cmd(["init"])
    output = run_cmd(["add", "   ", "10"])
    assert "Invalid product name" in output


def test_add_duplicate_product():
    run_cmd(["init"])
    run_cmd(["add", "Pencil", "50"])
    output = run_cmd(["add", "Pencil", "30"])
    assert "Product already exists" in output


def test_add_missing_arguments():
    run_cmd(["init"])
    output = run_cmd(["add", "Pencil"])
    assert "Usage: python solution_v1.py add <name> <quantity>" in output


# --- list testleri ---

def test_list_before_init():
    output = run_cmd(["list"])
    assert "Not initialized. Run: python solution_v1.py init" in output


def test_list_empty_inventory():
    run_cmd(["init"])
    output = run_cmd(["list"])
    assert "No products found." in output


def test_list_products():
    run_cmd(["init"])
    run_cmd(["add", "Pencil", "50"])
    run_cmd(["add", "Notebook", "20"])
    output = run_cmd(["list"])
    assert "[1] Pencil - Quantity: 50 (2026-03-15)" in output
    assert "[2] Notebook - Quantity: 20 (2026-03-15)" in output


# --- update testleri ---

def test_update_product():
    run_cmd(["init"])
    run_cmd(["add", "Pencil", "50"])
    output = run_cmd(["update", "1", "80"])
    assert "Product #1 updated to quantity 80." in output


def test_update_before_init():
    output = run_cmd(["update", "1", "80"])
    assert "Not initialized. Run: python solution_v1.py init" in output


def test_update_invalid_quantity():
    run_cmd(["init"])
    run_cmd(["add", "Pencil", "50"])
    output = run_cmd(["update", "1", "-1"])
    assert "Invalid quantity" in output


def test_update_missing_product():
    run_cmd(["init"])
    output = run_cmd(["update", "1", "80"])
    assert "Product #1 not found." in output


def test_update_missing_arguments():
    run_cmd(["init"])
    output = run_cmd(["update", "1"])
    assert "Usage: python solution_v1.py update <id> <quantity>" in output


# --- delete testleri ---

def test_delete_product():
    run_cmd(["init"])
    run_cmd(["add", "Pencil", "50"])
    output = run_cmd(["delete", "1"])
    assert "Deleted product #1." in output


def test_delete_before_init():
    output = run_cmd(["delete", "1"])
    assert "Not initialized. Run: python solution_v1.py init" in output


def test_delete_missing_product():
    run_cmd(["init"])
    output = run_cmd(["delete", "1"])
    assert "Product #1 not found." in output


def test_delete_missing_arguments():
    run_cmd(["init"])
    output = run_cmd(["delete"])
    assert "Usage: python solution_v1.py delete <id>" in output


def test_deleted_ids_are_not_reused():
    run_cmd(["init"])
    run_cmd(["add", "Pencil", "50"])
    run_cmd(["add", "Notebook", "20"])
    run_cmd(["delete", "1"])
    output = run_cmd(["add", "Eraser", "10"])
    assert "Added product #3: Eraser (10)" in output


# --- genel hata testleri ---

def test_unknown_command():
    run_cmd(["init"])
    output = run_cmd(["fly"])
    assert "Unknown command: fly" in output


def test_missing_command():
    output = run_cmd([])
    assert "Usage: python solution_v1.py <command> [args]" in output
