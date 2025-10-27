## Issues fixed

| Issue Type | Line(s) | Description | Fix Approach |
|---|---:|---|---|
| Mutable default arg | 9 | logs=[] shared across calls | Changed to logs=None and init inside function |
| Bare except | 24 | hides exceptions | Use KeyError and general except Exception as e |
| Insecure eval | 67 | dangerous eval() | Removed eval() |
| File handling | 38,45 | open() without context manager | Use with open(...) |
