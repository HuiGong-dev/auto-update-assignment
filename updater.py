import bs4, requests, os
import urllib.parse as ul

#URL of lecture programming paradigmen
url = "https://pp.ipd.kit.edu/lehre/WS202122/paradigmen/uebung/"
#stored html file of lecture page from last scrape
page_storage = "page_storage.html"
#Telegram bot token
token = "[your_telegram_bot_token]"
#Send updates to this telegram user
chat_id = "[your_chat_id]"

#Get propa ws2021 uebungspage
def get_page(url):
    page = requests.get(url)
    page.raise_for_status()
    return page.text

#Get uebungs material table
def get_table(page):
      #Store contengs of the website under soup
      soup  = bs4.BeautifulSoup(page, 'lxml')
      #get first table which contains uebungsmaterial
      first_table = soup.find_all('table')[1]
      return first_table

#Get links of materials in the table
def get_uebung_links(table):
    links = []
    #get links from the table
    for row in table.find_all('tr')[1:]:
        try:
            for anchor in row.find_all('td')[2].find_all('a'):
                links.append(anchor['href'])
        except ValueError:
            continue #ignore blank/empty row
    return links

# Get what has been changed in the table.
# Return added item list and deleted item list
def getDifference(fresh_links, storage_links):
    added = []
    # deleted = []
    for item in fresh_links:
          if item not in storage_links:
              added.append(url + item)
    # for item in storage_links:
    #     if item not in fresh_links:
    #         deleted.append(url + item)
    return added

# Prepare result text for telegram bot
def formResultText(added_list):
    length = len(added_list)
    if length == 0:
        return "No update"
    else:
        updates = "Added:\n"
        for item in added_list[:(length - 1)]:
            updates += item + "\n"
        updates += added_list[length - 1]
        return updates

def makeUpdatesUrlFriendly(updates):
    return ul.quote_plus(updates)

def buildTelegramBotRequestUrl(token, chat_id, parsedUpdates):
    return "https://api.telegram.org/bot" + token + "/sendMessage?chat_id=" + chat_id + "&text={}".format(parsedUpdates)


#Compare fresh scraped page with last scrape. (If difference is found, we need to call telegram bot)
def compare(page_fresh, page_storage):
    fresh_links = get_uebung_links(get_table(page_fresh))
    if os.path.isfile("./" + page_storage):
        print("Storage file exists. Checking for update...")
        with open(page_storage, "r", newline='') as f:
            storage = f.read()
            storage_links = get_uebung_links(get_table(storage))
            f.close()
        if storage_links != fresh_links:
            with open(page_storage, "w", newline='') as f:
                f.write(page_fresh)
                f.close()
            callBot(getDifference(fresh_links, storage_links), token, chat_id)
        else:
            print('You are up to date.')
    else:
        with open(page_storage, "w", newline='') as f:
            print("Download page to local storage for the first time")
            f.write(page_fresh)
            f.close()
            print("Call bot first time")
            callBot(combineUrlWithLinks(url, fresh_links), token, chat_id)

def combineUrlWithLinks(url, link_list):
    url_links = []
    for link in link_list:
        url_links.append(url + link)
    return url_links


def callBot(added_list, token, chat_id):
    parsedUpdates = makeUpdatesUrlFriendly(formResultText(added_list))
    requests.get(buildTelegramBotRequestUrl(token, chat_id, parsedUpdates))

compare(get_page(url),page_storage)
