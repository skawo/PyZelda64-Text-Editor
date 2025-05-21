from enum import IntEnum

MAX_MES_SIZE = 1280
SAVE_TABLE_FILENAME = "message_data_static_NES"
SAVE_STRINGS_FILENAME = "message_data_static_NES"

class DestinationMode(IntEnum):
    Files = 0
    ROM = 1

class MessageMode(IntEnum):
    Ocarina = 0
    Majora = 1
    Credits = 2

class OcarinaTextboxType(IntEnum):
    Black = 0
    Wooden = 1
    Blue = 2
    Ocarina = 3
    None_White = 4
    None_Black = 5
    Credits = 11

class TextboxPosition(IntEnum):
    Dynamic = 0
    Top = 1
    Center = 2
    Bottom = 3
    Unk_16 = 16
    Unk_17 = 17
    Unk_32 = 32
    Unk_33 = 33
    Unk_35 = 35
    Unk_48 = 48
    Unk_49 = 49
    Unk_113 = 113

class OcarinaControlCode(IntEnum):
    LINE_BREAK = 0x01
    END = 0x02
    NEW_BOX = 0x04
    COLOR = 0x05
    SHIFT = 0x06
    JUMP = 0x07
    DI = 0x08
    DC = 0x09
    PERSISTENT = 0x0A
    EVENT = 0x0B
    DELAY = 0x0C
    AWAIT_BUTTON = 0x0D
    FADE = 0x0E
    PLAYER = 0x0F
    OCARINA = 0x10
    FADE2 = 0x11
    SOUND = 0x12
    ICON = 0x13
    SPEED = 0x14
    BACKGROUND = 0x15
    MARATHON_TIME = 0x16
    RACE_TIME = 0x17
    POINTS = 0x18
    GOLD_SKULLTULAS = 0x19
    NS = 0x1A
    TWO_CHOICES = 0x1B
    THREE_CHOICES = 0x1C
    FISH_WEIGHT = 0x1D
    HIGH_SCORE = 0x1E
    TIME = 0x1F

    LCHEVRON = 0x3C
    RCHEVRON = 0x3E

    DASH = 0x7F
    À = 0x80
    Î = 0x81
    Â = 0x82
    Ä = 0x83
    Ç = 0x84
    È = 0x85
    É = 0x86
    Ê = 0x87
    Ë = 0x88
    Ï = 0x89
    Ô = 0x8A
    Ö = 0x8B
    Ù = 0x8C
    Û = 0x8D
    Ü = 0x8E
    ß = 0x8F
    à = 0x90
    á = 0x91
    â = 0x92
    ä = 0x93
    ç = 0x94
    è = 0x95
    é = 0x96
    ê = 0x97
    ë = 0x98
    ï = 0x99
    ô = 0x9A
    ö = 0x9B
    ù = 0x9C
    û = 0x9D
    ü = 0x9E

    A_BUTTON = 0x9F
    B_BUTTON = 0xA0
    C_BUTTON = 0xA1
    L_BUTTON = 0xA2
    R_BUTTON = 0xA3
    Z_BUTTON = 0xA4
    C_UP = 0xA5
    C_DOWN = 0xA6
    C_LEFT = 0xA7
    C_RIGHT = 0xA8,
    TRIANGLE = 0xA9
    CONTROL_STICK = 0xAA
    D_PAD = 0xAB

class OcarinaMsgColor(IntEnum):
    W = 0x40
    R = 0x41
    G = 0x42
    B = 0x43
    C = 0x44
    M = 0x45
    Y = 0x46
    BLK = 0x47

class OcarinaHighScore(IntEnum):
    ARCHERY = 0x00
    POE_POINTS = 0x01
    FISH_WEIGHT = 0x02
    HORSE_RACE = 0x03
    MARATHON = 0x04
    HS_UNK = 0x05
    DAMPE_RACE = 0x06

