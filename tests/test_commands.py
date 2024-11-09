import pytest
from Backend import Commands
from unittest.mock import AsyncMock, MagicMock, patch
from Backend.Commands import (
    new_expense_command,
    export,
    delete_expense,
    add_category,
    list_expenses,
    stats,
    brake_even
)
from telegram import Update, User, Chat
import sys
print(sys.path)
@pytest.fixture
def update():
    user = User(id=12345, first_name="TestUser", is_bot=False)
    chat = Chat(id=-4560716368, type="group")
    update = Update(update_id=1, message=AsyncMock(from_user=user, chat=chat))
    return update

@pytest.fixture
def context():
    return AsyncMock()

@patch("Backend.Commands.db")
@pytest.mark.asyncio
async def test_new_expense_command():
    with patch("Backend.Database.Database.new_expense", new_callable=AsyncMock) as mock_new_expense:
        mock_update = AsyncMock()
        mock_context = AsyncMock()
        mock_update.message.text = "/new Food 50"

        await Commands.new_expense_command(mock_update, mock_context)

        mock_new_expense.assert_awaited_once_with(1, -4560716368, "Food", 50)
        mock_update.message.reply_text.assert_awaited_once_with("Added expense: Food  50")


@patch("Backend.Commands.db")
@pytest.mark.asyncio
async def test_export(mock_db, update, context):
    mock_db.toExcel = AsyncMock()
    await export(update, context)
    mock_db.toExcel.assert_called_once_with(update.message.chat.id)

@patch("Backend.Commands.db")
@pytest.mark.asyncio
async def test_delete_expense(mock_db, update, context):
    context.args = ["1"]
    mock_db.delete_expense = AsyncMock(return_value=True)
    await delete_expense(update, context)
    mock_db.delete_expense.assert_called_once_with(1)

@patch("Backend.Commands.db")


@pytest.mark.asyncio
async def test_add_category():
    with patch("Backend.Commands.db.add_category", new_callable=AsyncMock) as mock_add_category:
        mock_update = AsyncMock()
        mock_context = AsyncMock()
        mock_update.message.text = "/add_category Food"

        await Commands.add_category(mock_update, mock_context)

        mock_add_category.assert_awaited_once_with("Food")
        mock_update.message.reply_text.assert_awaited_once_with("Added category: Food")


@patch("Backend.Commands.db")
@pytest.mark.asyncio
async def test_list_expenses(mock_db, update, context):
    mock_db.get_expenses = AsyncMock(return_value=[("2023-01-01", "Food", 100)])
    await list_expenses(update, context)
    mock_db.get_expenses.assert_called_once_with(update.message.from_user.id, update.message.chat.id)

@patch("Backend.Commands.db")
@pytest.mark.asyncio
async def test_stats(mock_db, update, context):
    mock_db.total_expenses = AsyncMock(return_value=100)
    await stats(update, context)
    mock_db.total_expenses.assert_called()

@patch("Backend.Commands.db")
@pytest.mark.asyncio
async def test_brake_even(mock_db, update, context):
    mock_db.calculate_balances = AsyncMock(return_value={"User1": -25, "User2": 25})
    await brake_even(update, context)
    mock_db.calculate_balances.assert_called_once_with(update.message.chat.id)
