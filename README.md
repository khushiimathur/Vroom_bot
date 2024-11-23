# VROOM bot
**Description**
The Formula 1 Telegram Bot is a Python-based Telegram bot designed to provide information about Formula 1 races, drivers, constructors, schedules, and regulations. It uses the [Ergast Developer API](https://ergast.com/mrd/) to fetch real-time Formula 1 data and responds to user queries based on pre-defined commands.

**Features**
1. Driver Information: Get details about drivers from a specific season.
2. Race Results: View the results of specific races.
3. Race Schedules: Check the time and date of races for a given year.
4. Constructors List: List all constructors and their associated drivers.
5. F1 Rules: Learn about various categories of Formula 1 rules and regulations.
6. Dynamic Year Selection: Change the year for fetching race data (2012–2019 by default).
7. Interactive Commands: Provides an interactive experience by responding to user inputs.

Here is the list of commands supported by the bot:
- /start:	Displays the welcome message and list of available commands.
- /listdrivers:	Lists all the drivers for a specific year.
- /listresults:	Lists races for a specific year and prompts the user to select a race to view its results.
- /raceschedule:	Displays the race schedule for a specific year.
- /driverinfo:	Prompts the user to enter a driver name and provides detailed information about the driver.
- /constructors:	Lists all constructors for a specific year and their associated drivers.
- /listrules:	Displays a menu of Formula 1 rule categories and fetches details from corresponding files.
- /changeyear:	Prompts the user to change the year (valid years: 2012–2019).
