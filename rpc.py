# Importing libraries (probably too many tbh)
from pypresence import Presence
from tcpgecko import TCPGecko
import time
import urllib.request
import urllib.parse
import re
import json
from config import *
import os
import struct

# Fair warning - I barely have any Python experience so there's no doubt a lot of this code could be significantly improved.
# I kinda got tired of writing this after a while, so some parts will look a bit rushed. (and there's plenty of global spam if you're into that)
# With all that said, this thing actually somehow works (at least it should) and I'm pretty surprised I even got this far.
# Credits are at the bottom of the README.md if you're interested.

release_date = "2020/04/25"

# Variables
debug_mode = False
tcp_connected = False
rpc_running = False
debug_keyword = "supersecretdebugmode" # type to enable debug mode
debug_disable_keyword = "notsosecretnormalmode" # type to disable debug mode (if you would want to do that)

# Functions
def tcp_connect():
    global tcp
    global tcp_connected
    try: 
        tcp = TCPGecko(ip) # connect to your Wii U
    except TimeoutError:
        clear()
        print("Connection timed out. Please try again.") 
        menu()
    tcp_connected = True
    clear()
    print("Successfully connected to your Wii U at " + ip + ".")
    print("Waiting for Discord...")

def launch_rpc():
    global RPC
    global start_time
    global rpc_running
    RPC = Presence(client_id)  # Initialize the client class
    RPC.connect() # Start the handshake loop
    rpc_running = True
    start_time = str(int(time.time()))
    while True:  # The presence will stay on as long as the program is running
        clear()
        try:
            global running_title
            running_title = "000" + str(format(struct.unpack(">Q", tcp.readmem(0x10013C10, 8))[0] , "x")) # get the current title ID from memory
            title_split = re.findall("........" , running_title) # format title ID for CemUI API
            running_title = title_split[0] + "-" + title_split[1]
        except ConnectionResetError: # auto-reconnection if connection closes unexpectedly
            print("Connection lost (likely switching titles). Reconnecting...")
            time.sleep(3)
            tcp_connect()
            running_title = "000" + str(format(struct.unpack(">Q", tcp.readmem(0x10013C10, 8))[0] , "x")) # get the current title ID from memory
            title_split = re.findall("........" , running_title) # format title ID for CemUI API
            running_title = title_split[0] + "-" + title_split[1]
            
        title_info()
        get_icon()
        update_rpc()

        # Report detected information for rich presence
        print("Rich Presence updated with the following information.\n")
        print("Status: " + details)
        print("Game Icon: " + large_image)
        print("Nintendo Network ID: " + nnid)
        print("\nThe running application's title ID (hex) is " + running_title + ".")
        print("\nUpdating again in 15 seconds.")
        print("\nPress Ctrl+C or close your terminal to stop.")

        time.sleep(15) # Can only update rich presence every 15 seconds
        tcp # connect to your Wii U again

def launch_rpc_debug():
    global RPC
    global start_time
    global running_title
    global rpc_running
    RPC = Presence(client_id)  # Initialize the client class
    RPC.connect() # Start the handshake loop
    start_time = int(time.time())
    rpc_running = True    
    running_title = debug_running_title

    while True:  # The presence will stay on as long as the program is running
        clear()

        title_info()
        get_icon()
        update_rpc()

        print("Rich Presence updated with the following information.\n")
        print("Status: " + details)
        print("Game Icon: " + large_image)
        if show_nnid == True:
            print("Nintendo Network ID: " + nnid)
        print("\nRich Presence is currently running in test mode.")
        print("\nUpdating again in 15 seconds.")
        print("\nPress Ctrl+C or close your terminal to stop.")

        time.sleep(15) # Can only update rich presence every 15 seconds

def update_rpc():
    if show_nnid == True:
        if wrap_title == True:
            RPC.update(details=line_1 , state=line_2 , small_image="nnid", small_text=nnid , large_image=large_image , large_text=large_text , start=start_time)
        else:
            RPC.update(details=details , small_image="nnid" , small_text=nnid , large_image=large_image , large_text=large_text , start=start_time)
    else:
        if wrap_title == True:
            RPC.update(details=line_1 , state=line_2 , large_image=large_image , large_text=large_text , start=start_time)
        else:
            RPC.update(details=details , large_image=large_image , large_text=large_text , start=start_time)

        
def title_info():
    global game
    global running_title
    global details
    global line_1
    global line_2
    global wrap_title
    url = "https://cemui.com/api/v2/GetGame/title_id/" + running_title # send the current title ID
    data = urllib.request.urlopen(url).read().decode("utf-8")
    try: game = json.loads(data)["game_title_clean"]
    except KeyError:
        game = "Wii U Menu"
        details = "In the " + game
        get_icon()
    details = "Playing " + game

    spaces = game.count(" ")
    if spaces >= 3:
        line_1 = "Playing " + " ".join(game.split(" ",3)[:3])
        line_2 = " ".join(game.split(" ",3)[-1:])
        wrap_title = True
    else:
        line_1 = "Playing " + game # pretty sure this is redundant but python will yell at me if I don't define it
        wrap_title = False

