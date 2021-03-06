# What-To-Watch-This-Week

 https://www.reddit.com/r/WhatToWatchThisWeek/

## Changelog

### v2

- Added Round
- Added Leg
- Added Aggregate

### v3

- Created two spreadsheets, one for input - to fill in the data - and another for output - to make the necessary process.

### v4

- Removed the aggregate column to become: Team A (2) vs (3) Team B

### v5

- Added Sprites

#### v5.1

- Added Sprites with official (standart) names to promote coherency and avoid spelling mistakes

### v6

- Added italic instead of just bold
- Added a circle (button) to clear only a few cells instead of all cells

### v7

- Removed italic
- Tried to change to excel (dropdown list search was bad even with add-in)
- Created a new spreadsheet to have all days of the week and tidy the sheets / formula to improve workflow								

### v8

- Use App Scripts to integrate all days and give a single text to copy

### v9

- Use Selenium to automate the fetching of the data (Still needs manual correcting because of differing linguistic terms e.g. Bayern Munich != Bayern Munch)
- Use vlookup to help with CL and EL groups

### v10

- Used BeautifulSoup to create a json file of links to each competition for use in WTWTW.py. File located in FSJSON folder.
- imported requests and json->load
- created new function WTWTW to run entire script
- parser now returns data instead of writes to csv. Parser also retrieves date and region for later use. Returns date and checked matches for that day.
- Created WTWTWmatches and competitions_dict dictionaries. WTWTWmatches is used to store checked match data. competitions_dict tracks each region/competition from checked matches for later use.
- WTWTW fetches checked matches and uses competitions_dict to retrieve the round and aggregate for each match in that competition in WTWTWmatches using competition_matches and acha_round functions and add to WTWTWmatches. Also returns correct competition name (sometimes includes string such as " - Losers Stage". That gets removed.) acha_round parses through list for the match and returns round and aggregate. WTWTW function writes data to csv at end. Uses requests and BeautifulSoup
- This version completes the two checked boxes in Backlog. Not tested for competitions with group stages yet.

### v11

- Rearranged functions in file to make it easier to read. 
- Updated webdriver initator arguments
- Removed sleep after webdriver initiates and replaced with keyboard input. Allows user to to select different starting day.
- Created "days" variable in fetcher to use throughout function instead of hardcoded integers.
- Added logic to filter round info. Only returns results for cups (Round of 16, Quarter-finals, etc). Same few lines also translates web site's round names to the more commonly referred names using a hard-coded dictionary. Not yet tested for competitions with group stages.
- Separated some logic from WTWTW function into it's own function to clean up the code.
- Used sorted to print each day's matches ordered by time in csv
- WTWTW() function now returns the dictionary of the checked matches. For use in future functions or scripts.
- Added encoding argument in listas writer to work with less common letters such as ç
- TeamNames-Sprites folder added. Dictionary for automatic team name correction. Added function automating team name correction and to fetch team sprites and addes to WTWTW's returned dictionary for later use. Should complete backlog items to add more flairs and creating automatic name correction.
- Added function to fetch aggregate scores
- Created WTWTW_Post.py to write reddit post. Asks user for which matches to bold. It imports and calls on WTWTW.py functions.
- Added CompNames-Sprites.json into TeamNames-Sprites folder. Incorporated into WTWTW.
- Added international teams to TeamNames-Sprites-V2.json

## Backlog

- [ ] Install Grid (needs Docker) to use python in spreadsheets easily
- [x] (Hard) Automate round and group letter of the competition (e.g. "Semi-Final"; "Group B") as stated in v9. (Not tested for Group Stage)
- [x] Maybe ditch the spreadsheets (probably hard because of bold matches)
- [x] Add more flairs (maybe use https://www.reddit.com/r/soccer/comments/f8z3sc/what_to_watch_this_week_241_march/fioh87b/). https://www.reddit.com/r/soccerbot/wiki/index has a good collection of flairs. Used to create TeamNames-Sprites json.
- [ ] Add code to allow script to continue if competition doesn't exist in fslinks.json. Competition can change name or be created. Maybe prompt user for Competition name and link for competition.
- [ ] GUI for a more visual process. https://wiki.python.org/moin/GuiProgramming

## Technology Stack

- Github
- Python
- Requests
- Selenium

## Contribute

Feel free to contribute