# auto-update-assignment
## What?

A small piece of code to scrape assignments of lecture [Programmierparadigmen](https://pp.ipd.kit.edu/lehre/WS202122/paradigmen/index.php?lang=de) and send the updates through Telegram Bot. (Set variable `chat_id` to send message to your account/ others account/a channel).

## Why?

The reasons for this piece of code are:

- Instead of using official learning platform [Ilias](https://ilias.studium.kit.edu/), all the assignments of this lecture are updated on [this](https://pp.ipd.kit.edu/lehre/WS202122/paradigmen/index.php?lang=de) website.
- I'm too lazy to refresh the page and check if there's new assignment there.
- It's fun xD


## How?

 - scrape the lecture page and get the html content.
 - find the assignment table and get all assignment URLs.
 - compare with the result of last scrape (saved as a local file), if new assignment material found, update the local file and send the updates to me through Telegram Bot.

## Requirements

- [Python3](https://www.python.org/downloads/)
- Library dependencies:

```Python
import bs4, requests, os
import urllib.parse as ul
```
- A telegram account.
- A telegram bot (Use [BotFather](https://t.me/botfather) to create new bot accounts if you don't have one).
- Optional: crontab as scheduler to run it on Linux machine.


## Usage

```Shell
$ pyhon3 updater.py
```
## Scheduling
Crontab is a job scheduler on Ubuntu. Since the assignment is always due on Friday, I set the scheduler to run at minute 15 past every hour from 14 through 18 on Friday.
```Shell
$ crontab -e
```

```Shell
15 14-18 * * 5 /path/to/python3 /path/to/updater.py >> /path/to/cron.log 2>&1
```
