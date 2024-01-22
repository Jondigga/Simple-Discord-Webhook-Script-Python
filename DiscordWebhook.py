import requests
from rich import print
from rich.color import Color
from configparser import ConfigParser
import os
import re

class ExitCommandException(Exception):
    pass

def is_valid_url(webhook_url):
    pattern = r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$'
    return bool(re.match(pattern, webhook_url))

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
config_file_path = os.path.join(script_directory, "config.ini")

config = ConfigParser()
config.read(config_file_path)

def send_message_to_discord_webhook(webhook_url, message):
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, json=data, headers=headers)

def messagesender():
    try:
        default_url = config["URL"]["default_url"]
        print(f"Your default URL is: {default_url}")
        webhook_url = input("Please input your Webhook URL! (To use the default one press enter!)\n")
        if webhook_url == "":
            webhook_url = default_url

        while is_valid_url(webhook_url) == False:
            webhook_url = input("The entered URL is not valid or the default URL hasn't been changed to a valid one.\nPlease enter a valid URL (type 'exit' to quit):\n")
            if webhook_url.lower() == "exit":
                raise ExitCommandException()

        def webhookconfigandsend():
            send_message_to_discord_webhook(webhook_url, message)

        repeat = True
        while repeat:
            message = input("What would you like to send to the discord webhook? (type 'exit' to quit)\n")

            if message.lower() == "exit":
                raise ExitCommandException()

            webhookconfigandsend()
            print("Message sent!")

            while True:
                answer = input("Would you like to send another message? Y/N (type 'exit' to quit)\n")

                if answer.lower() == "n":
                    repeat = False
                    break
                elif answer.lower() == "y":
                    break
                elif answer.lower() == "exit":
                    raise ExitCommandException()
                else:
                    print("Please answer with Y, N, or 'exit'")
                    
    except ExitCommandException:
        raise ExitCommandException()

def beginning():
    global default_url  
    beginning_mode = True

    while beginning_mode:
        try:
            reply = input("""
These are your controls:
[start] to start the message sender
[change] to change the default webhook url
[exit] to quit

""")
            if reply == "start":
                messagesender() 

            elif reply == "change":
                change_default(config)

            elif reply == "exit":
                print("Goodbye!")
                quit()

            else:
                print("Please answer with one of the words given above!\n")

        except ExitCommandException:
            pass

def change_default(config):
    try:
        change_mode = True

        while change_mode:
            if not config.has_section("URL"):
                print("Section 'URL' does not exist in the config file.")
                return

            current_value = config.get("URL", "default_url")
            print(f"\nThe current default url is {current_value}")
            new_default = input(f"Enter the new default Webhook URL (type 'exit' to quit):\n")
            
            if new_default.lower() == "exit":
                raise ExitCommandException()

            config.set("URL", "default_url", new_default)

            with open(config_file_path, "w") as configfile:
                config.write(configfile)

            print("Configuration updated successfully!")

    except ExitCommandException:
        raise ExitCommandException()

font = '''
██████  ██ ███████  ██████  ██████  ██████  ██████          
██   ██ ██ ██      ██      ██    ██ ██   ██ ██   ██         
██   ██ ██ ███████ ██      ██    ██ ██████  ██   ██         
██   ██ ██      ██ ██      ██    ██ ██   ██ ██   ██         
██████  ██ ███████  ██████  ██████  ██   ██ ██████          
'''

print(font)
print("Welcome to the Discord Webhook Message sender!")

beginning()
