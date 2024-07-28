# Amazon Invoice Gettor

Downloads invoices from Amazon when given the order ID.

```
Usage: invoice_gettor [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  get
  login
  logout
```

# Features

-   Search across multiple Amazon accounts for a single order.
-   Integration with ChatGPT (using 4o-mini) to summarize item listings.
-   Integration with Actual Budget to automatically add transaction.

# Example usage

```
invoice_gettor get 111-9886129-5664243 --gpt --actual
```

Output:

```
Order ID: 111-9886129-5624243
--------------------------------
Items in invoice:
1. Double Sided Tape,3M Heavy duty double sided tape,15.4FT Length, 1/2 Inch Width for Car, LED Strip Lights, Home Decor, Office Decor, Made with of 3M VHB Tape (1/2in*15.4FT)
2. Mr. Clean 2X Concentrated Multi Surface Cleaner with Lemon Scent, All Purpose Cleaner, 41 fl oz
Sold by: Amazon.com S
--------------------------------
Order total: $14.93  Grand total: $14.93
--------------------------------
Summarized items:
1. Double sided tape
2. Multi Surface Cleaner
--------------------------------
New Actual transaction:
Double sided tape, Multi Surface Cleaner | 111-9886129-5664243
Add this transaction? (yes/no):
```

# Building

Setup playwright: https://playwright.dev/python/docs/library

Run: `pip install --editable .`
