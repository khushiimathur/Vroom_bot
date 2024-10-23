import telethon.sync as ts 
from telethon.sessions import StringSession
import requests
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Read environment variables (set these in Render's dashboard or .env file)
api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
bot_token = os.getenv("bot_token")

# Functions for specific commands
def list_drivers(year):
    url = f'http://ergast.com/api/f1/{year}/drivers.json?limit=100'  
    results = requests.get(url)
    results = results.json()['MRData']['DriverTable']['Drivers']

    drivers = ''
    for driver in results:
        drivers += f"{driver['givenName']} {driver['familyName']}\n"
    return drivers

def list_results(n, year):
    url = f'http://ergast.com/api/f1/{year}/{n}/results.json'
    results = requests.get(url)
    results = results.json()['MRData']['RaceTable']['Races']
    
    result_table = ''
    i = 1
    for race in results:
        result_table += race['raceName'] + '\n'
        for driver in race['Results']:
            result_table += f"{i}. {driver['Driver']['givenName']} {driver['Driver']['familyName']}\n"
            i += 1
    return result_table

def race_schedule(year):
    url = f'http://ergast.com/api/f1/{year}.json'
    result = requests.get(url)
    race_schedule = result.json()['MRData']['RaceTable']['season'] + '\n'
    
    for race in result.json()['MRData']['RaceTable']['Races']:
        race_schedule += f"{race['round']}. {race['raceName']} - {race['Circuit']['circuitName']} ({race['Circuit']['Location']['country']})\n"\
                         f"{race['date']} {race['time']}\n"
    return race_schedule

def driver_info(name, year):
    url = f'https://ergast.com/api/f1/{year}/1/drivers.json'
    result = requests.get(url)
    
    driver = ''
    for drivers in result.json()['MRData']['DriverTable']['Drivers']:
        first  = drivers['givenName'].lower() 
        second = drivers['familyName'].lower()
        if (first in name.lower()) or (second in name.lower()):
            driver += f"Permanent number: {drivers['permanentNumber']}\n"\
                      f"Driver name: {drivers['givenName']} {drivers['familyName']}\n"\
                      f"Date of birth: {drivers['dateOfBirth']}\n"\
                      f"Nationality: {drivers['nationality']}\n"\
                      f"More about him: {drivers['url']}\n"
    return driver

def list_constructors(year):
    url = f'http://ergast.com/api/f1/{year}/constructors.json'
    result = requests.get(url)
    
    constructor_list = 'Constructor\t---\tCountry\n'
    url2 = f'http://ergast.com/api/f1/{year}/driverstandings.json'
    result2 = requests.get(url2)
    
    for constructor in result.json()['MRData']['ConstructorTable']['Constructors']:
        constructor_list += f"\n\n{constructor['name']}\t---\t{constructor['nationality']}\n"
        for i in result2.json()['MRData']['StandingsTable']['StandingsLists']:
            for j in i['DriverStandings']:
                for k in j['Constructors']:
                    if k['name'] == constructor['name']:
                        constructor_list += f"{j['Driver']['givenName']} {j['Driver']['familyName']}\n"
    return constructor_list

def list_rules(n):
    with open(f"{n}.txt", 'r') as file:
        content = file.read()
    return content

# Bot initialization with explicit bot token
bot = ts.TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(ts.events.NewMessage(pattern='/start'))
async def handleStart(event):
    reply = 'Hi, I am a bot! Ask me something about Formula 1 (2012 - 2019).\n'\
            'Here is a list of my commands:\n'\
            '1. /listdrivers - List of all drivers of a particular year\n'\
            '2. /listresults - Use this command to view the list of races and input the round number to view its results\n'\
            '3. /raceschedule - View time and date of all races\n'\
            '4. /driverinfo - Know about a particular driver\n'\
            '5. /constructors - List of constructors for a given year\n'\
            '6. /listrules - List the rules and regulations\n'\
            'Enter the year you want to know about (Eg - .2013)\n'\
            'Default year is 2019'
    await event.respond(reply)

# Global variables
wait_for_numerical_input = False 
flag_rules = False
driver_details = False
year = 2019
change_year = False

@bot.on(ts.events.NewMessage())
async def handleMessage(event):
    global year 
    global wait_for_numerical_input
    global flag_rules 
    global driver_details
    global change_year 

    if event.message.message[0] == '/':
        command = event.message.message[1:]
        
        if command == 'listdrivers':
            result = list_drivers(year)
            await event.respond(result)

        elif command == 'listresults':
            first = race_schedule(year) + '\nEnter race number to view results:'
            wait_for_numerical_input = True
            await event.respond(first)

        elif command == 'raceschedule':
            result = race_schedule(year)
            await event.respond(result)

        elif command == 'driverinfo':
            driver_details = True
            await event.respond('Please enter the name of the driver.')

        elif command == 'constructors':
            result = list_constructors(year)
            await event.respond(result)

        elif command == 'listrules':
            rules_menu = 'Categories:\n1. Circuits\n2. Race Distance\n3. Lights Out: Race start\n4. Free Practice\n'\
                         '5. Qualifying\n6. Sprint\n7. Grand Prix\n8. Tyres\n9. Pit Lane\n10. Pit Stops\n'\
                         '11. DRS\n12. Car regulations\n13. Points\n14. Flag rules\nPlease choose a category.'
            flag_rules = True
            await event.respond(rules_menu)

        elif command == 'changeyear':
            change_year = True
            await event.respond('Enter the desired year.')

    elif driver_details:
        drivers = list_drivers(year).split()
        for driver in drivers:
            if event.message.message.lower() in driver.lower():
                result = driver_info(event.message.message, year)
                await event.respond(result)

    elif wait_for_numerical_input:
        if 22 - int(event.message.message) > 0:
            result = list_results(event.message.message, year)
            wait_for_numerical_input = False  
            await event.respond(result)
        else:
            wait_for_numerical_input = False
            await event.respond("Invalid option. Start again.")

    elif flag_rules:
        flag_rules = False
        if 15 - int(event.message.message) > 0:
            result = list_rules(event.message.message)
            await event.respond(result)
        else: 
            await event.respond("Invalid option. Start again.")

    elif change_year:
        change_year = False
        new_year = int(event.message.message)
        if 2012 <= new_year <= 2019:
            year = new_year
            await event.respond(f'Changed year to {year}')
        else:
            await event.respond('Invalid year.')

    else:
        await event.respond("Invalid message.")

print('Bot is running...')

# Server to keep Render service alive
def run_server():
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Bot is running.')

    port = int(os.getenv('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Run the server in a separate thread
threading.Thread(target=run_server).start()

# Start the bot and keep it running
bot.run_until_disconnected()