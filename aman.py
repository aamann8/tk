import requests
import time
from datetime import datetime
from colorama import Fore, Style

# Logo and introduction
logo = """
  /$$$$$$   /$$$$$$  /$$      /$$ /$$$$$$$$ /$$$$$$$$ /$$$$$$$ 
 /$$__  $$ /$$__  $$| $$$    /$$$| $$_____/| $$_____/| $$__  $$
| $$  \__/| $$  \ $$| $$$$  /$$$$| $$      | $$      | $$  \ $$
|  $$$$$$ | $$$$$$$$| $$ $$/$$ $$| $$$$$   | $$$$$   | $$$$$$$/
 \____  $$| $$__  $$| $$  $$$| $$| $$__/   | $$__/   | $$__  $$
 /$$  \ $$| $$  | $$| $$\  $ | $$| $$      | $$      | $$  \ $$
|  $$$$$$/| $$  | $$| $$ \/  | $$| $$$$$$$$| $$$$$$$$| $$  | $$
 \______/ |__/  |__/|__/     |__/|________/|________/|__/  |__/
  
 /$$   /$$ /$$      /$$ /$$$$$$$                               
| $$  / $$| $$  /$ | $$| $$__  $$                              
|  $$/ $$/| $$ /$$$| $$| $$  \ $$                              
 \  $$$$/ | $$/$$ $$ $$| $$  | $$                              
  >$$  $$ | $$$$_  $$$$| $$  | $$                              
 /$$/\  $$| $$$/ \  $$$|    o $$  | $$                              
| $$  \ $$| $$/   \  $$| $$$$$$$/                              
|__/  |__/|__/     \__/|_______/                               
                                                        
--------------------------------------------------------------  
      WELCOME TO THE MULTI TOKEN POST TOOL
--------------------------------------------------------------                                                                                
       THIS TOOL CREATED BY AALAM HASHMI
--------------------------------------------------------------  
        MULTI IDZ MULTI PAGE WALLS MULTI FILE LOADER TOOL
--------------------------------------------------------------                            
"""

# Print the logo
print(Fore.CYAN + logo + Style.RESET_ALL)

# Prompt for token file
token_file = input("ENTER TOKEN FILE PATH: ")

# Read access token IDs from file
with open(token_file, 'r') as f:
    access_tokens = f.read().splitlines()

# Prompt for the number of user IDs
num_user_ids = int(input("HOW MANY POSTS YOU WANT FOR LOADER: "))

# Define dictionaries to store user IDs and message files
user_messages = {}
haters_name = {}

# Prompt for user IDs, hater names, and message files
for i in range(num_user_ids):
    user_id = input(f"ENTER POST ID #{i+1}: ")
    hater_name = input(f"ENTER HATER NAME FOR POST ID {user_id}: ")
    message_file = input(f"ENTER MESSAGES FILE FOR {user_id}: ")
    user_messages[user_id] = message_file
    haters_name[user_id] = hater_name

# Prompt for delay time in messages
while True:
    try:
        delay_time = int(input("ENTER DELAY (in seconds) FOR MESSAGES: "))
        break
    except ValueError:
        print("Please enter a valid integer for delay time.")

# Prompt for delay before repeating the process
while True:
    try:
        repeat_delay = int(input("ENTER DELAY (in seconds) BEFORE REPEATING THE PROCESS: "))
        break
    except ValueError:
        print("Please enter a valid integer for repeat delay.")

# Function to get profile name using an access token
def get_profile_name(access_token):
    try:
        url = f'https://graph.facebook.com/v17.0/me?access_token={access_token}'
        response = requests.get(url)
        data = response.json()
        if 'name' in data:
            return data['name']
        else:
            print(f'{Fore.RED}Profile name not found for access token: {access_token}{Style.RESET_ALL}')
            return None
    except requests.exceptions.RequestException as e:
        print(f'{Fore.RED}Request error: {str(e)}{Style.RESET_ALL}')
        return None
    except Exception as e:
        print(f'{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}')
        return None

# Function to send a message to a user's inbox conversation using an access token
def send_message(access_token, user_id, hater_name, message):
    try:
        url = f"https://graph.facebook.com/v15.0/{user_id}/comments"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
            'Referer': 'https://www.facebook.com/',
            'Authorization': f'Bearer {access_token}'
        }
        data = {'message': hater_name + ' ' + message}

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{Fore.BLUE}[{current_time}] {Fore.YELLOW}Comment sent successfully to user ID {user_id}: {Fore.GREEN}{hater_name + message}')
        return True

    except requests.exceptions.RequestException as e:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{Fore.RED}[{current_time}] {Fore.RED}Request error sending comment to user ID {user_id}: {str(e)}{Style.RESET_ALL}')
        return False

    except requests.exceptions.HTTPError as e:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{Fore.RED}[{current_time}] {Fore.RED}HTTP error sending comment to user ID {user_id}: {str(e)}{Style.RESET_ALL}')
        return False

    except Exception as e:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{Fore.RED}[{current_time}] {Fore.RED}An unexpected error occurred sending comment to user ID {user_id}: {str(e)}{Style.RESET_ALL}')
        return False

# Main loop to send messages
while True:
    total_successful_messages = 0
    total_unsuccessful_messages = 0

    # Iterate over the access tokens
    for i, access_token in enumerate(access_tokens):
        try:
            # Login using the access token and get the profile name
            profile_name = get_profile_name(access_token)
            if not profile_name:
                continue

            profile_number = i + 1
            access_token_id = access_token[:4] + '********'

            # Print the profile information
            print(f'{Fore.YELLOW}Profile {profile_number} (ID: {access_token_id}): {profile_name}')
            print('--------------------------------------------')

            # Iterate over the user IDs and messages
            for user_id, message_file in user_messages.items():
                # Read messages from the message file for the current user ID
                with open(message_file, 'r') as f:
                    messages = f.read().splitlines()

                # Get the hater name for the current user ID
                hater_name = haters_name[user_id]

                # Get the messages count for the current user
                messages_count = len(messages)

                # Get the current message index for the user ID
                message_index = i % messages_count

                # Get the message for the current index
                message = messages[message_index]

                if send_message(access_token, user_id, hater_name, message):
                    total_successful_messages += 1
                else:
                    total_unsuccessful_messages += 1

                time.sleep(delay_time)  # Delay between each message

            # Print Facebook ID, message, and current date/time after message is sent
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{Fore.MAGENTA}Facebook ID: {user_id}')
            print('--------------------------------------------')
            print('Next ID Ready To Send Comment')
            print('--------------------------------------------')

        except requests.exceptions.RequestException as e:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{Fore.RED}[{current_time}] Internet disconnected. Reconnecting in 10 seconds...{Style.RESET_ALL}')
            time.sleep