def get_icon(): # pre-defined icons for some titles, this will likely be reworked / de-spaghetified in the future
    global game
    global large_image
    if game == "Splatoon":
        large_image = "splatoon"
    elif game == "MARIO KART 8":
        large_image = "mariokart8"
    elif game == "The Legend of Zelda Breath of the Wild":
        large_image = "breath_of_the_wild"
    elif game == "The Legend of Zelda The Wind Waker HD":
        large_image = "wind_waker_hd"
    elif game == "Super Mario 3D World":
        large_image = "super_mario_3d_world"
    elif game == "Super Mario Maker":
        large_image = "super_mario_maker"
    elif game == "Super Smash Bros for Wii U":
        large_image = "super_smash_bros"
#   Adding your own icons (if using your own Discord application) - uncomment the next two lines, match the indents, and use this format        
#   elif game == "whatever the value of game_title_clean is for your title from https://cemui.com/api/v2/GetGame/title_id/[your title id]":
#       large_image = "whatever_you_named_the_icon_in_the_developer_portal"        
    else:
        large_image = "wiiu"

def header():
    if debug_mode == True:
        print("dmgr_'s wii u tcpgecko rich presence implementation - updated " + release_date + " [debug mode enabled]")
        print("─────────────────────────────────────────────────────────────────────────────────────────────\n")
    else:
        print("dmgr_'s wii u tcpgecko rich presence implementation - updated " + release_date)
        print("────────────────────────────────────────────────────────────────────────\n")

def clear(): # clear the screen
    if os.name == "nt": # clear screen
        os.system("cls")
    else:    
        os.system("clear")
    header()

def invalid():
    clear()
    print("That\'s not a valid choice.\n")

def menu(): # main application menu
    print("This application can run in two modes. What would you like to do?\n")
    print("1. Automatic - Automatically connect to your Wii U, launch rich presence, and switch games on the fly.\nMight cause issues with some games or your console to freeze in some cases.\n")
    print("2. Manual - Allows you to manually choose to connect to TCPGecko and/or start Rich Presence.\nYour status won't update automatically, but this can fix and/or help to diagnose issues.\n")
    print("0. Exit\n")
    mode_selection = input("Type the corresponding number. ")
    if mode_selection == "1":
        clear()
        print("Running in Automatic mode.\n")
        tcp_connect()
        launch_rpc()
    elif mode_selection == "2":
        clear()
        manual_menu()
    elif mode_selection == "0":
        exit()
    elif mode_selection == debug_keyword:
        enable_debug()
        menu()
    elif mode_selection == debug_disable_keyword:
        disable_debug()
        menu()
    else:
        invalid()
        menu()

def manual_menu(): # menu for manual mode
    if tcp_connected == True:
        print("Connected to your Wii U at " + ip + ". What now?\n")
        print("1. Reconnect to your Wii U at " + ip + " via TCPGecko")
    else:
        print("What would you like to do?\n")
        print("1. Connect to your Wii U at " + ip + " via TCPGecko") 
    print("2. Launch Rich Presence (requires TCPGecko to be running)")
    if debug_mode == True:
        print("3. Launch Rich Presence in test mode (uses pre-defined values from config.py)")
    print("0. Go back to the main menu\n")
    mode_selection = input("Type the corresponding number. ")
    if mode_selection == "1":
        tcp_connect()
        clear()
        manual_menu()
    elif mode_selection == "2":
        if tcp_connected == True:
            launch_rpc()
        else:
            clear()
            print("Please start TCPGecko before starting rich presence. If you'd like to run rich presence with pre-defined values, enable debug mode.\n")
            manual_menu()
    elif mode_selection == "3" and debug_mode == True:
        launch_rpc_debug()
    elif mode_selection == "0":
        clear()
        menu()
    elif mode_selection == debug_keyword:
        enable_debug()
        manual_menu()
    elif mode_selection == debug_disable_keyword:
        disable_debug()
        manual_menu()
    else:
        invalid()
        manual_menu()

def enable_debug():
    global debug_mode
    debug_mode = True
    clear()

def disable_debug():
    global debug_mode
    debug_mode = False
    clear()

# Actual code

clear() # clear screen and print header
      
if "." not in ip:
    print("Please enter your Wii U's IP in config.py.")
    print("Closing...")
    time.sleep(5)
    exit()

try: menu()
except KeyboardInterrupt: # handle Ctrl+C a little better
    print("\nClosing...")
    pass