# Minebell   ![MC Icon](https://iili.io/6Jdw5g.png)
 
Simple console application that pings user and logs when any specified players appear online in a given server IP (Java Edition)

## Overview
Makes periodic GET requests to minecraft statistic sites to fetch player list data on given server.

Websites include:
- minecraft-statistic.net
- minecraftlist.com
- mcsrvstat.us

## Dependencies

- **Python V3.10** (or later)


- **simpleaudio**
  - License: MIT
  - [GitHub Repository](https://github.com/hamiltron/py-simple-audio)

- **mcstatus**
  - License: Apache License 2.0
  - [GitHub Repository](https://github.com/py-mine/mcstatus)

```bash
pip install simpleaudio
pip install mcstatus
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
4. Type and enter 'newconfig' to initialize configurations.

5. Type and enter 'start' to begin running checker

- Type and enter 'help' to see full list of commands

## Contributing
Pull requests are welcome. Please specify fixes/changes.  
Telling me how trash the code is is also welcome


## License
[MIT](https://choosealicense.com/licenses/mit/)


## Issues
- Existence of Global Variables
- No UI
