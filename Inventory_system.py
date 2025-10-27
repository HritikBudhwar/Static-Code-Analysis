import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='inventory.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

stock_data = {}


def add_item(item=None, qty=0, logs=None):
    """Add an item and quantity to the stock data."""
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):
        logging.warning("Invalid input types for add_item: item=%s, qty=%s", item, qty)
        return

    if not item:
        logging.warning("Empty item name provided.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s", qty, item)


def remove_item(item, qty):
    """Remove quantity of an item from stock data."""
    if not isinstance(item, str) or not isinstance(qty, int):
        logging.warning("Invalid input types for remove_item: item=%s, qty=%s", item, qty)
        return

    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
        logging.info("Removed %d of %s", qty, item)
    except KeyError:
        logging.error("Attempted to remove non-existent item: %s", item)
    except Exception as e:
        logging.error("Unexpected error while removing item: %s", e)


def get_qty(item):
    """Return the quantity of an item if it exists."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load stock data from a JSON file."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        logging.info("Data loaded from %s", file)
    except FileNotFoundError:
        logging.warning("File %s not found. Starting with empty inventory.", file)
        stock_data = {}
    except json.JSONDecodeError:
        logging.error("Invalid JSON format in %s", file)


def save_data(file="inventory.json"):
    """Save stock data to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        logging.info("Data saved to %s", file)
    except Exception as e:
        logging.error("Failed to save data: %s", e)


def print_data():
    """Print all inventory items."""
    print("Items Report:")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold=5):
    """Return items below a given threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Main function to test inventory system."""
    add_item("apple", 10)
    add_item("banana", 2)
    remove_item("apple", 3)
    remove_item("orange", 1)
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()
