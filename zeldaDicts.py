import csv
from PyQt6.QtGui import QColor
from zeldaEnums import *

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

ocarinaHighScorePreviewPresets = {
    OcarinaHighScore.ARCHERY:'9999',
    OcarinaHighScore.POE_POINTS:'9999',
    OcarinaHighScore.FISHING:'99',
    OcarinaHighScore.HORSE_RACE:'00\"00\"',
    OcarinaHighScore.MARATHON:'00\"00\"',
    OcarinaHighScore.HS_UNK:'',
    OcarinaHighScore.DAMPE_RACE:'00\"00\"',
}

ocarinaControlCharPreviewPresets = {
    OcarinaControlCode.PLAYER:'LinkName',
    OcarinaControlCode.POINTS:'9999',
    OcarinaControlCode.FISH_WEIGHT:'99',
    OcarinaControlCode.GOLD_SKULLTULAS:'100',
    OcarinaControlCode.MARATHON_TIME:'00"00"',
    OcarinaControlCode.RACE_TIME:'00"00"',
    OcarinaControlCode.TIME:'00"00"',
}

ocarinaTextColors = {
    OcarinaMsgColor.D:QColor(255, 255, 255, 255),
    OcarinaMsgColor.R:QColor(255, 60, 60, 255),
    OcarinaMsgColor.G:QColor(70, 255, 80, 255),
    OcarinaMsgColor.B:QColor(80, 110, 255, 255),
    OcarinaMsgColor.C:QColor(90, 180, 255, 255),
    OcarinaMsgColor.M:QColor(210, 100, 255, 255),
    OcarinaMsgColor.Y:QColor(255, 255, 30, 255),
    OcarinaMsgColor.BLK:QColor(0, 0, 0, 255),
}

ocarinaWoodTextColors = {
    OcarinaMsgColor.D:QColor(0, 0, 0, 255),
    OcarinaMsgColor.R:QColor(255, 120, 0, 255),
    OcarinaMsgColor.G:QColor(70, 255, 80, 255),
    OcarinaMsgColor.B:QColor(80, 90, 255, 255),
    OcarinaMsgColor.C:QColor(100, 180, 255, 255),
    OcarinaMsgColor.M:QColor(255, 150, 180),
    OcarinaMsgColor.Y:QColor(255, 255, 50, 255),
    OcarinaMsgColor.BLK:QColor(0, 0, 0, 255),
}

