"""Inventory Management System — a Python-based program to manage, update
, and store stock data securely."""
import json
import logging
from datetime import datetime

logging.basicConfig(
    filename="inventory.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

stock_data = {}


def add_item(item: str, qty: int, logs=None) -> None:
    """Add an item and quantity to the stock data."""
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):
        logging.warning(
            "Invalid input types for add_item: item=%s, qty=%s", item, qty
        )
        return

    if not item:
        logging.warning("Empty item name provided.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s", qty, item)


def remove_item(item: str, qty: int) -> None:
    """Remove quantity of an item from stock data."""
    if not isinstance(item, str) or not isinstance(qty, int):
        logging.warning(
            "Invalid input types for remove_item: item=%s, qty=%s", item, qty
        )
        return

    try:
        if item not in stock_data:
            raise KeyError(item)

        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
        logging.info("Removed %d of %s", qty, item)
    except KeyError:
        logging.error("Attempted to remove non-existent item: %s", item)
    except (OSError, ValueError) as error:
        logging.error("Unexpected error while removing item: %s", error)


def get_qty(item: str) -> int:
    """Return the quantity of an item if it exists."""
    return stock_data.get(item, 0)


def load_data(file_path: str = "inventory.json") -> dict:
    """Load stock data from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        logging.info("Data loaded from %s", file_path)
        return data
    except FileNotFoundError:
        logging.warning(
            "File %s not found. Starting with empty inventory.", file_path
        )
        return {}
    except json.JSONDecodeError:
        logging.error("Invalid JSON format in %s", file_path)
        return {}


def save_data(data: dict, file_path: str = "inventory.json") -> None:
    """Save stock data to a JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        logging.info("Data saved to %s", file_path)
    except (OSError, TypeError) as error:
        logging.error("Failed to save data: %s", error)


def print_data() -> None:
    """Print all inventory items."""
    print("Items Report:")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold: int = 5) -> list:
    """Return items below a given threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main() -> None:
    """Main function to test inventory system."""
    data = load_data()

    add_item("apple", 10)
    add_item("banana", 2)
    remove_item("apple", 3)
    remove_item("orange", 1)
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data(data)
    print_data()


if __name__ == "__main__":
    main()