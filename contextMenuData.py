from zeldaEnums import *

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

