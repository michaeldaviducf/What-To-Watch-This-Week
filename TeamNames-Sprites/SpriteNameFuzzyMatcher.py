import json
import csv
import difflib
import time
import re
from typing import NoReturn

"""
Assumes you run this file from the "What-To-Watch-This-Week" folder

soccer wiki sprites https://www.reddit.com/r/soccerbot/wiki/index
"""

TNSDICT_LOCATE = './TeamNames-Sprites/TeamNames-Sprites-V2.json'
NAME_CORRECTOR_DICT = {
    'USA' : 'United States',
    'Bosnia and Herzegovina' : 'Bosnia-Herzegovina',
    'Macao' : 'Macau',
    'Australia & Oceania' : 'Australasia'
}

def main():
    noList = ['n', 'no', 'none']
    print('Select from options below.')
    functionOptions = {
    '1' : 'Clubs: Cycle through entire dictionary, stopping at empty entries.',
    '2' : 'Clubs: Find entries with duplicate data in each region',
    '3' : 'Competitions: Cycle through entire dictionary, stopping at empty entries',
    '4' : 'International teams: Cycle through the entire Soccerbot dictionary and enter the fs team name'
    }
    numberList = []
    for key in functionOptions.keys():
        print(key, ':', functionOptions[key])
        numberList.append(key)
    while True:
        response = input('Select option: ')
        strch = str(response).lower()
        if (strch in noList):
            return
        elif response in numberList:
            break
        else:
            print('Invalid input. Enter desired option or [n, no, none].')
    if response == '1':
        CompleteMissingFieldsMain()
    elif response == '2':
        FindDuplicateEntriesMain()
    elif response == '3':
        CompleteMissingCompNames()
    elif response == '4':
        IntlTeamNames()
    return

def FindDuplicateEntriesMain():
    with open('./TeamNames-Sprites/soccerbot-TeamNameSprites.json', 'r', encoding='utf8') as rj:
        sBTNSDict = json.load(rj)
    with open(TNSDICT_LOCATE, 'r', encoding='utf8') as rj:
        tNSDict = json.load(rj)
    for region in sBTNSDict:
        if len(sBTNSDict[region]) == 0:
            continue
        tNSRegion = region
        for key, value in NAME_CORRECTOR_DICT.items():
            if value == region:
                tNSRegion = key
        for club in sBTNSDict[region]:
            duplicates = []
            sprite = sBTNSDict[region][club]
            if tNSRegion not in tNSDict.keys():
                continue
            for key, value in tNSDict[tNSRegion].items():
                if sprite == value['Sprite']:
                    duplicates.append(key)
            if len(duplicates) > 1:
                print('\n', tNSRegion)
                print('Duplicates', duplicates)
                input("enter to continue..")
            if len(duplicates) == 0:
                skipList = ['n', 'no', 'none', 's', 'skip', '\n']
                print('\n', tNSRegion)
                response = input(club +  ' not used. Enter FS team name or skip [n, no, none, s, skip]: ')
                if response in skipList:
                    continue
                else:
                    while True:
                        newFSClubName = response
                        if newFSClubName in tNSDict[tNSRegion]:
                            print('That club already exists in the json file')
                            break
                        else:
                            break

                    tNSDict[tNSRegion][newFSClubName] = {}
                    tNSDict[tNSRegion][newFSClubName]['Proper'] = club
                    tNSDict[tNSRegion][newFSClubName]['Sprite'] = sBTNSDict[region][club]
                    with open(TNSDICT_LOCATE, 'w', encoding='utf8') as wf:
                        json.dump(tNSDict, wf, indent=4, sort_keys=True)
    return

def CompleteMissingFieldsMain():
    with open('./TeamNames-Sprites/soccerbot-TeamNameSprites.json', 'r', encoding='utf8') as rj:
        sBTNSDict = json.load(rj)
    with open(TNSDICT_LOCATE, 'r', encoding='utf8') as rj:
        tNSDict = json.load(rj)
    for region in tNSDict:
        if region in NAME_CORRECTOR_DICT.keys():
            sBRegion = NAME_CORRECTOR_DICT[region]
        else:
            sBRegion = region
        if sBRegion not in sBTNSDict.keys():
            for item in tNSDict[region]:
                TNSDictWriter(tNSDict, region, item, None, None)
            continue
        elif len(sBTNSDict[sBRegion]) == 0:
            for item in tNSDict[region]:
                TNSDictWriter(tNSDict, region, item, None, None)
            continue
        else:
            teamNameList = list(sBTNSDict[sBRegion].keys())
        for item in tNSDict[region]:
            if 'Sprite' not in tNSDict[region][item].keys():
                fSTeamName = item
                #tNMatch = OnlyPt9orBetterFuzzyMatcher(fSTeamName, teamNameList)
                tNMatch = FuzzyMatcher(fSTeamName, teamNameList, region)
                if tNMatch != None:
                    sprite = sBTNSDict[sBRegion][tNMatch]
                else:
                    sprite = None
                    #continue
                TNSDictWriter(tNSDict, region, item, tNMatch, sprite)
    return

