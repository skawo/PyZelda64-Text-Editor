import csv

sfxOcarina = {}
sfxMajora = {}

try:
    with open('res/SFX_Ocarina.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) >= 3:
                sfxOcarina[int(row[0])] = (row[1], row[2])
            elif len(row) == 2:
                sfxOcarina[int(row[0])] = (row[1], '')
            else:
                pass
except Exception:
    pass

try:
    with open('res/SFX_Majora.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) >= 3:
                sfxMajora[int(row[0])] = (row[1], row[2])
            elif len(row) == 2:
                sfxMajora[int(row[0])] = (row[1], '')
            else:
                pass
except Exception:
    pass

def findSFXByname(dictionary, sfxName):
    for key, value in dictionary.items():
        if isinstance(value, tuple) and value[0] == sfxName:
            return key
    return None