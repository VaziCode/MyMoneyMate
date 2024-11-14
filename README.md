---

# MyMoneyMate

MyMoneyMate is a Telegram bot designed to simplify tracking personal and group expenses. It provides features to manage expenses, savings, and financial goals in an intuitive way.

---

## Features

- **Personal Expense Tracking**: Keep track of your individual expenses in various categories.
- **Group Expense Sharing**: Manage shared expenses within groups, calculate balances, and split costs.
- **Category Management**: Add and organize expense categories.
- **Expense Reports**: Export expense data to Excel for analysis.
- **Statistics**: Get a breakdown of your spending habits by time periods.
- **Savings Goals**: Track your progress toward savings goals.
- **Intuitive Commands**: Use Telegram commands to interact with the bot.

---

## Usage

### Bot Commands

1. **Adding an Expense**:
   - Command: `/new <category> <amount>`
   - Example: `/new Food 50`

2. **Deleting an Expense**:
   - Command: `/delete <expense_id>`
   - Example: `/delete 123`

3. **Listing Expenses**:
   - Command: `/list`
   - Shows all expenses recorded for the current group or user.

4. **Adding a Category**:
   - Command: `/add_category <category_name>`
   - Example: `/add_category Travel`

5. **Viewing Statistics**:
   - Command: `/stats`
   - Provides a breakdown of expenses for various time periods.

6. **Exporting to Excel**:
   - Command: `/export`
   - Generates an Excel file of your expenses.

7. **Breaking Even**:
   - Command: `/brake_even`
   - Calculates how much each participant owes or is owed in a group.

---

## Prerequisites

1. **Python**: Ensure Python 3.12 or later is installed.
2. **Dependencies**: Install required libraries using the following command:
   ```bash
   pip install -r requirements.txt
   ```
3. **Database**: Set up a database server with the necessary credentials.

---

## Running the Application

To run MyMoneyMate, you must provide database credentials as arguments. This ensures secure and flexible configuration. There are two ways to execute the app:

### 1. Using the Script

Run the `run_app.bat` script:

- **Command**:
  ```batch
  run_app.bat
  ```

- **Editing the Script**:
  Open the script and replace the placeholders with your database credentials. Example:

  ```batch
  python Backend/main.py --db_host <DB_HOST> --db_name <DB_DATABASE_NAME> --db_user <DB_USER> --db_password <DB_PASSWORD> --db_port <DB_PORT>
  ```

  Example with placeholders replaced:
  ```batch
  python Backend/main.py --db_host ptojectname-db.c78gm24osi89.us-east-1.rds.amazonaws.com --db_name initial_db --db_user my_SQL --db_password Tal123456 --db_port 5432
  ```

---

### 2. Using the Command Line

Run the following command:

```bash
python Backend/main.py --db_host <DB_HOST> --db_name <DB_DATABASE_NAME> --db_user <DB_USER> --db_password <DB_PASSWORD> --db_port <DB_PORT>
```

Replace the placeholders with actual values:

- `<DB_HOST>`: Database host (e.g., `your_db_host`).
- `<DB_DATABASE_NAME>`: Database name (e.g., `your_db_name`).
- `<DB_USER>`: Database username (e.g., `your_-db_user`).
- `<DB_PASSWORD>`: Database password (e.g., `your_password`).
- `<DB_PORT>`: Database port (e.g., `your_port`).

Example:
```bash
python Backend/main.py --db_host ptojectname-db.c78gm24osi89.us-east-1.rds.amazonaws.com --db_name initial_db --db_user my_SQL --db_password Tal123456 --db_port 5432
```

---

## Important Notes

1. **Database Credentials**: Ensure the credentials match your database configuration. Contact your database administrator for the correct details.
2. **Security**: Avoid hardcoding sensitive credentials into your codebase. Use the provided script or pass them securely as command-line arguments.

---