class OcarinaIcon(IntEnum):
    DEKU_STICK = 0
    DEKU_NUT = 1
    BOMBS = 2
    BOW = 3
    FIRE_ARROWS = 4
    DINS_FIRE = 5
    SLINGSHOT = 6
    FAIRY_OCARINA = 7
    OCARINA_OF_TIME = 8
    BOMBCHUS = 9
    HOOKSHOT = 10
    LONGSHOT = 11
    ICE_ARROWS = 12
    FARORES_WIND = 13
    BOOMERANG = 14
    LENS_OF_TRUTH = 15
    BEANS = 16
    MEGATON_HAMMER = 17
    LIGHT_ARROWS = 18
    NAYRUS_LOVE = 19
    EMPTY_BOTTLE = 20
    RED_POTION = 21
    GREEN_POTION = 22
    BLUE_POTION = 23
    FAIRY = 24
    FISH = 25
    MILK = 26
    RUTOS_LETTER = 27
    BLUE_FIRE = 28
    BOTTLE_BUG = 29
    BOTTLE_POE = 30
    HALF_MILK = 31
    BOTTLE_BIGPOE = 32
    WEIRD_EGG = 33
    CHICKEN = 34
    ZELDAS_LETTER = 35
    KEATON_MASK = 36
    SKULL_MASK = 37
    SPOOKY_MASK = 38
    BUNNY_HOOD = 39
    GORON_MASK = 40
    ZORA_MASK = 41
    GERUDO_MASK = 42
    MASK_OF_TRUTH = 43
    SOLD_OUT = 44
    POCKET_EGG = 45
    POCKET_CUCCO = 46
    COJIRO = 47
    ODD_MUSHROOM = 48
    ODD_POTION = 49
    POACHERS_SAW = 50
    BROKEN_SWORD = 51
    PRESCRIPTION = 52
    EYEBALL_FROG = 53
    EYEDROPS = 54
    CLAIM_CHECK = 55
    BOW_FIRE = 56
    BOW_ICE = 57
    BOW_LIGHT = 58
    KOKIRI_SWORD = 59
    MASTER_SWORD = 60
    BIGGORON_SWORD = 61
    DEKU_SHIELD = 62
    HYLIAN_SHIELD = 63
    MIRROR_SHIELD = 64
    KOKIRI_TUNIC = 65
    GORON_TUNIC = 66
    ZORA_TUNIC = 67
    BOOTS = 68
    IRON_BOOTS = 69
    HOVER_BOOTS = 70
    BULLET_BAG = 71
    BIGGER_BULLET_BAG = 72
    BIGGEST_BULLET_BAG = 73
    QUIVER = 74
    BIG_QUIVER = 75
    BIGGEST_QUIVER = 76
    BOMB_BAG = 77
    BIGGER_BOMB_BAG = 78
    BIGGEST_BOMB_BAG = 79
    GORON_BRACELET = 80
    SILVER_GAUNTLETS = 81
    GOLDEN_GAUNTLETS = 82
    ZORA_SCALE = 83
    GOLDEN_SCALE = 84
    BROKEN_KNIFE = 85
    ADULTS_WALLET = 86
    GIANTS_WALLET = 87
    DEKU_SEEDS = 88
    FISHING_ROD = 89
    NOTHING_1 = 90
    NOTHING_2 = 91
    NOTHING_3 = 92
    NOTHING_4 = 93
    NOTHING_5 = 94
    NOTHING_6 = 95
    NOTHING_7 = 96
    NOTHING_9 = 97
    NOTHING_10 = 98
    NOTHING_11 = 99
    NOTHING_12 = 100
    NOTHING_13 = 101
    FOREST_MEDALLION = 102
    FIRE_MEDALLION = 103
    WATER_MEDALLION = 104
    SPIRIT_MEDALLION = 105
    SHADOW_MEDALLION = 106
    LIGHT_MEDALLION = 107
    KOKIRI_EMERALD = 108
    GORON_RUBY = 109
    ZORA_SAPPHIRE = 110
    STONE_OF_AGONY = 111
    GERUDO_PASS = 112
    GOLDEN_SKULLTULA = 113
    HEART_CONTAINER = 114
    HEART_PIECE = 115
    BOSS_KEY = 116
    COMPASS = 117
    DUNGEON_MAP = 118
    SMALL_KEY = 119
    MAGIC_JAR = 120
    BIG_MAGIC_JAR = 121

class MajoraTextboxType(IntEnum):
    Black = 0
    Wooden = 1
    Blue = 2
    Ocarina = 3
    None_White = 4 
    None_Black = 5
    Black2 = 6
    No_Box = 7
    Blue2 = 8
    Red = 9 
    None2 = 10
    Credits = 11
    None3 = 12
    Bombers_Notebook = 13
    None4 = 14
    Red2 = 15

class MajoraMsgColor(IntEnum):
    D = 0x00
    R = 0x01
    G = 0x02
    B = 0x03
    Y = 0x04
    N = 0x05
    P = 0x06
    S = 0x07
    O = 0x08

