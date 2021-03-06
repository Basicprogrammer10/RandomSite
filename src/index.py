import sqlite3, requests,  os, re
from datetime import datetime

from requests.models import Response
############ VARS ############
configFile = 'config.confnose'
DEBUG = True

######### FUNCTIONS #########
def colored(text, color):
    ColorCodes = {'black':'30','red':'31','yellow':'33','green':'32','blue':'34','cyan':'36','magenta':'35','white':'37','gray':'90','reset':'0'}
    return '\033[' + ColorCodes[str(color).lower()] + 'm' + str(text) + "\033[0m"

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

def connectDB(database):
    DebugPrint('Database', 'Connecting to ' + colored(database, 'blue'), 'cyan')
    db = sqlite3.connect(database)
    DebugPrint('Database', 'Connection Successfull', 'green')

    table = db.cursor()
    table.execute('SELECT count(name) FROM sqlite_master WHERE type=\'table\' AND name=\'' + config.get('tableName') + '\'')

    if table.fetchone()[0] != 1:
        DebugPrint('Database', 'Createing Table: ' + colored(config.get('tableName'), 'blue'), 'cyan')
        db.execute("CREATE TABLE IF NOT EXISTS " + config.get('tableName') + " (url TEXT, done INT)")
        db.execute("INSERT INTO " + config.get('tableName') + " (url, done) values (" + config.get('seedUri') + ",0)")
        DebugPrint('Database', 'Table creation Successfull', 'green')

    return db

def getDbData(db):
    cursor = db.execute("SELECT * FROM " + config.get('tableName'))
    rows = cursor.fetchall()
    return rows

def requestSite(url):
    DebugPrint('Request', 'Fetching ' + colored(url, 'blue'), 'cyan')
    responce = requests.get(url)
    if not responce.status_code == 200:
        DebugPrint('Request', 'Error ' + colored(str(responce.status_code)), 'red')
        return None
    DebugPrint('Request', 'Sucess ' + colored('[' + str(int(responce.elapsed.total_seconds() * 1000)) + ' ms]', 'blue'), 'green')
    return responce.content

def goThroughDatabase(sites):
    for i in sites:
        if i[1] == 1: return
        requestSite(i[0])

####### MAIN FUNCTION #######
def main():
    DebugPrint('Main', 'Starting...', 'green')
    config.read(configFile)
    db = connectDB(config.get('database'))

    db.execute("INSERT INTO " + config.get('tableName') + " (url, done) values (" + config.get('seedUri') + ",0)")

    for i in range(int(config.get('seedItarations'))):
        goThroughDatabase(getDbData(db))
    DebugPrint('Main', 'Finished...', 'red')
if __name__ == "__main__":
    main()