# To be used with the 2 commented out lines in main function.
# Will iterate through TNS json and fill in all matches above .901 cutoff (if there's only 1 match)
# .901 cutoff is high. Returned matches should be the correct team. 
def OnlyPt9orBetterFuzzyMatcher(teamName, tNList):
    fuzzyMatches = difflib.get_close_matches(teamName, tNList, cutoff=.901, n=2)
    if len(fuzzyMatches) == 1:
        return fuzzyMatches[0]
    return None

def SubstringFuzzyMatcher(teamName, tList, returnSize):
    returnSSFuzzyMatches = {}
    tNSplit = re.split(r"[. \-]+", teamName)
    for clubFromtList in tList:
        clubSplit = re.split(r"[. \-]+", clubFromtList)
        returnSSFuzzyMatches[clubFromtList] = 0
        for word in tNSplit:
            wordMatch = []
            if (len(word) < 3):
                continue
            else:
                wordMatch = difflib.get_close_matches(word, clubSplit, cutoff=.8, n=1)
            for w in wordMatch:
                score = difflib.SequenceMatcher(None, word, w).ratio()
                if score > returnSSFuzzyMatches[clubFromtList]:
                    returnSSFuzzyMatches[clubFromtList] = score
    for i in list(returnSSFuzzyMatches):
        if returnSSFuzzyMatches[i] == 0:
            del returnSSFuzzyMatches[i]
    returnSSFuzzyMatches = dict(sorted(returnSSFuzzyMatches.items(), key=lambda item: item[1], reverse=True))
    return list(returnSSFuzzyMatches.keys())[:returnSize]

def FuzzyMatcher(teamName, tNList, region):
    for cutoff, resultsSize in [[.85, 3], [.6, 5], [.8, 5], [.55, 5]]:
        if (cutoff == .8):
            fuzzyMatches = SubstringFuzzyMatcher(teamName, tNList, resultsSize)
        elif (cutoff == .55):
            print('\n', region, ':', teamName, ':', cutoff)
            print("Enter best approximation of team name or one of [s, skip] to skip.")
            userinput = input("Team name: ")
            if userinput in ['s', 'skip']:
                continue
            fuzzyMatches = difflib.get_close_matches(userinput, tNList, cutoff=cutoff, n=resultsSize)
        else:
            fuzzyMatches = difflib.get_close_matches(teamName, tNList, cutoff=cutoff, n=resultsSize)
        if fuzzyMatches == []:
            continue
        elif (cutoff == .9 and len(fuzzyMatches) == 1):
            print(region, ':', teamName, '- Match:', fuzzyMatches[0])
            return fuzzyMatches[0]
        print('\n', region, ':', teamName, ':', cutoff)
        match = ResultsPrompt(fuzzyMatches, teamName)
        if match == '--skip--':
            break
        elif match != None:
            return match
    print('No matches found. Moving on to next team..')
    return None

def ResultsPrompt(fMatchList, team):
    noList = ['no', 'n', 'none']
    skipList = ['s', 'skip']
    numberList = []
    matchListLen = len(fMatchList)
    for n in range(matchListLen):
        numberList.append(str(n))
        matchingTeam = fMatchList[n]
        score = round(difflib.SequenceMatcher(None, fMatchList[n], team).ratio(), 4)
        print(n, ':', matchingTeam, ':', score)
    while True:
        response = input('Select correct team. Type [n, no, none] if no matches. ')
        strch = str(response).lower()
        if (strch in noList or strch in skipList or response in numberList):
            break
        else:
            print('Invalid input. Enter correct match or [s, skip, n, no, none].')
    if response.lower() in noList:
        return None
    elif response.lower() in skipList:
        return '--skip--'
    else:
        match = fMatchList[int(response)]
        return match

