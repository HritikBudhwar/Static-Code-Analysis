# Inventory Management System Refactoring Report

This report documents the security, reliability, and code quality improvements made to the original `inventory.py` file during refactoring.

## Refactoring and Issue Resolution Table

The table below documents the major issues identified in the original code and the corresponding robust fixes implemented in the updated system.

| Issue in Original Code | Type | Description of Problem | Implementation of Fix |
| :--- | :--- | :--- | :--- |
| **Mutable Default Argument (`logs=[]`)** | Bug | The `logs` list was initialized in the function signature, causing it to be **shared across all function calls**. This resulted in state leakage and incorrect logging. | The parameter was set to **`logs=None`**, and the list is now initialized uniquely inside the function body (`if logs is None: logs = []`), preventing state sharing. |
| **Broad Exception Handling (`except: pass`)** | Reliability | The `removeItem` function used a general `except` block, which **silently swallowed all errors**, including critical issues like `KeyError` (item not found), making the code unreliable and impossible to debug. | The logic was updated to use **specific exception handling** (`try...except KeyError:`). Detailed **logging** was added to record specific errors instead of ignoring them. |
| **Lack of Input Validation** | Vulnerability/Bug | Functions accepted any data type for key parameters (`item`, `qty`), leading to unpredictable behavior and runtime crashes if invalid types were passed. | **Runtime type checks** were introduced using `isinstance()` for the `item` (must be `str`) and `qty` (must be `int`) parameters. A `logging.warning` is issued for invalid inputs. |
| **Insecure Use of `eval()`** | Security Risk | The `main` function contained a call to `eval()`, a well-known security vulnerability that allows execution of arbitrary, potentially malicious, code. | The **`eval()` call was completely removed** from the `main` function to eliminate this critical security exposure. |
| **Unsafe File I/O** | Reliability | File opening and closing were managed manually (`f.close()`), which is prone to **resource leaks** if an exception occurs. It also lacked handling for common I/O errors. | All file operations were refactored to use the **`with open(...)`** context manager, guaranteeing file closure. Specific exceptions like `FileNotFoundError` and `json.JSONDecodeError` were added for robust data handling. |
| **Ambiguous Item Check** | Bug | The original check `if not item:` was too generic and could allow non-string, falsy values (e.g., `0`) to bypass the item-name check. | A specific check was added to ensure the `item` string is not empty, which, combined with the new type check, prevents inventory entries with blank names. |