class MajoraIcon(IntEnum):
    GREEN_RUPEE = 1
    BLUE_RUPEE = 2
    WHITE_RUPEE = 3
    RED_RUPEE = 4
    PURPLE_RUPEE = 5
    ORANGE_RUPEE = 7
    ADULT_WALLET = 8
    GIANTS_WALLET = 9
    RECOVERY_HEART = 10
    PIECE_OF_HEART = 12
    HEART_CONTAINER = 13
    SMALL_MAGIC_JAR = 14
    LARGE_MAGIC_JAR = 15
    STRAY_FAIRY = 17
    BOMB = 20
    BOMB_2 = 21
    BOMB_3 = 22
    BOMB_4 = 23
    BOMB_5 = 24
    DEKU_STICK = 25
    BOMBCHU = 26
    BOMB_BAG = 27
    BIG_BOMB_BAG = 28
    BIGGER_BOMB_BAG = 29
    HEROS_BOW = 30
    HEROS_BOW_1 = 31
    HEROS_BOW_2 = 32
    HEROS_BOW_3 = 33
    QUIVER = 34
    BIG_QUIVER = 35
    BIGGEST_QUIVER = 36
    FIRE_ARROW = 37
    ICE_ARROW = 38
    LIGHT_ARROW = 39
    DEKU_NUT = 40
    DEKU_NUT_1 = 41
    DEKU_NUT_2 = 42
    HEROS_SHIELD = 50
    MIRROR_SHIELD = 51
    POWDER_KEG = 52
    MAGIC_BEAN = 53
    KOKIRI_SWORD = 55
    RAZOR_SWORD = 56
    GILDED_SWORD = 57
    FIERCE_DEITYS_SWORD = 58
    GREAT_FAIRYS_SWORD = 59
    SMALL_KEY = 60
    BOSS_KEY = 61
    DUNGEON_MAP = 62
    COMPASS = 63
    POWDER_KEG_2 = 64
    HOOKSHOT = 65
    LENS_OF_TRUTH = 66
    PICTOGRAPH_BOX = 67
    FISHING_ROD = 68
    OCARINA_OF_TIME = 76
    BOMBERS_NOTEBOOK = 80
    GOLD_SKULLTULA_TOKEN = 82
    ODOLWAS_REMAINS = 85
    GOHTS_REMAINS = 86
    GYORGS_REMAINS = 87
    TWINMOLDS_REMAINS = 88
    RED_POTION = 89
    EMPTY_BOTTLE = 90
    RED_POTION_2 = 91
    GREEN_POTION = 92
    BLUE_POTION = 93
    FAIRYS_SPIRIT = 94
    DEKU_PRINCESS = 95
    MILK = 96
    MILK_HALF = 97
    FISH = 98
    BUG = 99
    BLUE_FIRE = 100
    POE = 101
    BIG_POE = 102
    SPRING_WATER = 103
    HOT_SPRING_WATER = 104
    ZORA_EGG = 105
    GOLD_DUST = 106
    MUSHROOM = 107
    SEAHORSE = 110
    CHATEAU_ROMANI = 111
    HYLIAN_LOACH = 112
    DEKU_MASK = 120
    GORON_MASK = 121
    ZORA_MASK = 122
    FIERCE_DEITY_MASK = 123
    MASK_OF_TRUTH = 124
    KAFEIS_MASK = 125
    ALL_NIGHT_MASK = 126
    BUNNY_HOOD = 127
    KEATON_MASK = 128
    GARO_MASK = 129
    ROMANI_MASK = 130
    CIRCUS_LEADERS_MASK = 131
    POSTMANS_HAT = 132
    COUPLES_MASK = 133
    GREAT_FAIRYS_MASK = 134
    GIBDO_MASK = 135
    DON_GEROS_MASK = 136
    KAMAROS_MASK = 137
    CAPTAINS_HAT = 138
    STONE_MASK = 139
    BREMEN_MASK = 140
    BLAST_MASK = 141
    MASK_OF_SCENTS = 142
    GIANTS_MASK = 143
    GOLD_DUST_2 = 147
    HYLIAN_LOACH_2 = 148
    SEAHORSE_2 = 149
    MOONS_TEAR = 150
    TOWN_TITLE_DEED = 151
    SWAMP_TITLE_DEED = 152
    MOUNTAIN_TITLE_DEED = 153
    OCEAN_TITLE_DEED = 154
    ROOM_KEY = 160
    SPECIAL_DELIVERY_TO_MAMA = 161
    LETTER_TO_KAFEI = 170
    PENDANT_OF_MEMORIES = 171
    TINGLES_MAP = 179
    TINGLES_MAP_2 = 180
    TINGLES_MAP_3 = 181
    TINGLES_MAP_4 = 182
    TINGLES_MAP_5 = 183
    TINGLES_MAP_6 = 184
    TINGLES_MAP_7 = 185
    ANJU = 220
    KAFEI = 221
    CURIOSITY_SHOP_OWNER = 222
    BOMB_SHOP_OWNERS_MOTHER = 223
    ROMANI = 224
    CREMIA = 225
    MAYOR_DOTOUR = 226
    MADAME_AROMA = 227
    TOTO = 228
    GORMAN = 229
    POSTMAN = 230
    ROSA_SISTERS = 231
    TOILET_HAND = 232
    GRANNY = 233
    KAMARO = 234
    GROG = 235
    GORMAN_BROTHERS = 236
    SHIRO = 237
    GURUGURU = 238
    BOMBERS = 239
    EXCLAMATION_MARK = 240
    NO_ICON = 254

