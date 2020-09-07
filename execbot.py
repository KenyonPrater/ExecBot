"""
This code was written by Kenyon Prater on September 7 2020. I release it into
the public domain under the CC0 liscence by waiving all rights to the work
worldwide under copyright law, including all related and neighboring rights, to
the extent allowed by law. You can copy, modify, distribute, and perform the
work, even for commercial purposes, all without asking permission.

Telegram bot to run user-submitted commands in a bash process.
Obviously, do not run this anywhere other than a VM, and don't publicize the
bot you're running this on to anybody but designated friends.

I cannot overstate how bad of an idea it is to run this.
"""

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

import subprocess as sp
from subprocess import PIPE, STDOUT

import time

# Terminal part

def send_terminal(text):
    print(f"$: {text}")
    process.stdin.write(text + "\n")

def read_terminal(term_file):
    data = []
    while True:
        time.sleep(0.1)
        where = term_file.tell()
        read_line = term_file.readline()

        if read_line == "": # no more data in stream
            break
        data.append(read_line)
    term_file.seek(where) # leave file in a valid state
    resp = "".join(data)
    print(resp)
    return resp

def lazy_validation(text):
    return ("--no-preserve-root" in text) or (":(){ :|:& };:" in text)

def send_and_recieve(command):
    if (lazy_validation(command)):
        return 'alright look the validation bans exactly two substrings and you found one of them. be more creative'
    send_terminal(command)
    reply = read_terminal(f_read)
    return reply

################################################################################

def help_command(update, context):
    update.message.reply_text('Prefix a message with $ to run it in a terminal. Don\'t ruin my computer!')

def run_command(update, context):
    #strip the /run@.... out
    cmd = " ".join(update.message.text.split(" ")[1:])
    resp = send_and_recieve(cmd).strip()

    if (resp):
        update.message.reply_text(resp)
    else:
        # It's useful to have some prompts for when something finishes
        update.message.reply_text("...")

def main(token):
    """Start the bot."""

    print(f"using {token} as token!")
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("run", run_command))

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    if "yes" != input("This is a bad idea. by typing 'yes' you affirm that you understand the consequences of running this. "):
        sys.exit(0)
    shell = input("input path of shell to run: ")
    with open("token.token") as f:

        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        logger = logging.getLogger(__name__)

        # The bash shell will read from a pipe as stdin and write to test.log as stdout
        # Python will write to the pipe and read from test.log
        f_write = open("test.log", "w")
        f_read = open("test.log", "r")
        process = sp.Popen(shell, stdin=PIPE, stdout=f_write, stderr=STDOUT, bufsize=1, universal_newlines=True)
        f_write.close()

        tok = f.readline().strip()
        main(tok)
