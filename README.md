# Minebell   ![MC Icon](https://iili.io/6Jdw5g.png)
 
Simple console application that pings user and logs when any specified players appear online in a given server IP (Java Edition)

## Overview
This application utilizes the ***mcstatus*** library to incrementally fetch server data on the user's behalf.



## Dependencies
- **Python V3.10** (or later)


- **simpleaudio**
  - License: MIT
  - [GitHub Repository](https://github.com/hamiltron/py-simple-audio)

- **mcstatus**
  - License: Apache License 2.0
  - [GitHub Repository](https://github.com/py-mine/mcstatus)

- **discord.py** | (Used only if integrating Discord Bot)
  - License: MIT
  - [GitHub Repository](https://github.com/Rapptz/discord.py)

- **python-dotenv** | (Used only if integrating Discord Bot)
  - License: BSD-3-Clause License
  - [GitHub Repository](https://github.com/theskumar/python-dotenv)


## Usage
1. Clone Repo or download/unzip folder onto local machine

2. Install dependencies using PIP

```bash
pip install -r requirements.txt
```

4. Open terminal from repository folder then run the following command:
```bash
python pinger.py
```
Or

```bash
python3 pinger.py
```
4. Type and enter 'newconfig' to initialize configurations.

5. Type and enter 'start' to begin running checker

- Type and enter 'help' to see full list of commands

**Example config.json file:**


 ![config example](https://i.ibb.co/B3pD02q/Screenshot-2023-09-02-113850.png)

---
### Discord Bot Implementation

1. Install dependencies using PIP
```bash
pip install -r requirements.txt
```
2. Create a Discord Bot following [this guide](https://discordpy.readthedocs.io/en/stable/discord.html)
- For scopes, only "bot" needs to be checked
- For permissions, only "send messages" needs to be checked

3. Run discord_bot.py inside the 'discord' directory

4. You will be prompted for the Bot Token. Copy, paste, then enter your Bot Token key.
5. Invite bot to your server.
6. Refer to the help.txt guide for commands

---

## Contributing
Pull requests are welcome. Please specify fixes/changes.  
Telling me how trash the code is is also welcome

## License
[MIT](https://choosealicense.com/licenses/mit/)


## Issues
- No UI for main application.
