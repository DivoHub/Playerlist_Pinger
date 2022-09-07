# Playerlist Pinger For Java Edition Minecraft   ![MC Icon](https://iili.io/6Jdw5g.png)
 
Simple console application that pings user and logs when any specified players appear online in a given server IP (Java Edition)

## Overview
Makes GET requests to minecraftlist.com to fetch player list data on user's behalf

## Dependencies
```bash
pip install bs4
pip install simpleaudio
pip install requests
```
## Usage
1. Clone Repo or download/unzip folder onto local machine

2. Install dependencies using PIP

3. Open terminal from repository folder then run the following command:
```bash
python pinger.py
```
Or

```bash
python3 pinger.py
```
4. Type and enter 'fresh' to initialize configurations.

5. Type and enter 'start' to begin running checker

- Type and enter 'help' to see full list of commands

## Contributing
Pull requests are welcome. Please specify fixes/changes.  
Telling me how trash the code is is also welcome


## License
[MIT](https://choosealicense.com/licenses/mit/)


## Issues
- Difficulties parallelizing threads to have separate refresh intervals (Sharing the same refresh interval 60 seconds is temporary solution)
- No UI 
