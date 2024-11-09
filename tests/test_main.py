import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from Backend.main import button
from telegram import Update, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from Backend import main
import sys
print(sys.path)
@pytest.fixture
def update():
    callback_query = MagicMock(spec=CallbackQuery)
    callback_query.data = "USD"
    callback_query.message = MagicMock()
    return Update(update_id=1, callback_query=callback_query)

@pytest.fixture
def context():
    return MagicMock()

@patch("Backend.main.db")
@pytest.mark.asyncio
async def test_button_currency(mock_db, update, context):
    context.bot = AsyncMock()
    mock_db.total_expenses.return_value = 100
    await button(update, context)
    mock_db.total_expenses.assert_called_once_with(update.callback_query.message.chat.id, "USD")

@patch("Backend.main.db")
@pytest.mark.asyncio
async def test_button_cancel(mock_db, update, context):
    update.callback_query.data = "cancel"
    await button(update, context)
    update.callback_query.edit_message_text.assert_called_once_with(text="Cancelled")

@patch("Backend.main.db")
# @pytest.mark.asyncio
# async def test_button_add_expense(mock_db, update, context):
#     context.user_data = {'amount': 100, 'user_id': 12345, 'group_id': -4560716368}
#     update.callback_query.data = "Food"
#     await button(update, context)
#     mock_db.new_expense.assert_called_once_with(12345, -4560716368, "Food", 100)

def test_button_add_expense():
    with patch("Backend.main.db.add_expense", new_callable=AsyncMock) as mock_add_expense:
        button = main.button()  # Assuming button is defined in main.py
        # button.add_expense(1, -4560716368, "Food", 50)
        
        mock_add_expense.assert_awaited_once_with(1, -4560716368, "Food", 50)


def setup_module(module):
    # Mock db and assign to main.db if it doesn't exist
    main.db = MagicMock()

def test_button_currency():
    # Test that interacts with main.db
    main.db.some_method.return_value = "Expected Result"
    # Perform assertions here