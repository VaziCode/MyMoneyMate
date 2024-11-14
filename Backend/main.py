import os
import sys
import argparse
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import uuid


# from Backend.Commands import logger
from Backend.Responses import responses, get_price, get_category, valid_email, help_response
from Backend.config import (
	TOKEN,
	BOT_USERNAME,
	Category,
	Button,
	Status,
	Command,
	categories_config,
	categories_config_dict,
	PASSWORD_MAX_LENGTH,
	PASSWORD_MIN_LENGTH,
	LOGIN_NAME_MIN_LENGTH,
	LOGIN_NAME_MAX_LENGTH
)
# from Backend.backend import Database, get_categories, write_category, remove_category, validate_input
from Backend.Server import Database, validate_input

from telegram import (
	InlineKeyboardButton,
	InlineKeyboardMarkup,
	Update
)

from telegram.ext import (
	Application,
	CommandHandler,
	ContextTypes,
	MessageHandler,
	filters,
	CallbackQueryHandler
)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	query = update.callback_query
	await query.answer()
	data = query.data
	group_id = query.message.chat.id
	
	# Handle cancel button
	if data.lower() == "cancel":
		await query.edit_message_text(text="Cancelled")
		return
	
	# Handle expense amount entry
	if data.isdigit():
		amount = int(data)
		context.user_data['amount'] = amount  # Store the amount
		await query.edit_message_text("Please select a category for this expense.")
		# Here we can show the category selection buttons if applicable
		return
	
	# Check if the user selected a stats time period
	stats_responses = ["This Month", "Last Month", "All Time"]
	currency_options = ["USD", "Euro", "NIS"]
	
	if data in stats_responses:
		context.user_data['time_period'] = data
		keyboard = [
			[InlineKeyboardButton("USD", callback_data="USD")],
			[InlineKeyboardButton("Euro", callback_data="Euro")],
			[InlineKeyboardButton("NIS", callback_data="NIS")]
		]
		reply_markup = InlineKeyboardMarkup(keyboard)
		await query.edit_message_text("Select the currency for your stats:", reply_markup=reply_markup)
		return
	
	# Check if the user selected a currency
	if data in currency_options:
		time_period = context.user_data.get('time_period')
		currency = data
		
		if time_period and currency:
			result = db.total_expenses(group_id, time_period, currency)
			if not result:
				await query.message.reply_text(f"No expenses found for {time_period} in {currency}.")
				return
			
			db.piechart(group_id, time_period, currency)
			db.barchart(group_id, time_period, currency)
			await query.message.reply_text(f"Total expenses for {time_period} in {currency}: {result}")
			await context.bot.send_photo(chat_id=group_id, photo=open('my_plot.png', 'rb'))
			if query.message.chat.type == 'group':
				await context.bot.send_photo(chat_id=group_id, photo=open('my_plot2.png', 'rb'))
			await query.message.delete()
			
			# Clear stored data
			context.user_data.pop('time_period', None)
			return
		
		await query.message.reply_text("Please select a time period first.")
		return
	
	# Handling category selection after an amount has been entered
	if context.user_data.get('amount') is not None:
		user_id = context.user_data.get('user_id')
		amount = context.user_data['amount']  # Get the stored amount
		try:
			db.new_expense(user_id, group_id, data, amount)  # Adding the expense
			await query.edit_message_text(text=f"Added expense: {data}  {amount}")
			context.user_data.pop('amount', None)  # Clear stored amount after adding
		except Exception as e:
			await query.edit_message_text(text=f"Error adding expense: {e}")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
	print(f'Update {update} caused error {context.error}')


# Run the program

from Backend import Commands



def initialize_app(host, database, user, password, port):
		# Initialize the database connection
		global db
		db = Database(host, database, user, password, port)
		Commands.db = db  # Pass the database instance to Commands
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="MyMoneyMate Database Configuration")
	parser.add_argument("--db_host", required=True, help="Database host address")
	parser.add_argument("--db_name", required=True, help="Database name")
	parser.add_argument("--db_user", required=True, help="Database username")
	parser.add_argument("--db_password", required=True, help="Database password")
	parser.add_argument("--db_port", type=int, required=True, help="Database port number")
	args = parser.parse_args()
	# Initialize the app with database parameters
	initialize_app(
		host=args.db_host,
		database=args.db_name,
		user=args.db_user,
		password=args.db_password,
		port=args.db_port,
	)
	
	# Initialize the application
	app = Application.builder().token(TOKEN).build()
	
	# Command handlers
	app.add_handler(CommandHandler(f"{Command.START.value}", Commands.start))
	app.add_handler(CommandHandler(f"{Command.HELP.value}", Commands.help_command))
	app.add_handler(CommandHandler(f"{Command.STATS.value}", Commands.stats))
	app.add_handler(CommandHandler(f"{Command.SIGN_IN.value}", Commands.sign_in))
	app.add_handler(CommandHandler(f"{Command.SET_LOGIN.value}", Commands.set_login))
	app.add_handler(CommandHandler(f"{Command.GET_LOGIN.value}", Commands.get_login))
	app.add_handler(CommandHandler(f"{Command.SET_PASSWORD.value}", Commands.set_password))
	app.add_handler(CommandHandler(f"{Command.GET_PASSWORD.value}", Commands.get_password))
	app.add_handler(CommandHandler(f"{Command.DELETE_EXPENSE.value}", Commands.delete_expense))
	app.add_handler(CommandHandler(f"{Command.EXPORT.value}", Commands.export))
	app.add_handler(CommandHandler(f"{Command.BRAKE_EVEN.value}", Commands.brake_even))
	app.add_handler(CommandHandler(f"{Command.ADD_CATEGORY.value}", Commands.add_category))
	app.add_handler(CommandHandler(f"{Command.DELETE_CATEGORY.value}", Commands.delete_category))
	app.add_handler(CommandHandler(f"{Command.DASHBOARD.value}", Commands.dashboard))
	app.add_handler(CommandHandler(f"{Command.SUM.value}", Commands.db.total_expenses))
	app.add_handler(CommandHandler("new", Commands.new_expense_command))
	app.add_handler(CommandHandler(f"{Command.LIST.value}", Commands.list_expenses))
	app.add_handler(MessageHandler(filters.COMMAND, Commands.unknown_command))
	
	# Click handler
	app.add_handler(CallbackQueryHandler(button))
	
	# Messages handler
	app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, Commands.handler))
	
	# Log all errors
	app.add_error_handler(error)
	
	print('MyMoneyMate Is Running...')
	# Run the bot
	app.run_polling(poll_interval=1)
