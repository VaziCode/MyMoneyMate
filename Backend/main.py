
import os
import sys
import uuid

from Backend import Commands, Responses, config
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
from Backend.backend import Database, validate_input

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
    
    # Check if the user selected a stats time period
    stats_responses = ["This Month", "Last Month", "All Time"]
    currency_options = ["USD", "Euro", "NIS"]
    
    if data in stats_responses:
        # Store the time period in user_data and prompt for currency selection
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
        # Retrieve stored time period and selected currency
        time_period = context.user_data.get('time_period')
        currency = data
        
        # Ensure time period and currency are set
        if time_period and currency:
            # Calculate total expenses in the selected currency
            result = db.total_expenses(group_id, time_period, currency)
            if not result:
                await query.message.reply_text(f"No expenses found for {time_period} in {currency}.")
                return
            
            # Generate charts in the selected currency
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



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')




# Run the program

from Backend import Commands


if __name__ == '__main__':
    #sys.stdout.reconfigure(encoding='utf-8')
    db = Database()
    
    #os.environ["PYTHONIOENCODING"] = "utf-8"
    app = Application.builder().token(TOKEN).build()
    
    
    #--------------------------------------------------------------------------
    #---------------------------COMMAND HANDLERS-------------------------------
    #--------------------------------------------------------------------------    #
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
    app.add_handler(CommandHandler(f"{Command.SUM.value}",Commands.db.total_expenses))
    app.add_handler(CommandHandler("new", Commands.new_expense_command))
    app.add_handler(CommandHandler(f"{Command.LIST.value}", Commands.list_expenses))
    app.add_handler(MessageHandler(filters.COMMAND, Commands.unknown_command))
    
    #click handler
    app.add_handler(CallbackQueryHandler(button))

    # Messages handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, Commands.handler))
    
    # Log all errors
    app.add_error_handler(error)

    print('Polling...')  # TODO: delete this debug line
    # Run the bot
    app.run_polling(poll_interval=1)
