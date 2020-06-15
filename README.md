<p align="center">
  <img width="256px" height="256px" src="https://i.living-me.me/i/fckk.png">
</p>

<h1 align="center">wiiu-tcp-rich-presence</h1>

A small Python program that sends Wii U activity to your Discord status using [pygecko](https://github.com/wiiudev/pyGecko), [pypresence](https://github.com/qwertyquerty/pypresence), and the CemUI API.

Portions of the code (such as for reading memory and the API) are based on a [similar project](https://github.com/NexoDevelopment/WiiU-DiscordRichPresence) by NexoDevelopment.

This is still very much unfinished - if you run into a bug, want to see something implemented, or just want to contribute, feel free to file an issue and/or fork and submit a pull request.

One thing to note: This application only **reads** from memory and **does not** alter gameplay in any way, so it ***should*** be safe to use online. Regardless, as with any homebrew, the possibility of a ban, however slight, is always there. Please don't hold me responsible if something happens.

With all that out of the way, let's talk about the application!

## Features

- Automatically connects to TCPGecko on your Wii U, detects title launches, and updates your status on the fly
- Automatically gets your game's title from the CemUI API
- Displays your Nintendo Network ID (optional)
- Displays game icons for supported titles (currently Breath of the Wild, Mario Kart 8, Super Mario 3D World, Super Mario Maker, Super Smash Bros for Wii U, Splatoon, and Wind Waker HD)
- Support for US, EU, and Japanese titles
- Support for the Wii U Menu
- Text wrapping (kinda) for longer title names
- Error handling and automatic reconnection for unexpected disconnects (usually when switching titles)
- Manual mode and "hidden" debug mode for troubleshooting
- Simple, relatively decent looking text-based UI

## Setup

Before starting, you'll want to install the latest version of [Python 3](https://www.python.org/downloads/) (for obvious reasons) and [Git](https://git-scm.com/) for your OS. If you don't want to or can't install Git, you can also download the .zip [here](https://github.com/dmgrstuff/wiiu-tcp-rich-presence/archive/master.zip) and extract the files manually. You'll also need TCPGecko (downloadable from the Homebrew App Store or [this repo](https://github.com/BullyWiiPlaza/tcpgecko/)) on your Wii U's SD card and a homebrew entry point (Haxchi, browser exploit, CBHC, whatever).

**1.** First things first, navigate to a convenient place in your terminal and run `git clone https://github.com/dmgrstuff/wiiu-tcp-rich-presence.git && cd wiiu-tcp-rich-presence`. This will clone the repo into a correspondingly named folder and navigate into that folder. Alternatively, download the .zip mentioned above and extract it somewhere convenient.

**2.** Next, you'll want to run `python -m pip install pypresence`. This should install the rich presence library we're using using Python's package installer.

**3.** Rename `config.example.py` to `config.py` and open the file in a text editor. Fill in your Wii U's IP, your NNID (if you want to display it - if not, set `show_nnid` to `False`) and any other options you'd like to change.

**4.** Moving over to your Wii U, boot into the Homebrew Launcher and run TCPGecko. Press A to install it into memory (we won't need SD cheats, obviously) and you'll be sent back to the Wii U Menu.

**5.** From here, run `python3 rpc.py` in your terminal and you'll see the program's main menu. Unless you run into issues, Automatic mode is the easiest and best option here. If Python throws an `InvalidPipe` exception, make sure Discord is running.

**6.** Assuming everything went according to plan, you should now see whatever you're doing on your Wii U in your status. You can now launch your game of choice, show off to the world, brag to your friends, or whatever you want.

Just make sure they don't read my code because it's really, ***really*** bad.

## Known issues

- Certain games or apps might cause the console to freeze if TCPGecko tries to connect. As far as I know, this is an issue with TCPGecko itself, so it may or may not be fixed.
- If you're using an application that's accessible in game (like the Friend List, Internet Browser, eShop, etc.) the program will hang. This happens because TCPGecko doesn't seem to send any data when in these types of titles. This also happens with JGecko U so again, it's likely not something I can fix.
- Trying to launch Rich Presence without Discord running will crash the application. It's normal to throw an exception but I'd like to handle it a little more smoothly.
- Wii VC games don't (and likely will never) work due to the way vWii and cafe2wii works.

## Planned features

- Better translation/localization support
- Detailed stats for games like Splatoon, Mario Kart 8, Smash, etc.
- Less spaghetti in the code

## Credits

**NexoDevelopment** and **2secslater** for the original idea behind and implementations of this project  
**RedDucks** for the CemUI API

> Taken from [https://github.com/BullyWiiPlaza/tcpgecko](https://github.com/BullyWiiPlaza/tcpgecko):

**dimok** for Homebrew Launcher project engine/base  
**BullyWiiPlaza** for further development of advanced/efficient features  
**wj44** for porting [`pyGecko`](https://github.com/wiiudev/pyGecko) to the Homebrew Launcher and some development  
**Marionumber1** for exploit development and TCP Gecko Installer contributions  
**NWPlayer123** for the `pyGecko` client library  
**Chadderz** for the original `TCP Gecko Installer`  
**Kinnay** for some `DiiBugger` code this project made use of
