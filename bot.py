import telethon.sync as ts 
from telethon.sessions import StringSession
import requests
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler




api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
bot_token = os.getenv("bot_token")

#functions for specific commands
def list_drivers(year):
    url = 'http://ergast.com/api/f1/{}/drivers.json?limit=100'.format(year)  
    results = requests.get(url)
    results = results.json()['MRData']['DriverTable']['Drivers']

    drivers = ''

    for driver in results:
        print(driver)
        drivers += driver['givenName'] + ' ' + driver['familyName'] + '\n'

    return drivers


def list_results(n, year):
    base_url = 'http://ergast.com/api/f1/{}'.format(year)
    race = n
    end = 'results.json'
    url = f"{base_url}/{race}/{end}"
    results = requests.get(url)
    results = results.json()['MRData']['RaceTable']['Races']
    result_table = ''
    i = 1
    for race in results:
        print (race['raceName'])
        result_table += race['raceName'] + '\n'
        for driver in race['Results']:
            print(driver['Driver']['givenName'] + ' ' + driver['Driver']['familyName'] )
            result_table += str(i) + ' ' + driver['Driver']['givenName'] + ' ' + driver['Driver']['familyName']+ '\n'
            i+=1
    flag = True
    return result_table


def race_schedule(year):
    url = 'http://ergast.com/api/f1/{}.json'.format (year)
    result = requests.get(url)
    race_schedule = result.json()['MRData']['RaceTable']['season'] + '\n'
    for race in result.json()['MRData']['RaceTable']['Races']:
        print (race['round'],race['raceName'], race['Circuit']['circuitName'], race['Circuit']['Location']['country'])
        race_schedule += race['round'] + '.' + '\t' + race['raceName'] + '\t' + race['Circuit']['circuitName'] +'\t'+ race['Circuit']['Location']['country'] + '\n'+'\t'+ race['date']+ '\t'  \
            + race['time']+'\n'
    return race_schedule


def driver_info(name, year):
    url = 'https://ergast.com/api/f1/{}/1/drivers.json'.format(year)
    result = requests.get(url)
    driver = ''
    for drivers in result.json()['MRData']['DriverTable']['Drivers']:
        first  = drivers['givenName'].lower() 
        second = drivers['familyName'].lower()
        if (first in name.lower()) or (second in name.lower()):
            driver += 'Permanent number' +' : '+ drivers['permanentNumber'] + '\n' + 'Driver name'+ ' : ' + drivers['givenName']+' '+drivers['familyName']\
            +'\n' + 'Date of birth' +' : '+ drivers['dateOfBirth'] + '\n' + 'Nationality' + ' : ' + drivers['nationality'] + '\n' + 'More about him : ' + drivers['url'] + '\n' 
    return driver


def list_constructors(year):
    url = 'http://ergast.com/api/f1/{}/constructors.json'.format(year)
    result = requests.get(url)
    constructor_list = 'Constructor' + '\t' + '---' + 'Country' + '\n'
    url2 = 'http://ergast.com/api/f1/{}/driverstandings.json'.format(year)
    result2 = requests.get(url2)
    
    for constructor in result.json()['MRData']['ConstructorTable']['Constructors']:
        print (constructor['name'], constructor['nationality'], sep = '\t',)
        constructor_list += '\n' + '\n'+ constructor['name'] + '\t' + '---' + constructor['nationality'] + '\n' 
        for i in result2.json()['MRData']['StandingsTable']['StandingsLists']:
            for j in i['DriverStandings']:
                for k in j['Constructors']:
                    if k['name']==constructor['name']:
                        print(j['Driver']['familyName'])
                        constructor_list += j['Driver']['givenName'] + ' ' + j['Driver']['familyName'] + '\n' 
    return constructor_list


def list_rules(n):
    with open (f"{n}.txt", 'r') as file:
        content = file.read()
    
    print ('Done')
    return content 



# We have to manually call "start" if we want an explicit bot token
bot = ts.TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(ts.events.NewMessage(pattern='/start'))
async def handleStart(event):
    reply = 'Hi, I am a bot! Ask me something about Formula 1 (2012 - 2019). Explore the menu to learn more about what tasks I can do!'
    reply += '\n' + 'Here is a list of my commands :\n' + '1. /listdrivers - List of all drivers of a particular year\n'+\
    '2. /listresults - Use this command to view the list of races and then input the round number to view its results \n' + '3. /raceschedule - To'\
    'view time and date of all races\n' + '4. /driverinfo - Use this command to know about a particular driver\n' + \
    '5. /constructors - Lists out all the constructors that participated in a given year\n' + \
    '6. /listrules - List the rules and regulations \n\n' + 'Enter the year you want to know about (Eg - .2013)\n' +\
    'Default year is 2019' 
    await event.respond(reply)


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

    #if event.message.message[0] == '.':
        #year = event.message.message[1:5]

    if event.message.message[0] == '/':
        command = event.message.message[1:]
        
        if command == 'listdrivers':
            result = list_drivers(year)
            await event.respond (result)

        elif command == 'listresults':
            first = race_schedule(year) + '\n' + 'Enter race number to view results of '
            wait_for_numerical_input = True
            await event.respond(first)
            
        elif command == 'raceschedule':
            result = race_schedule(year)
            await event.respond(result)
            
        elif command == 'driverinfo':
            driver_details = True
            await event.respond('Please enter the name of driver.')
            
        elif command == 'constructors':
            result = list_constructors(year)
            await event.respond(result)

        elif command == 'listrules':
            rules_menu = 'Categories:\n' + '1. Circuits\n' + '2. Race Distance\n' + '3. Lights Out: Race start\n' + '4. Free Practice\n' \
            '5. Qualifying\n' + '6. Sprint\n' + '7. Grand Prix\n' + '8. Tyres\n' + '9. Pit Lane\n' + '10. Pit Stops\n'\
            '11. DRS\n' + '12. Car regulations\n' + '13. Points\n' + '14. Flag rules\n' + 'Please choose a category'
            flag_rules = True
            print ('rules input ')
            await event.respond(rules_menu)

        elif command == 'changeyear':
            change_year = True
            await event.respond('Enter desired year')

    elif (driver_details == True):
        drivers = list_drivers(year).split()
        for driver in drivers:
            if (event.message.message.lower() in driver.lower()):
                result = driver_info(event.message.message, year)
                await event.respond (result)
    

    elif ( wait_for_numerical_input == True) :
        if (22 - int (event.message.message)>0):
            result = list_results(event.message.message, year)
            wait_for_numerical_input = False  
            await event.respond (result)

        else:
            wait_for_numerical_input = False
            await event.respond ("Invalid option. Start again")


    elif (flag_rules == True):
        flag_rules = False
        if (15 - int (event.message.message) > 0 ):
            result = list_rules( (event.message.message))
            await event.respond (result)
            print('Rules')
        else: 
            await event.respond ("Invalid option. Start again") 
            print('Not rules')


    elif (change_year == True):
        change_year = False
        new_year = int (event.message.message)
        if (new_year >= 2012 and new_year<=2019):
            year = new_year
            await event.respond ('Changed year to {}'.format(year))
        else:
            await event.respond ('Invalid year')


    else:
        await event.respond("Invalid message.")

print('Bot is running...')

#def run_server():
#    class SimpleHandler(BaseHTTPRequestHandler):
#        def do_GET(self):
#            self.send_response(200)
#            self.end_headers()
#            self.wfile.write(b'Bot is running.')
#
#    port = int(os.getenv('PORT', 8000))
#    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
#    server.serve_forever()
#
#threading.Thread(target=run_server).start()
bot.run_until_disconnected()