OCARINA_FONT_WIDTHS = [
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

majoraControlCharPreviewPresets = {
    MajoraControlCode.PLAYER: 'LinkName',
    MajoraControlCode.SWAMP_CRUISE_HITS: '20',
    MajoraControlCode.STRAY_FAIRY_SCORE: '20th',
    MajoraControlCode.GOLD_SKULLTULAS: '20th',
    MajoraControlCode.POSTMAN_RESULTS: '00"00',
    MajoraControlCode.MOON_CRASH_TIME: '00"00',
    MajoraControlCode.DEKU_RESULTS: '00"00',
    MajoraControlCode.TIMER: '00"00',
    MajoraControlCode.TIMER2: '00"00',
    MajoraControlCode.TIMER3: '00"00',
    MajoraControlCode.TIMER4: '00"00',
    MajoraControlCode.SHOOTING_GALLERY_RESULT: '9999',
    MajoraControlCode.BANK_PROMPT: '0 0 0  Rupee(s)',
    MajoraControlCode.RUPEES_ENTERED: '500 Rupees',
    MajoraControlCode.RUPEES_IN_BANK: '5000 Rupees',
    MajoraControlCode.MOON_CRASH_TIME_REMAINS: '72:00',
    MajoraControlCode.BET_RUPEES_PROMPT: '0 0  Rupees',
    MajoraControlCode.BOMBER_CODE_PROMPT: '0 0 0 0 0',
    MajoraControlCode.SOARING_DESTINATION: 'Great Bay Coast',
    MajoraControlCode.UNK_D3: '----',
    MajoraControlCode.LOTTERY_NUMBER_PROMPT: '1 1 1',
    MajoraControlCode.OCEANSIDE_HOUSE_ORDER: '123456',
    MajoraControlCode.WOODFALL_FAIRIES_REMAIN: '15',
    MajoraControlCode.SNOWHEAD_FAIRIES_REMAIN: '15',
    MajoraControlCode.BAY_FAIRIES_REMAIN: '15',
    MajoraControlCode.IKANA_FAIRIES_REMAIN: '15',
    MajoraControlCode.SWAMP_CRUISE_RESULT: '45',
    MajoraControlCode.WINNING_LOTTERY_NUM: '000',
    MajoraControlCode.PLAYER_LOTTERY_NUM: '000',
    MajoraControlCode.ITEM_VALUE: '500 Rupees',
    MajoraControlCode.BOMBER_CODE: '12345',
    MajoraControlCode.OCEANSIDE_HOUSE_ORDER_1: 'YELLOW',
    MajoraControlCode.OCEANSIDE_HOUSE_ORDER_2: 'YELLOW',
    MajoraControlCode.OCEANSIDE_HOUSE_ORDER_3: 'YELLOW',
    MajoraControlCode.OCEANSIDE_HOUSE_ORDER_4: 'YELLOW',
    MajoraControlCode.OCEANSIDE_HOUSE_ORDER_5: 'YELLOW',
    MajoraControlCode.OCEANSIDE_HOUSE_ORDER_6: 'YELLOW',
    MajoraControlCode.MOON_CRASH_HOURS_REMAIN: '72 hours',
    MajoraControlCode.UNTIL_MORNING: '23:59',
    MajoraControlCode.TOTAL_IN_BANK: '5000',
    MajoraControlCode.TOWN_SHOOTING_HIGHSCORE: '50',
    MajoraControlCode.EPONA_ARCHERY_HIGHSCORE: '99\'99"99',
    MajoraControlCode.DEKU_HIGHSCORE_DAY1: '99\'99"99',
    MajoraControlCode.DEKU_HIGHSCORE_DAY2: '99\'99"99',
    MajoraControlCode.DEKU_HIGHSCORE_DAY3: '99\'99"99',
    MajoraControlCode.UNK_F4: ':0"00\'',
    MajoraControlCode.UNK_F3: '0"10\'',
    MajoraControlCode.UNK_F2: '0',
    MajoraControlCode.UNK_F1: '0',
    MajoraControlCode.FISH_WEIGHT: '00'
}

majoraTextColors = {
    MajoraControlCode.COLOR_DEFAULT: [QColor(255, 255, 255), QColor(255, 255, 255), QColor(0, 0, 0), QColor(0, 0, 0)],
    MajoraControlCode.COLOR_RED: [QColor(255, 60, 60), QColor(255, 120, 0), QColor(255, 60, 60), QColor(255, 60, 60)],
    MajoraControlCode.COLOR_GREEN: [QColor(70, 255, 80), QColor(70, 255, 80), QColor(70, 255, 80), QColor(124, 179, 255)],
    MajoraControlCode.COLOR_BLUE: [QColor(80, 110, 255), QColor(80, 90, 255), QColor(80, 110, 255), QColor(80, 110, 255)],
    MajoraControlCode.COLOR_YELLOW: [QColor(255, 255, 30), QColor(255, 255, 50), QColor(255, 255, 30), QColor(255, 255, 30)],
    MajoraControlCode.COLOR_NAVY: [QColor(74, 138, 234), QColor(74, 138, 234), QColor(74, 138, 234), QColor(74, 138, 234)],
    MajoraControlCode.COLOR_PINK: [QColor(255, 192, 203), QColor(255, 192, 203), QColor(255, 192, 203), QColor(255, 192, 203)],
    MajoraControlCode.COLOR_SILVER: [QColor(192, 192, 192), QColor(192, 192, 192), QColor(192, 192, 192), QColor(192, 192, 192)],
    MajoraControlCode.COLOR_ORANGE: [QColor(255, 165, 0), QColor(255, 165, 0), QColor(255, 165, 0), QColor(255, 165, 0)]
}

boxTextColorIndexes = {
    MajoraTextboxType.Black: 0,
    MajoraTextboxType.Wooden: 1,
    MajoraTextboxType.Blue: 0,
    MajoraTextboxType.Ocarina: 0,
    MajoraTextboxType.None_White: 0,
    MajoraTextboxType.None_Black: 2,
    MajoraTextboxType.Black2: 0,
    MajoraTextboxType.No_Box: 0,
    MajoraTextboxType.Blue2: 0,
    MajoraTextboxType.Red: 0,
    MajoraTextboxType.None2: 0,
    MajoraTextboxType.Credits: 0,
    MajoraTextboxType.None3: 0,
    MajoraTextboxType.Bombers_Notebook: 2,
    MajoraTextboxType.None4: 0,
    MajoraTextboxType.Red2: 0
}

majoraSpecificTagTextColor = {
    MajoraControlCode.A_BUTTON: [QColor(0x41, 0x69, 0xE1), QColor(0x41, 0x69, 0xE1), QColor(0x41, 0x69, 0xE1), QColor(0x41, 0x69, 0xE1)],
    MajoraControlCode.B_BUTTON: [QColor(0x32, 0xCD, 0x32), QColor(0x32, 0xCD, 0x32), QColor(0x32, 0xCD, 0x32), QColor(0x32, 0xCD, 0x32)],
    MajoraControlCode.C_BUTTON: [QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00)],
    MajoraControlCode.R_BUTTON: [QColor(0xFF, 0xFF, 0xFF), QColor(0xFF, 0xFF, 0xFF), QColor(0x00, 0x00, 0x00), QColor(0x00, 0x00, 0x00)],
    MajoraControlCode.L_BUTTON: [QColor(0xFF, 0xFF, 0xFF), QColor(0xFF, 0xFF, 0xFF), QColor(0x00, 0x00, 0x00), QColor(0x00, 0x00, 0x00)],
    MajoraControlCode.Z_BUTTON: [QColor(0xFF, 0xFF, 0xFF), QColor(0xFF, 0xFF, 0xFF), QColor(0x00, 0x00, 0x00), QColor(0x00, 0x00, 0x00)],
    MajoraControlCode.C_UP: [QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00)],
    MajoraControlCode.C_DOWN: [QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00)],
    MajoraControlCode.C_LEFT: [QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00)],
    MajoraControlCode.C_RIGHT: [QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00), QColor(0xFF, 0xFF, 0x00)],
    MajoraControlCode.TRIANGLE: [QColor(0x32, 0xCD, 0x32), QColor(0x32, 0xCD, 0x32), QColor(0x32, 0xCD, 0x32), QColor(0x32, 0xCD, 0x32)],
    MajoraControlCode.CONTROL_STICK: [QColor(0xFF, 0xFF, 0xFF), QColor(0xFF, 0xFF, 0xFF), QColor(0x00, 0x00, 0x00), QColor(0x00, 0x00, 0x00)],
    MajoraControlCode.D_PAD: [QColor(0xFF, 0xFF, 0xFF), QColor(0xFF, 0xFF, 0xFF), QColor(0x00, 0x00, 0x00), QColor(0x00, 0x00, 0x00)]
}

MAJORA_FONT_WIDTHS = [
    8.0,    # 
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
    12.0,   # Á
    12.0,   # Â
    12.0,   # Ä
    11.0,   # Ç
    8.0,    # È
    8.0,    # É
    8.0,    # Ê
    8.0,    # Ë
    6.0,    # Ï
    6.0,    # Ì
    6.0,    # Î
    6.0,    # Ï
    12.0,   # Ñ
    13.0,   # Ò
    13.0,   # Ó
    13.0,   # Ô
    13.0,   # Ö
    10.0,   # Ù
    10.0,   # Ú
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
    6.0,    # ì
    6.0,    # í
    5.0,    # î
    5.0,    # ï
    10.0,   # ñ
    9.0,    # ò
    9.0,    # ó
    9.0,    # ô
    9.0,    # ö
    9.0,    # ù
    9.0,    # ú
    9.0,    # û
    9.0,    # ü
    6.0,    # ¡
    11.0,   # ¿
    8.0,    # ª
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
    14.0    # ?
]
