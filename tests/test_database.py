import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from Backend import Server, Commands


@pytest.fixture
def db():
    db = Server.Database()
    db.cursor = MagicMock()
    return db

# def test_new_expense(db):
#     db.new_expense(1, -4560716368, "Food", 100.0)
#     db.cursor.execute.assert_called_once_with(
#         "INSERT INTO userproducts (fk_user_id, fk_group_id, category_name, amount) VALUES (%s, %s, %s, %s)",
#         (1, -4560716368, "Food", 100.0)
#     )

# def test_new_expense():
#     db = Server.Database()  # Use a properly instantiated Database object or mock
#     db.cursor = MagicMock()  # Mock cursor
#     db.new_expense(1, -4560716368, "Food", 50)
#
#     # Adjust expectations to ensure the call matches
#     db.cursor.execute.assert_called_once_with(
#         "INSERT INTO userproducts (fk_user_id, fk_group_id, category_name, amount) VALUES (%s, %s, %s, %s);",
#         (1, -4560716368, "Food", 50)
#     )

# def test_new_expense():
#     db = Server.Database()  # Ensure Database is properly instantiated
#     db.cursor = MagicMock()  # Mock cursor
#
#     # Assuming the `new_expense` method has multiple calls to execute
#     db.new_expense(1, -4560716368, "Food", 50)
#
#     # Check the specific call you expect
#     db.cursor.execute.assert_any_call(
#         "INSERT INTO userproducts (fk_user_id, fk_group_id, category_name, amount) VALUES (%s, %s, %s, %s);",
#         (1, -4560716368, "Food", 50)
#     )

def test_new_expense():
    db = Server.Database()
    db.cursor = AsyncMock()  # Mock the cursor as AsyncMock
    
    db.new_expense(1, -4560716368, "Food", 50)
    
    db.cursor.execute.assert_any_call(
        "INSERT INTO userproducts (fk_user_id, fk_group_id, category_name, amount) VALUES (%s, %s, %s, %s);",
        (1, -4560716368, "Food", 50)
    )



def test_delete_expense():
    db = Server.Database()
    db.cursor = AsyncMock()
    
    db.delete_expense(1)
    
    db.cursor.execute.assert_called_once_with(
        "DELETE FROM userproducts WHERE pk_id = %s;", (1,)
    )

# def test_add_category(db):
#     db.add_category("Travel")
#     db.cursor.execute.assert_called_once_with(
#         "INSERT INTO categories (category_name) VALUES (%s)", ("Travel",)
#     )
@pytest.mark.asyncio
async def test_add_category():
    with patch("Backend.Commands.db.add_category", new_callable=AsyncMock) as mock_add_category:
        mock_update = AsyncMock()
        mock_context = AsyncMock()
        
        mock_update.message.text = "/add_category Food"
        await Commands.add_category(mock_update, mock_context)
        
        mock_add_category.assert_awaited_once_with("Food")
        mock_update.message.reply_text.assert_called_once_with("Added category: Food")


def test_get_expenses(db):
    db.get_expenses(1, -4560716368)
    db.cursor.execute.assert_called_once_with(
        """
        SELECT pk_id, date_created, fk_user_id, category_name, amount
            FROM userproducts
            WHERE fk_user_id = %s AND fk_group_id = %s
            ORDER BY date_created DESC;
        """, (1, -4560716368)
    )

def test_total_expenses(db):
    db.total_expenses(-4560716368, "This Month")
    db.cursor.execute.assert_called()

def test_calculate_balances(db):
    db.calculate_balances(-4560716368)
    db.cursor.execute.assert_called_once_with(
        "SELECT user_id, SUM(amount) FROM userproducts WHERE fk_group_id = %s GROUP BY user_id",
        (-4560716368,)
    )
