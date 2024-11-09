# MyMoneyMate

**MyMoneyMate** is a versatile expense-tracking application designed to help users manage both personal and group expenses. The app integrates seamlessly with Telegram, providing an easy-to-use interface for tracking expenses, setting savings goals, and analyzing spending patterns. 

## Features

- **Personal and Group Expense Tracking:** Log expenses individually or within groups.
- **Category Management:** Organize expenses by categories for easier tracking.
- **Expense Analysis and Statistics:** Review your spending patterns and generate reports.
- **Multi-Currency Support:** Track expenses in different currencies.

## Running the Application

You have two options to run **MyMoneyMate**:

### Option 1: Using the `main.exe` Executable

1. **Locate `main.exe`:**
   - Navigate to the `Backend/dist` directory in your project folder.

   ```plaintext
   Backend/dist
   ```

2. **Run `main.exe`:**
   - Double-click `main.exe` or run it from the terminal using:

     ```bash
     ./main.exe
     ```

   - This option includes all dependencies, so no additional installation is required.

### Option 2: Installing Dependencies and Running the App Manually

If you prefer to manually set up the environment:

1. **Set Up Python and Virtual Environment:**
   - Install Python (version 3.12 or compatible).
   - Create and activate a virtual environment:

     ```bash
     python -m venv myenv
     myenv\Scripts\activate  # Windows
     source myenv/bin/activate  # macOS/Linux
     ```

2. **Install Required Packages:**
   - Move to the `Backend` directory and install dependencies:

     ```bash
     cd Backend
     pip install -r requirements.txt
     ```

3. **Run the Application:**
   - With all dependencies in place, launch the app:

     ```bash
     python main.py
     ```

## Main Commands and Usage

Below are the primary commands available in **MyMoneyMate**:

### 1. `/new <category> <amount>`
   - **Description:** Adds a new expense.
   - **Example:** `/new Food 50`
   - **Usage:** Provides an interface to log a new expense under a specified category.

### 2. `/delete <expense_id>`
   - **Description:** Deletes an expense based on the unique expense ID.
   - **Example:** `/delete 1`
   - **Usage:** Deletes the expense entry with the specified ID.

### 3. `/add_category <category_name>`
   - **Description:** Adds a new category to organize expenses.
   - **Example:** `/add_category Travel`
   - **Usage:** Useful for setting up custom categories beyond the default list.

### 4. `/list`
   - **Description:** Lists all expenses for the user or group.
   - **Usage:** Displays expenses in a structured format, showing date, category, and amount.

### 5. `/stats`
   - **Description:** Provides a summary of expenses over different timeframes.
   - **Example Usage:** Select between "This Month," "Last Month," or "All Time" to view relevant statistics.

### 6. `/brakeeven`
   - **Description:** Shows balances between group members based on expenses.
   - **Usage:** Helps group members understand their owed or due amounts within shared expenses.

## Additional Information

- **Multi-Currency Support:** Use `/stats` to select the currency you want to view your statistics in. The app provides a selection of common currencies.
- **Database Configuration:** Ensure any required database connections are configured in the `config.py` file or through environment variables.
- **Environment Variables:** Define any needed environment variables in a `.env` file if required by the app.
