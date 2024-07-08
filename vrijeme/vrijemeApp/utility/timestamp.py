from datetime import datetime

def vratiSateIMiute(timestamp):
    datum = datetime.fromtimestamp(timestamp)
    datum_vrijeme = datum.strftime("%H : %M")
    return datum_vrijeme

def vratiDatum(timestamp):
    datumObj = datetime.fromtimestamp(timestamp)
    datum = datumObj.strftime("%d - %m - %y")
    return datum