def TNSDictWriter(dictIn, region, club, properName, sprite):
    dictIn[region][club]['Proper'] = properName
    dictIn[region][club]['Sprite'] = sprite

    with open(TNSDICT_LOCATE, 'w', encoding='utf8') as wf:
        json.dump(dictIn, wf, indent=4, sort_keys=True)
    return

def CompleteMissingCompNames():
    with open('./TeamNames-Sprites/soccerbot-CompetitionSprites.json', 'r', encoding='utf8') as rf:
        sBCSDict = json.load(rf)
    with open('./TeamNames-Sprites/CompNames-Sprites.json', 'r', encoding='utf8') as rf:
       cNSDict = json.load(rf)
    for region in cNSDict:
        regionSB = region
        if regionSB in list(NAME_CORRECTOR_DICT.keys()):
            regionSB = NAME_CORRECTOR_DICT[region]
        if regionSB not in list(sBCSDict.keys()):
            for competition in cNSDict[region]:
                cNSDict[region][competition]['Proper'] = None
                cNSDict[region][competition]['Sprite'] = None
            continue
        if len(sBCSDict[regionSB]) == 0:
            for competition in cNSDict[region]:
                cNSDict[region][competition]['Proper'] = None
                cNSDict[region][competition]['Sprite'] = None
                with open('./TeamNames-Sprites/CompNames-Sprites.json', 'w', encoding='utf8') as wf:
                    json.dump(cNSDict, wf, indent=4, sort_keys=True)

            continue
        for competition in cNSDict[region]:
            if 'Sprite' not in cNSDict[region][competition].keys():
                compNameProper, compSprite = CompResultsPrompt(competition, region, sBCSDict[regionSB])
                if compNameProper == None:
                    cNSDict[region][competition]['Proper'] = None
                    cNSDict[region][competition]['Sprite'] = None
                else:
                    cNSDict[region][competition]['Proper'] = compNameProper
                    cNSDict[region][competition]['Sprite'] = compSprite
                with open('./TeamNames-Sprites/CompNames-Sprites.json', 'w', encoding='utf8') as wf:
                    json.dump(cNSDict, wf, indent=4, sort_keys=True)


def CompResultsPrompt(compName, region, compSpriteDict):
    compNameList = list(compSpriteDict.keys())
    noList = ['n', 'no', 'none', 's']
    print('\n', region, ' : ', compName)
    numberList = []
    for n in range(len(compNameList)):
        numberList.append(str(n))
        print(n, ' : ', compNameList[n])
    while True:
        print('select matching competition name or [n, no, none] if no matches')
        response = input('Make selection: ')
        if (response in noList):
            return None, None
        elif (response in numberList):
            print(compNameList[int(response)], compSpriteDict[compNameList[int(response)]])
            return compNameList[int(response)], compSpriteDict[compNameList[int(response)]]
        else:
            print('Invalid input. Enter matching number or [n, no, none].')
    
def IntlTeamNames():
    with open(TNSDICT_LOCATE, 'r', encoding='utf8') as rf:
        tNSDict = json.load(rf)
    with open('./TeamNames-Sprites/soccerbot-TeamNameSprites.json', 'r', encoding='utf8') as rf:
        sBTNSDict = json.load(rf)
    for region, intlTeams in sBTNSDict['National Teams'].items():
        region = 'Australia & Oceania' if region == 'Australasia' else region
        if region not in tNSDict.keys():
            tNSDict[region] = {}
        for intlTeam, sprite in intlTeams.items():
            alreadyThere = 0
            for tDict in tNSDict[region].values():
                if intlTeam == tDict['Proper']:
                    alreadyThere = 1
                    break
            if alreadyThere == 1:
                continue
            print(intlTeam, ':', sprite)
            response = input("Is the team name the same in FS? [y or n] ")
            if response == "y":
                tNSDict[region][intlTeam] = {}
                tNSDict[region][intlTeam]['Proper'] = intlTeam
                tNSDict[region][intlTeam]['Sprite'] = sprite
            else:
                fSTeamName = input("Enter FS team name: ")
                tNSDict[region][fSTeamName] = {}
                tNSDict[region][fSTeamName]['Proper'] = intlTeam
                tNSDict[region][fSTeamName]['Sprite'] = sprite
            with open(TNSDICT_LOCATE, 'w', encoding='utf8') as wf:
                json.dump(tNSDict, wf, indent=4, sort_keys=True)
    return
    

main()