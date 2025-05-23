import csv
from PyQt6.QtGui import QColor
from zeldaEnums import OcarinaHighScore, OcarinaControlCode, OcarinaMsgColor

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

def findInDictByName(dictionary, sfxName):
    for key, value in dictionary.items():
        if isinstance(value, tuple) and value[0] == sfxName:
            return key
    return None

highScorePreviewPresets = {

    OcarinaHighScore.ARCHERY:'9999',
    OcarinaHighScore.POE_POINTS:'9999',
    OcarinaHighScore.FISHING:'99',
    OcarinaHighScore.HORSE_RACE:'00\"00\"',
    OcarinaHighScore.MARATHON:'00\"00\"',
    OcarinaHighScore.HS_UNK:'',
    OcarinaHighScore.DAMPE_RACE:'00\"00\"',
}

controlCharPreviewPresets = {
    OcarinaControlCode.PLAYER:'LinkName',
    OcarinaControlCode.POINTS:'9999',
    OcarinaControlCode.FISH_WEIGHT:'99',
    OcarinaControlCode.GOLD_SKULLTULAS:'100',
    OcarinaControlCode.MARATHON_TIME:'00"00"',
    OcarinaControlCode.RACE_TIME:'00"00"',
    OcarinaControlCode.TIME:'00"00"',
}

ocarinaTextColors = {
    OcarinaMsgColor.W:QColor(255, 255, 255, 255),
    OcarinaMsgColor.R:QColor(255, 60, 60, 255),
    OcarinaMsgColor.G:QColor(70, 255, 80, 255),
    OcarinaMsgColor.B:QColor(80, 110, 255, 255),
    OcarinaMsgColor.C:QColor(90, 180, 255, 255),
    OcarinaMsgColor.M:QColor(210, 100, 255, 255),
    OcarinaMsgColor.Y:QColor(255, 255, 30, 255),
    OcarinaMsgColor.BLK:QColor(0, 0, 0, 255),
}

ocarinaWoodTextColors = {
    OcarinaMsgColor.W:QColor(0, 0, 0, 255),
    OcarinaMsgColor.R:QColor(255, 120, 0, 255),
    OcarinaMsgColor.G:QColor(70, 255, 80, 255),
    OcarinaMsgColor.B:QColor(80, 90, 255, 255),
    OcarinaMsgColor.C:QColor(100, 180, 255, 255),
    OcarinaMsgColor.M:QColor(255, 150, 180),
    OcarinaMsgColor.Y:QColor(255, 255, 50, 255),
    OcarinaMsgColor.BLK:QColor(0, 0, 0, 255),
}

FONT_WIDTHS = [
    8.0,    # (space)
    8.0,    # !
    6.0,    # "
    9.0,    # #
    9.0,    # $
    14.0,   # %
    12.0,   # &
    3.0,    # '
    7.0,    # (
    7.0,    # )
    7.0,    # *
    9.0,    # +
    4.0,    # ,
    6.0,    # -
    4.0,    # .
    9.0,    # /
    10.0,   # 0
    5.0,    # 1
    9.0,    # 2
    9.0,    # 3
    10.0,   # 4
    9.0,    # 5
    9.0,    # 6
    9.0,    # 7
    9.0,    # 8
    9.0,    # 9
    6.0,    # :
    6.0,    # ;
    9.0,    # <
    11.0,   # =
    9.0,    # >
    11.0,   # ?
    13.0,   # @
    12.0,   # A
    9.0,    # B
    11.0,   # C
    11.0,   # D
    8.0,    # E
    8.0,    # F
    12.0,   # G
    10.0,   # H
    4.0,    # I
    8.0,    # J
    10.0,   # K
    8.0,    # L
    13.0,   # M
    11.0,   # N
    13.0,   # O
    9.0,    # P
    13.0,   # Q
    10.0,   # R
    10.0,   # S
    9.0,    # T
    10.0,   # U
    11.0,   # V
    15.0,   # W
    11.0,   # X
    10.0,   # Y
    10.0,   # Z
    7.0,    # [
    10.0,   # ¥
    7.0,    # ]
    10.0,   # ^
    9.0,    # _
    5.0,    # `
    8.0,    # a
    9.0,    # b
    8.0,    # c
    9.0,    # d
    9.0,    # e
    6.0,    # f
    9.0,    # g
    8.0,    # h
    4.0,    # i
    6.0,    # j
    8.0,    # k
    4.0,    # l
    12.0,   # m
    9.0,    # n
    9.0,    # o
    9.0,    # p
    9.0,    # q
    7.0,    # r
    8.0,    # s
    7.0,    # t
    8.0,    # u
    9.0,    # v
    12.0,   # w
    8.0,    # x
    9.0,    # y
    8.0,    # z
    7.0,    # {
    5.0,    # |
    7.0,    # }
    10.0,   # ~
    10.0,   # ‾
    12.0,   # À
    6.0,    # î
    12.0,   # Â
    12.0,   # Ä
    11.0,   # Ç
    8.0,    # È
    8.0,    # É
    8.0,    # Ê
    6.0,    # Ë
    6.0,    # Ï
    13.0,   # Ô
    13.0,   # Ö
    10.0,   # Ù
    10.0,   # Û
    10.0,   # Ü
    9.0,    # ß
    8.0,    # à
    8.0,    # á
    8.0,    # â
    8.0,    # ä
    8.0,    # ç
    9.0,    # è
    9.0,    # é
    9.0,    # ê
    9.0,    # ë
    6.0,    # ï
    9.0,    # ô
    9.0,    # ö
    9.0,    # ù
    9.0,    # û
    9.0,    # ü
    14.0,   # [A]
    14.0,   # [B]
    14.0,   # [C]
    14.0,   # [L]
    14.0,   # [R]
    14.0,   # [Z]
    14.0,   # [C-Up]
    14.0,   # [C-Down]
    14.0,   # [C-Left]
    14.0,   # [C-Right]
    14.0,   # ▼
    14.0,   # [Analog-Stick]
    14.0,   # [D-Pad]
    14.0,   # ?
    14.0,   # ?
    14.0,   # ?
    14.0,   # ?
]
