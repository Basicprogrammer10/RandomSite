import sqlite3
from datetime import datetime
import os
import re
############ VARS ############
configFile = 'config.confnose'
DEBUG = True

initialise = {}
toImport  =  {}
########### SETUP ###########
for i in toImport:
    defult = False if toImport[i] != '' else True
    exec(str('from ' if defult == False else 'import ')+str(i)+str(' import ' + toImport[i] if defult == False else ''))
def colored(text, color):
    ColorCodes = {'black':'30','red':'31','yellow':'33','green':'32','blue':'34','cyan':'36','magenta':'35','white':'37','gray':'90','reset':'0'}
    return '\033[' + ColorCodes[str(color).lower()] + 'm' + str(text) + "\033[0m"
for i in initialise:
    exec(i + '=' + initialise[i])
######### FUNCTIONS #########
class config():
    def read(file):
        DebugPrint('Config','Parseing Config File', 'cyan')
        data = open(file, 'r').read().split('\n')
        final = {}
        for i in data:
            working = i.split('=')
            try:
                working[0] = working[0].replace(' ','')
                working[1] = re.search(r'"([A-Za-z0-9_\./\\-]*)"', working[1]).group().replace('"','')
            except:
                pass
            if len(working[0]) >= 3 and working[0][0] != '#':
                final[working[0]] = working[1]
        DebugPrint('Config','Config File Parsed Successfully', 'green')
        config.configFileData = final
        

    def get(Thing):
        return config.configFileData[Thing]

def DebugPrint(Catagory,Text,Color):
    if not DEBUG: return
    print(colored('['+datetime.now().strftime("%H:%M:%S")+'] ','yellow')+colored('['+Catagory+'] ','magenta')+colored(Text,Color))

def cls(): os.system('cls' if os.name=='nt' else 'clear')

def connectDB(db):
    DebugPrint('Database', 'Connecting to ' + colored(db, 'blue'), 'cyan')
    db = sqlite3.connect('sites.db')
    DebugPrint('Database', 'Connection Successfull', 'green')
    DebugPrint('Database', 'Createing Table: ' + colored(config.get('tableName'), 'blue'), 'cyan')
    db.execute("CREATE TABLE IF NOT EXISTS " + config.get('tableName') + " (url TEXT)")
    DebugPrint('Database', 'Table creation Successfull', 'green')
####### MAIN FUNCTION #######
def main():
    DebugPrint('Main', 'Starting...', 'green')
    config.read(configFile)
    connectDB(config.get('database'))
    DebugPrint('Main', 'Finished...', 'red')
if __name__ == "__main__":
    main()