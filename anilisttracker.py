import telebot
import anilist

bot = telebot.TeleBot('5242533550:AAERzY0hYkNEChMpfzELtV9cieoH0jXB1HE')


@bot.message_handler(commands=['start'])
def start(message):
    anilistDB = anilist.loadJSON()
    if str(message.chat.id) in anilistDB['chats']:
        bot.reply_to(message, f"Hi {message.from_user.first_name},\nI am Anilist Bot.\nI help you to manage your anilist account.\nTo know all features, type /help.\n\nTo add your profile to tracking list, type /adduser <username>.\nTo remove your profile from tracking list, type /removeuser <username>.\nTo see all users of this group, type /listusers.\n\nCreated by @w3Abhishek.\n\nThanks :)")
    else:
        anilistDB['chats'][message.chat.id] = {}
        bot.reply_to(message, "Hi,\nI am Anilist Bot.\nI help you to manage your anilist account.\nTo know all features, type /help.\n\nTo add your profile to tracking list, type /adduser <username>.\nTo remove your profile from tracking list, type /removeuser <username>.\nTo see all users of this group, type /listusers.\n\nCreated by @w3Abhishek.\n\nThanks :)")
    anilist.writeJSON(anilistDB)

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "Here's a list of features and commands:\n\n /help - shows this message\n\n /adduser <username> - adds a user to tracking list\n\n /removeuser <username> - removes a user from tracking list\n\n /listusers - lists all users of this group\n\n /anilist <username> - shows your anilist profile\n\n /anime <anime name> - shows anime info\n\n /manga <manga name> - shows manga info\n\n /character <character name> - shows character info\n\n /flex - flex your anilist profile\n\n /about - shows info about bot \n\n Created by @w3Abhishek. \n Thanks :)")



@bot.message_handler(commands=['adduser'])
def adduser(message):
    try:
        try:
            username = message.text.split()[1]
        except:
            bot.reply_to(message, "Please enter a valid Anilist username")
            return  None
        anilistDB = anilist.loadJSON()
        if str(message.chat.id) in anilistDB['chats']:
            if username not in anilistDB['chats'][str(message.chat.id)]:
                user = anilist.getUserId(username)
                if user is not None:
                    name = user[1]
                else:
                    name = user[0]
                userId = user[0]
                try:
                    activityNumber = anilist.anilistActivity(userId)['id']
                except:
                    activityNumber = 0
                anilistDB['chats'][str(message.chat.id)] = {username: {'activityNumber': activityNumber, 'name': name, 'userId': userId}}
                bot.reply_to(message, "Added Anilist account to our tracking list. I will send your Anilist updates to this group.")
            else:
                bot.reply_to(message, "This Anilist account is already added in our tracking list.")
        else:
            bot.reply_to(message, "Please start the bot first using /start.")
    except:
        bot.reply_to(message, "Please enter a valid Anilist username or maybe the API is down. Try again later.")

    anilist.writeJSON(anilistDB)


@bot.message_handler(commands=['removeuser'])
def removeuser(message):
    try:
        username = message.text.split()[1]
    except:
        bot.reply_to(message, "Please enter a valid Anilist username")
        return  None
    anilistDB = anilist.loadJSON()
    if str(message.chat.id) in anilistDB['chats']:
        if username in anilistDB['chats'][str(message.chat.id)]:
            del anilistDB['chats'][str(message.chat.id)][username]
            bot.reply_to(message, "Removed Anilist account from our tracking list.")
        else:
            bot.reply_to(message, "This Anilist account is not in our tracking list.")
    else:
        bot.reply_to(message, "Please start the bot first using /start.")

    anilist.writeJSON(anilistDB)
    
def trackActivity():
    anilistDB = anilist.loadJSON()
    for chatId in anilistDB['chats']:
        for username in anilistDB['chats'][chatId]:
            userId = anilistDB['chats'][chatId][username]['userId']
            name = anilistDB['chats'][chatId][username]['name']
            activityNumber = anilistDB['chats'][chatId][username]['activityNumber']
            aniActivity = anilist.anilistActivity(userId)
            newActivityNumber = aniActivity['id']
            if newActivityNumber != activityNumber:
                if aniActivity['media']['title']['english'] is not None:
                    animeName = aniActivity['media']['title']['english']
                else:
                    animeName = aniActivity['media']['title']['userPreferred']
                profileLink = 'https://anilist.co/user/' + str(userId)
                animeLink = 'https://anilist.co/anime/' + str(aniActivity['media']['id'])
                if aniActivity['progress'] == None:
                    final_message = f"[{name}]({profileLink}) {aniActivity['status']} [{animeName}]({animeLink})"
                else:
                    final_message = f"[{name}]({profileLink}) {aniActivity['status']} {aniActivity['progress']} of [{animeName}]({animeLink})"
                bot.send_photo(chatId, f"https://img.anili.st/media/{aniActivity['media']['id']}", caption=final_message, parse_mode='Markdown')
                anilistDB['chats'][chatId][username]['activityNumber'] = newActivityNumber
    anilist.writeJSON(anilistDB)


bot.polling(none_stop=True)

