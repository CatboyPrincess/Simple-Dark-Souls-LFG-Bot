# Simple Dark Souls LFG Bot

Here is a simple bot to help players find other players who are playing Soulsborne games (Demon's Souls, Dark Souls N, and Bloodborne at the time of writing).

#### Note

Any guides that follow are written for people who are who have a level of computer literacy slightly ahead of "I know how to use a mouse and keyboard" and hopefully the guides will suffice. Or not. Sorry!! ;A;

## License

See the file `LICENSE`.

## Commands

These are your commands:

* !request [game] [platform] [SL or SM] [optional note with a character limit] -> Add yourself to the game request list for one hour

* !list -> List players of the past hour (and remove older ones)

* !clear -> Clears requests made by you. Also removes stale requests

* !status -> Reports if the bot is enabled or not and other info

* !ADMIN_logout -> Logs the bot out

* !ADMIN_enable -> Enables bot's public functions

* !ADMIN_disable -> Disables bot's public functions

* !help -> Omnipresent and omniscient. Ask the bot for help!

## Basic Usage

After setting up the bot, the general usage involves people using `!request` and `!list` to facilitate finding other players.

Use of `!clear` by players will be primarily for when they want to take down their ad for whatever reason (need to leave, found enough players, etc.)

The `!ADMIN_xyz` commands are available to people in roles that are flagged with Administrator or Manage Server. The owner has access as well. Use at your discretion.

## Installing

First, you'll want to install the latest version of [Python 3][py] for your platform. At the time of writing it is 3.5.2. When you go to install it, make sure to mark the option "Add Python 3.5 to PATH".

Now, follow instructions in the `README.md` for [discord.py][discord_py].

You don't need voice so this should suffice (from the link):

```
py -3 -m pip install -U discord.py
```

This requires Python's directory to be on your PATH in your system environment variables.

Download and save `Simple-Dark-Souls-LFG-Bot.py` and `start_bot.bat` to some place.

[py]: https://www.python.org/
[discord_py]: https://github.com/Rapptz/discord.py

## Readying the Bot

Go to [Discord's Apps section][das] and select "New Application"

Fill out the name, description, avatar to your liking.

Save changes.

Add a "Redirect URI" and fill it in with `http://localhost:5000/callback`. I guess it's just the IP of the server host. I wouldn't know. If you're running the bot on the same machine as you use, then the localhost address will work. (Otherwise you probably know what to do with this field better than I do.)

Click "Create a Bot User".

You should probably leave "Public Bot" and "Require OAuth2 Code Grant" unchecked but frankly I don't know what to do with these either.

Nor do I know what to do with RPC Origin(s). lol :'D

Take note of the "Client ID". You will need it later.

Save changes.

Click on "click to reveal" for "Token" under "App Bot User".

Copy the text that appears. This is the token.

Open up the file `Simple-Dark-Souls-LFG-Bot.py` with a text editor like Notepad and look for

```
bot_token = 'text'
```

Replace `text` with your token. You should end up with something like:

```
bot_token = '01234.devour.all.humans.56789'
```

Save the file.

## don't give up, skeleton!

To get the bot into your server, you will need to this link: https://discordapp.com/oauth2/authorize?&client_id={bot-id}&scope=bot&permissions=3072&response_type=code

However, you will need to make one modification it first...

Substitute `{bot-id}` with the "Client ID" you noted earlier.

What should happen is that you are asked if you want to add your bot. If so, success! Go ahead and add the bot.

## Running the Bot

If you're on Windows, just double-click on `start_bot.bat`. If you're not on Windows then "you can do it, I believe in you".

THE BOT IS NOW RUNNING ~~probably~~ （‐＾▽＾‐）

[das]: https://discordapp.com/developers/applications/me
