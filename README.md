# MyMoneyMate

MyMoneyMate is a Telegram bot designed to simplify personal and group expense tracking. By integrating directly with Telegram, MyMoneyMate provides a convenient way to manage expenses without leaving your chat. Users can add expenses, view statistics, manage shared group expenses, and export data to Excel, all within the chat interface.

## Table of Contents
1. [Features](#features)
2. [Setup](#setup)
3. [Configuration](#configuration)
4. [Commands](#commands)
5. [Project Structure](#project-structure)
6. [Contributing](#contributing)
7. [License](#license)

---

## Features

- **Add New Expenses**: Track personal or group expenses by adding new expense entries directly in the chat.
- **Group Expense Management**: Manage shared expenses with group members, keeping everyone up-to-date on balances and owed amounts.
- **Expense Statistics**: View statistics based on different time periods and currencies, making it easy to analyze spending habits.
- **Add Custom Categories**: Personalize expense tracking with user-defined categories.
- **Export to Excel**: Download expense data to an Excel file, allowing further analysis outside the bot.
  
## Setup

### Prerequisites
1. **Python 3.8+**: Ensure you have Python installed.
2. **Dependencies**: Install dependencies via `pip`.
3. **PostgreSQL**: Set up PostgreSQL as the database.

### Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/username/MyMoneyMate.git
    cd MyMoneyMate
    ```
2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the PostgreSQL database:
   - Create the necessary tables using the provided SQL scripts in `/database/`.

4. Configure environment variables in `.env` (see below).

### Environment Variables
In the root directory, create a `.env` file and configure the following:
   ```
   TELEGRAM_TOKEN=your_telegram_bot_token
   DATABASE_URL=your_database_url
   ```

## Configuration

Configuration is handled in `config.py`. You can adjust settings for logging, database connections, and Telegram API integration as needed. This file includes configurable parameters like categories and database connection settings.

## Commands

Here are the main commands available in MyMoneyMate:

- `/start` - Initialize the bot and get a welcome message.
- `/add [amount]` - Add a new expense, with further prompts for category selection.
- `/stats` - View statistics based on time period and currency. Options include "This Month," "Last Month," or "All Time."
- `/add_category [category_name]` - Add a new expense category for custom tracking.
- `/list` - List all expenses for the user or group.
- `/export` - Export all expenses to an Excel file with columns for user, date, category, amount, and expense ID.

## Project Structure

```
MyMoneyMate/
├── backend.py              # Handles database interactions
├── Commands.py             # Defines bot commands and interactions
├── main.py                 # Bot initialization and main loop
├── config.py               # Configuration and settings
├── requirements.txt        # Project dependencies
├── database/
│   ├── setup.sql           # SQL scripts for database setup
└── README.md               # Project README
```

## Contributing

We welcome contributions! If you'd like to improve MyMoneyMate, please fork the repository and create a pull request with your changes. Ensure your code follows standard practices and includes relevant documentation or comments.

### Steps to Contribute
1. Fork the project.
2. Create a branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

MyMoneyMate is licensed under the MIT License. See `LICENSE` for more information.

---

Thank you for using MyMoneyMate! If you encounter any issues, please reach out via GitHub issues.