class MajoraControlCode(IntEnum):
    COLOR_DEFAULT = 0x00
    COLOR_RED = 0x01
    COLOR_GREEN = 0x02
    COLOR_BLUE = 0x03
    COLOR_YELLOW = 0x04
    COLOR_NAVY = 0x05
    COLOR_PINK = 0x06
    COLOR_SILVER = 0x07
    COLOR_ORANGE = 0x08
    UNK_09 = 0x09
    NULL_CHAR = 0x0A
    SWAMP_CRUISE_HITS = 0x0B
    STRAY_FAIRY_SCORE = 0x0C
    GOLD_SKULLTULAS = 0x0D
    FISH_WEIGHT = 0x0E
    UNK_0F = 0x0F
    NEW_BOX = 0x10
    LINE_BREAK = 0x11
    NEW_BOX_CENTER = 0x12
    RESET_CURSOR = 0x13
    SHIFT = 0x14
    NOSKIP = 0x15
    PLAYER = 0x16
    DI = 0x17
    DC = 0x18
    NOSKIP_SOUND = 0x19
    PERSISTENT = 0x1A
    DELAY_NEWBOX = 0x1B
    FADE = 0x1C
    DELAY_END = 0x1D
    SOUND = 0x1E
    DELAY = 0x1F
    END = 0xBF
    BACKGROUND = 0xC1
    TWO_CHOICES = 0xC2
    THREE_CHOICES = 0xC3
    POSTMAN_RESULTS = 0xC4
    TIMER = 0xC5
    TIMER2 = 0xC6
    MOON_CRASH_TIME = 0xC7
    DEKU_RESULTS = 0xC8
    TIMER3 = 0xC9
    TIMER4 = 0xCA
    SHOOTING_GALLERY_RESULT = 0xCB
    BANK_PROMPT = 0xCC
    RUPEES_ENTERED = 0xCD
    RUPEES_IN_BANK = 0xCE
    MOON_CRASH_TIME_REMAINS = 0xCF
    BET_RUPEES_PROMPT = 0xD0
    BOMBER_CODE_PROMPT = 0xD1
    ITEM_PROMPT = 0xD2
    UNK_D3 = 0xD3
    SOARING_DESTINATION = 0xD4
    LOTTERY_NUMBER_PROMPT = 0xD5
    OCEANSIDE_HOUSE_ORDER = 0xD6
    WOODFALL_FAIRIES_REMAIN = 0xD7
    SNOWHEAD_FAIRIES_REMAIN = 0xD8
    BAY_FAIRIES_REMAIN = 0xD9
    IKANA_FAIRIES_REMAIN = 0xDA
    SWAMP_CRUISE_RESULT = 0xDB
    WINNING_LOTTERY_NUM = 0xDC
    PLAYER_LOTTERY_NUM = 0xDD
    ITEM_VALUE = 0xDE
    BOMBER_CODE = 0xDF
    END_CONVERSATION = 0xE0
    OCEANSIDE_HOUSE_ORDER_1 = 0xE1
    OCEANSIDE_HOUSE_ORDER_2 = 0xE2
    OCEANSIDE_HOUSE_ORDER_3 = 0xE3
    OCEANSIDE_HOUSE_ORDER_4 = 0xE4
    OCEANSIDE_HOUSE_ORDER_5 = 0xE5
    OCEANSIDE_HOUSE_ORDER_6 = 0xE6
    MOON_CRASH_HOURS_REMAIN = 0xE7
    UNTIL_MORNING = 0xE8
    UNK_E9 = 0xE9
    UNK_EA = 0xEA
    UNK_EB = 0xEB
    UNK_EC = 0xEC
    UNK_ED = 0xED
    UNK_EE = 0xEE
    UNK_EF = 0xEF
    TOTAL_IN_BANK = 0xF0
    UNK_F1 = 0xF1
    UNK_F2 = 0xF2
    UNK_F3 = 0xF3
    UNK_F4 = 0xF4
    UNK_F5 = 0xF5
    TOWN_SHOOTING_HIGHSCORE = 0xF6
    UNK_F7 = 0xF7
    UNK_F8 = 0xF8
    EPONA_ARCHERY_HIGHSCORE = 0xF9
    DEKU_HIGHSCORE_DAY1 = 0xFA
    DEKU_HIGHSCORE_DAY2 = 0xFB
    DEKU_HIGHSCORE_DAY3 = 0xFC
    UNK_FD = 0xFD
    UNK_FE = 0xFE
    UNK_FF = 0xFF
    LCHEVRON = 0x3C
    RCHEVRON = 0x3E
    DASH = 0x7F
    À = 0x80
    Á = 0x81
    Â = 0x82
    Ä = 0x83
    Ç = 0x84
    È = 0x85
    É = 0x86
    Ê = 0x87
    Ë = 0x88
    Ì = 0x89
    Í = 0x8A
    Î = 0x8B
    Ï = 0x8C
    Ñ = 0x8D
    Ò = 0x8E
    Ó = 0x8F
    Ô = 0x90
    Ö = 0x91
    Ù = 0x92
    Ú = 0x93
    Û = 0x94
    Ü = 0x95
    ß = 0x96
    à = 0x97
    á = 0x98
    â = 0x99
    ä = 0x9A
    ç = 0x9B
    è = 0x9C
    é = 0x9D
    ê = 0x9E
    ë = 0x9F
    ì = 0xA0
    í = 0xA1
    î = 0xA2
    ï = 0xA3
    ñ = 0xA4
    ò = 0xA5
    ó = 0xA6
    ô = 0xA7
    ö = 0xA8
    ù = 0xA9
    ú = 0xAA
    û = 0xAB
    ü = 0xAC
    A_BUTTON = 0xB0
    B_BUTTON = 0xB1
    C_BUTTON = 0xB2
    L_BUTTON = 0xB3
    R_BUTTON = 0xB4
    Z_BUTTON = 0xB5
    C_UP = 0xB6
    C_DOWN = 0xB7
    C_LEFT = 0xB8
    C_RIGHT = 0xB9
    TRIANGLE = 0xBA
    CONTROL_STICK = 0xBB
    D_PAD = 0xBC


