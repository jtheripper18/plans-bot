#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import pymysql

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    user = update.message.from_user
    
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hello " + user.first_name)
    
def help(bot, update):
    # Open database connection
    db = pymysql.connect("172.30.67.51", "userLDD", "lUWN0swSAp6EiQf8", "botdb")
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! ' + data[0] + ' ')
    
    # disconnect from server
    db.close()
    
def plans(bot, update):
    """List upcoming plans."""
    db = pymysql.connect("172.30.67.51", "userLDD", "lUWN0swSAp6EiQf8", "botdb")
    cursor = db.cursor()
    cursor.execute("SELECT pid, pname, ploc, pmeet, ptran, pdt from plans")
    # fetchall() enter 2 index [][] row x column
    # fetchone() enter 1 index [] column
    rows = cursor.fetchall()
    strmsg = ""
    
    for row in rows:
        strmsg += "Plan ID: %s\n"
                  "Plan: %s\n"
                  "Plan Location: %s\n"
                  "Meeting Point: %s\n"
                  "Transport: %s\n"
                  "Date / Time: %s\n"
                  % (row[0], row[1], row[2], row[3], row[4], row[5])
    
    update.message.reply_text(strmsg)
    
    db.close()

def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("526123359:AAFE_SXIa15DyjndDBF1bhcaIEeLfLz2iJ0")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("plans", plans))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