class ContextMenuData:
    MajoraColors = [
        ("Default", f'{MajoraMsgColor.D.name}', "Will appear white in most cases, but black in 'None_White' and 'Bomber Notebook'-type textboxes. Will also appear black inside the Bomber's Notebook itself."),
        ("Red", f'{MajoraMsgColor.R.name}', "Appears orange in 'Wooden'-type textboxes"),
        ("Green", f'{MajoraMsgColor.G.name}', "Inexplicably appears blue inside Bomber's Notebook"),
        ("Blue", f'{MajoraMsgColor.B.name}', ""),
        ("Yellow", f'{MajoraMsgColor.Y.name}', ""),
        ("Navy", f'{MajoraMsgColor.N.name}', ""),
        ("Silver", f'{MajoraMsgColor.S.name}', ""),
        ("Orange", f'{MajoraMsgColor.O.name}', "")
    ]

    Buttons = [
        ("A Button", f'{MajoraControlCode.A_BUTTON.name}', ""),
        ("B Button", f'{MajoraControlCode.B_BUTTON.name}', ""),
        ("C Button", f'{MajoraControlCode.C_BUTTON.name}', ""),
        ("C-Up Button", f'{MajoraControlCode.C_UP.name}', ""),
        ("C-Down Button", f'{MajoraControlCode.C_DOWN.name}', ""),
        ("C-Left Button", f'{MajoraControlCode.C_LEFT.name}', ""),
        ("C-Right Button", f'{MajoraControlCode.C_RIGHT.name}', ""),
        ("L Button", f'{MajoraControlCode.L_BUTTON.name}', ""),
        ("R Button", f'{MajoraControlCode.R_BUTTON.name}', ""),
        ("Z Button", f'{MajoraControlCode.Z_BUTTON.name}', ""),
        ("Triangle", f'{MajoraControlCode.TRIANGLE.name}', ""),
        ("Control Stick", f'{MajoraControlCode.CONTROL_STICK.name}', ""),
        ("D-Pad", f'{MajoraControlCode.D_PAD.name}', "Crashes the game in Majora's Mask.")
    ]

    ColorsOcarina = [
        ("White", f'{OcarinaMsgColor.W.name}', "Will appear black in 'None_White'-type textboxes"),
        ("Red", f'{OcarinaMsgColor.R.name}', "Appears orange in 'Wooden'-type textboxes"),
        ("Green", f'{OcarinaMsgColor.G.name}', ""),
        ("Blue", f'{OcarinaMsgColor.B.name}', ""),
        ("Cyan", f'{OcarinaMsgColor.C.name}', ""),
        ("Magenta", f'{OcarinaMsgColor.M.name}', ""),
        ("Yellow", f'{OcarinaMsgColor.Y.name}', ""),
        ("Black", f'{OcarinaMsgColor.BLK.name}', "")
    ]

    ScoresMajora = [
        ("Required Swamp Cruise Hits", f'{MajoraControlCode.SWAMP_CRUISE_HITS.name}', "Print the number of hits required to win the Swamp Cruise reward."),
        ("Stray Fairies", f'{MajoraControlCode.STRAY_FAIRY_SCORE.name}', "Print the amount of Stray Fairies collected in the current dungeon."),
        ("Gold Skulltulas", f'{MajoraControlCode.GOLD_SKULLTULAS.name}', "Print the amount of Gold Skulltula tokens collected in the current spider house."),
        ("Postman Minigame Time", f'{MajoraControlCode.POSTMAN_RESULTS.name}', "Print the time score attained in the postman minigame."),
        ("Timer", f'{MajoraControlCode.TIMER.name}', "Print the time shown on the last timer."),
        ("Moon Crash Time Left", f'{MajoraControlCode.MOON_CRASH_TIME.name}', "Print remaining time until Moon Crash (as on the Clock Tower roof)"),
        ("Deku Flying Time", f'{MajoraControlCode.DEKU_RESULTS.name}', "Print time attained in the Deku Flying minigame"),
        ("Town Shooting Gallery High Score", f'{MajoraControlCode.TOWN_SHOOTING_HIGHSCORE.name}', "Print the Town Shooting Gallery High Score"),
        ("Shooting Gallery Result", f'{MajoraControlCode.SHOOTING_GALLERY_RESULT.name}', "Print score attained in the Shooting Gallery"),
        ("Swamp Cruise Score", f'{MajoraControlCode.SWAMP_CRUISE_RESULT.name}', "Print score attained in the Swamp Cruise"),
        ("Winning Lottery Number", f'{MajoraControlCode.WINNING_LOTTERY_NUM.name}', "Print the winning lottery number"),
        ("Player's Lottery Number", f'{MajoraControlCode.PLAYER_LOTTERY_NUM.name}', "Print the player's lottery number"),
        ("Time remains", f'{MajoraControlCode.MOON_CRASH_TIME_REMAINS.name}', "Print time remaining in hours & minutes"),
        ("Hours remain", f'{MajoraControlCode.MOON_CRASH_HOURS_REMAIN.name}', "Print time remaining in hours"),
        ("Hours remain until morning", f'{MajoraControlCode.UNTIL_MORNING.name}', "Print time remaining until sunrise in hours & minutes"),
        ("Horseback Archery High Score", f'{MajoraControlCode.EPONA_ARCHERY_HIGHSCORE.name}', "Print the Epona Archery high score (Romani Ranch Balloon Game)"),
        ("Fish weight", f'{MajoraControlCode.FISH_WEIGHT.name}', "Print the caught fish's weight. Unused two-digit minigame score."),
        ("Deku Flying Highscore 1", f'{MajoraControlCode.DEKU_HIGHSCORE_DAY1.name}', "Print the Deku Flying high score from Day 1)"),
        ("Deku Flying Highscore 2", f'{MajoraControlCode.DEKU_HIGHSCORE_DAY2.name}', "Print the Deku Flying high score from Day 2)"),
        ("Deku Flying Highscore 3", f'{MajoraControlCode.DEKU_HIGHSCORE_DAY3.name}', "Print the Deku Flying high score from Day 3)")
    ]

    PromptsMajora = [
        ("Bank Prompt", f'{MajoraControlCode.BANK_PROMPT.name}', "Print the withdraw/deposit rupees prompt"),
        ("Rupees Entered in Prompt", f'{MajoraControlCode.RUPEES_ENTERED.name}', "Print the amount of rupees entered in the withdraw/deposit prompt"),
        ("Rupees in bank", f'{MajoraControlCode.RUPEES_IN_BANK.name}', "Print the amount of rupees deposited in the bank or won by betting"),
        ("Bet Rupees Prompt", f'{MajoraControlCode.BET_RUPEES_PROMPT.name}', "Print the rupee bet prompt"),
        ("Lottery Number Prompt", f'{MajoraControlCode.LOTTERY_NUMBER_PROMPT.name}', "Print the Lottery Number prompt"),
        ("Bomber's Code Prompt", f'{MajoraControlCode.BOMBER_CODE_PROMPT.name}', "Print the Bomber's Code prompt"),
        ("Item prompt", f'{MajoraControlCode.ITEM_PROMPT.name}', "Used in the Open-Menu-And-Choose-An-Item Message"),
        ("Song of Soaring Destination", f'{MajoraControlCode.SOARING_DESTINATION.name}', "Print the chosen Song of Soaring destination")
    ]

    CompletionMajora = [
        ("Oceanside House Order", f'{MajoraControlCode.OCEANSIDE_HOUSE_ORDER.name}', "Unused: print the entire Oceanside House Mask order"),
        ("Oceanside House Order 1", f'{MajoraControlCode.OCEANSIDE_HOUSE_ORDER_1.name}', "Print the first Oceanside House Mask color"),
        ("Oceanside House Order 2", f'{MajoraControlCode.OCEANSIDE_HOUSE_ORDER_2.name}', "Print the second Oceanside House Mask color"),
        ("Oceanside House Order 3", f'{MajoraControlCode.OCEANSIDE_HOUSE_ORDER_3.name}', "Print the third Oceanside House Mask color"),
        ("Oceanside House Order 4", f'{MajoraControlCode.OCEANSIDE_HOUSE_ORDER_4.name}', "Print the fourth Oceanside House Mask color"),
        ("Oceanside House Order 5", f'{MajoraControlCode.OCEANSIDE_HOUSE_ORDER_5.name}', "Print the fifth Oceanside House Mask color"),
        ("Remaining Woodfall Fairies", f'{MajoraControlCode.WOODFALL_FAIRIES_REMAIN.name}', "Print the amount of fairies left at the Woodfall Temple"),
        ("Remaining Snowhead Fairies", f'{MajoraControlCode.SNOWHEAD_FAIRIES_REMAIN.name}', "Print the amount of fairies left at the Woodfall Temple"),
        ("Remaining Great Bay Fairies", f'{MajoraControlCode.BAY_FAIRIES_REMAIN.name}', "Print the amount of fairies left at the Great Bay Temple"),
        ("Remaining Stone Tower Fairies", f'{MajoraControlCode.IKANA_FAIRIES_REMAIN.name}', "Print the amount of fairies left at the Stone Tower Temple"),
        ("Bomber's Code", f'{MajoraControlCode.BOMBER_CODE.name}', "Print the Bomber's Code")
    ]

    GenericTagMajora = [
        ("Null character", f'{MajoraControlCode.NULL_CHAR.name}', "Prints nothing, causing the text routine to print out slower."),
        ("New textbox", f'{MajoraControlCode.NEW_BOX.name}', "Starts a new message."),
        ("New textbox and center", f'{MajoraControlCode.NEW_BOX_CENTER.name}', "Starts a new message and ignores any extraneous linebreaks if the message has less than 4 lines"),
        ("Reset cursor", f'{MajoraControlCode.RESET_CURSOR.name}', "Used as a filler when there are fewer than four lines of text."),
        ("Offset", f'{MajoraControlCode.SHIFT.name}:{0}', "Insert the specified number of spaces into the textbox."),
        ("No skip", f'{MajoraControlCode.NOSKIP.name}', "Disallows skipping the message box it's inserted into using the B button."),
        ("No skip with sound", f'{MajoraControlCode.NOSKIP_SOUND.name}', "Disallows skipping the message box it's inserted into using the B button, and plays the 'sound finished' sound at the end."),
        ("Player name", f'{MajoraControlCode.PLAYER.name}', "Writes out the player's name (set on the file selection screen)."),
        ("Draw instantly", f'{MajoraControlCode.DI.name}', "Prints whatever follows this tag instantly until a Draw-Per-Character tag is present."),
        ("Draw per-character", f'{MajoraControlCode.DC.name}', "Prints whatever follows this tag one character at a time. This is the default typing mode."),
        ("Persistent", f'{MajoraControlCode.PERSISTENT.name}', "Prevents the player from closing the textbox in any way. Used for shop descriptions."),
        ("Delay, then new textbox", f'{MajoraControlCode.DELAY_NEWBOX.name}', "Inserts a pause in the text, then opens new textbox."),
        ("Delay", f'{MajoraControlCode.DELAY.name}', "Inserts a pause in the text."),
        ("Delay, then close textbox", f'{MajoraControlCode.DELAY_END.name}', "Inserts a pause in the text before closing the textbox."),
        ("Fade", f'{MajoraControlCode.FADE.name}:{0}', "Waits for the specified number of frames until ending the textbox."),
        ("Two choices", f'{MajoraControlCode.TWO_CHOICES.name}', "Displays a prompt which lets the player choose between two choices."),
        ("Three choices", f'{MajoraControlCode.THREE_CHOICES.name}', "Displays a prompt which lets the player choose between three choices."),
        ("Item Value", f'{MajoraControlCode.ITEM_VALUE.name}', "Displays the item value, taken from the message field."),
        ("End Conversation", f'{MajoraControlCode.END_CONVERSATION.name}', "Should be used at the end of NPC message, otherwise they become impossible to talk to again.")
    ]

    HighScoresOcarina = [
        ("Archery", f'{OcarinaControlCode.HIGH_SCORE.name}:{OcarinaHighScore.ARCHERY.name}', ""),
        ("Poe Salesman Points", f'{OcarinaControlCode.HIGH_SCORE.name}:{OcarinaHighScore.POE_POINTS.name}', ""),
        ("Fish weight", f'{OcarinaControlCode.HIGH_SCORE.name}:{OcarinaHighScore.FISH_WEIGHT.name}', ""),
        ("Horse race time", f'{OcarinaControlCode.HIGH_SCORE.name}:{OcarinaHighScore.HORSE_RACE.name}', ""),
        ("Running Man's marathon", f'{OcarinaControlCode.HIGH_SCORE.name}:{OcarinaHighScore.MARATHON.name}', ""),
        ("Dampe race", f'{OcarinaControlCode.HIGH_SCORE.name}:{OcarinaHighScore.DAMPE_RACE.name}', "")
    ]

    ScoresOcarina = [
        ("Running Man's time", f'{OcarinaControlCode.MARATHON_TIME.name}', "Running Man's marathon time result."),
        ("Timer", f'{OcarinaControlCode.RACE_TIME.name}', "Prints time shown on the last timer."),
        ("Archery points", f'{OcarinaControlCode.POINTS.name}', "Horseback Archery points result."),
        ("Gold skulltulas", f'{OcarinaControlCode.GOLD_SKULLTULAS.name}', "Current amount of Gold Skulltulas owned."),
        ("Fish weight", f'{OcarinaControlCode.FISH_WEIGHT.name}', "Caught fish's weight.")
    ]

    GenericTagOcarina = [
        ("Delay", f'{OcarinaControlCode.DELAY.name}:{0}', "Waits for the specified number of frames until switching to the next textbox."),
        ("Fade", f'{OcarinaControlCode.FADE.name}:{0}', "Waits for the specified number of frames until ending the textbox."),
        ("Fade2", f'{OcarinaControlCode.FADE2.name}:{0}', "Waits for the specified number of frames until ending the textbox. The duration can be made longer than with the FADE tag."),
        ("Offset", f'{OcarinaControlCode.SHIFT.name}:{0}', "Insert the specified number of spaces into the textbox."),
        ("New textbox", f'{OcarinaControlCode.NEW_BOX.name}', "Starts a new message."),
        ("Jump", f'{OcarinaControlCode.JUMP.name}:{0}', "Jumps to the specified message ID."),
        ("Player name", f'{OcarinaControlCode.PLAYER.name}', "Writes out the player's name (set on the file selection screen)."),
        ("No skip", f'{OcarinaControlCode.NS.name}', "Disallows skipping the message box it's inserted into using the B button."),
        ("Speed", f'{OcarinaControlCode.SPEED.name}:{0}', "Sets the amount of frames spent waiting between typing out each character."),
        ("Persistent", f'{OcarinaControlCode.PERSISTENT.name}', "Prevents the player from closing the textbox in any way. Used for shop descriptions."),
        ("Event", f'{OcarinaControlCode.EVENT.name}', "Prevents the textbox from closing until a programmed event does so."),
        ("Background", f'{OcarinaControlCode.BACKGROUND.name}:{0}', "Used to draw the failure X whenever player plays a song wrong. The variable seems to control the color."),
        ("Draw instantly", f'{OcarinaControlCode.DI.name}', "Prints whatever follows this tag instantly until a Draw-Per-Character tag is present."),
        ("Draw per-character", f'{OcarinaControlCode.DC.name}', "Prints whatever follows this tag one character at a time. This is the default typing mode."),
        ("Button prompt", f'{OcarinaControlCode.AWAIT_BUTTON.name}', "Waits until the player presses a button."),
        ("Two choices", f'{OcarinaControlCode.TWO_CHOICES.name}', "Displays a prompt which lets the player choose between two choices."),
        ("Three choices", f'{OcarinaControlCode.THREE_CHOICES.name}', "Displays a prompt which lets the player choose between three choices.")
    ]

