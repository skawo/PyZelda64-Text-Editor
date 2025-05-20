import struct
import string

from ZeldaEnums import *
from io import BytesIO

def GetMessageList(tableData, stringData, mode):
    messageRecordList = []
    messageList = []

    with BytesIO(tableData) as file:
        while True:
            peek_bytes = file.read(2)
            if not peek_bytes or struct.unpack('>h', peek_bytes)[0] == -1:
                file.seek(-2, 1)
                break
                
            file.seek(-2, 1)
            record = TableRecord(file)
            
            if any(x.messageId == record.messageId for x in messageRecordList):
                return None
                
            messageRecordList.append(record)

    with BytesIO(stringData) as file:
        for record in messageRecordList:
            if record.offset >= len(stringData):      
                continue     

            file.seek(record.offset)    
            start_pos = file.tell()

            message = Message(file, record, mode)

            if (file.tell() - start_pos > MAX_MES_SIZE):
                return None

            messageList.append(message)

    return messageList

def FormatMessageID(messageId):
    return '0x' + format(messageId & 0xFFFF, '04X')

class TableRecord:
    def __init__(self, reader):

        self.messageId = struct.unpack('>h', reader.read(2))[0] & 0xFFFF
        
        typePos = reader.read(1)[0]
        
        self.boxType = OcarinaTextboxType((typePos & 0xF0) >> 4)
        self.boxPosition = TextboxPosition(typePos & 0x0F)
    
        reader.read(1)
        self.offset = struct.unpack('>I', reader.read(4))[0] & 0x00FFFFFF


class Message:
    def __init__(self, reader, record, mode):

        if reader is None or record is None:
            self.messageId = 0
            self.boxType = 0
            self.boxPosition = 0
            self.textData = ""

            if mode == MessageMode.Majora:
                self.majoraIcon = 0
                self.majoraJumpTo = 0
                self.majoraFirstPrice = 0
                self.majoraSecondPrice = 0
            return

        self.reader = reader
        self.mode = mode

        if mode == MessageMode.Majora:
            self.messageId = record.messageId & 0xFFFF
            self.boxType = self.__get_byte()
            self.boxPosition = self.__get_byte() 
            self.majoraIcon = self.__get_byte()
            self.majoraJumpTo = self.__get_halfword()
            self.majoraFirstPrice = self.__get_halfword()
            self.majoraSecondPrice = self.__get_halfword()
            self.__get_halfword() # Padding
        else:
            self.messageId = record.messageId & 0xFFFF
            self.boxType = record.boxType
            self.boxPosition = record.boxPosition

        self.textData = self.__GetStringData()

    def __get_byte(self):
        return int.from_bytes(self.reader.read(1))
    
    def __get_halfword(self):
        return struct.unpack('>h', self.reader.read(2))[0]
    
    def __get_word(self):
        return struct.unpack('>w', self.reader.read(4))[0]

    def __GetStringData(self):
        char_data = []
        cur_byte = self.__get_byte()

        controlCodeType = MajoraControlCode if self.mode == MessageMode.Majora else OcarinaControlCode
        func = self.GetControlCodeMajora if self.mode == MessageMode.Majora else self.GetControlCode

        boundByte = 0xAF if self.mode == MessageMode.Majora else 0x9E

        while cur_byte != controlCodeType.END:
            read_control_code = False

            if cur_byte < 0x7F or cur_byte > boundByte:
                if (cur_byte in controlCodeType):
                    char_data.extend(func(controlCodeType(cur_byte)))
                    read_control_code = True

            if not read_control_code:
                if cur_byte == 0x7F:
                    # Never actually used in-game. Appears blank.
                    char_data.append(' ')
                # Stressed characters
                elif 0x80 <= cur_byte <= boundByte:
                    char_data.append(controlCodeType(cur_byte).name[0])
                # ASCII-mapped characters
                elif ((0x20 <= cur_byte < 0x7F) or 
                    chr(cur_byte).isalnum() or 
                    chr(cur_byte).isspace() or 
                    chr(cur_byte) in string.punctuation):
                    char_data.append(chr(cur_byte))
                else:
                    char_data.extend(f"<UNK {cur_byte:X}>")

            if self.reader.tell() != len(self.reader.getvalue()):
                cur_byte = self.__get_byte()
            else:
                cur_byte = controlCodeType.END

        return ''.join(char_data)
    
    def GetControlCodeMajora(self, code):
        code_bank = []
        code_insides = ""

        if code in [
            MajoraControlCode.COLOR_DEFAULT,
            MajoraControlCode.COLOR_RED,
            MajoraControlCode.COLOR_GREEN,
            MajoraControlCode.COLOR_BLUE,
            MajoraControlCode.COLOR_YELLOW,
            MajoraControlCode.COLOR_NAVY,
            MajoraControlCode.COLOR_PINK,
            MajoraControlCode.COLOR_SILVER,
            MajoraControlCode.COLOR_ORANGE
        ]:
            code_insides = MajoraMsgColor(code.value).name

        elif code == MajoraControlCode.SHIFT:
            num_spaces = self.__get_byte()
            code_insides = f"{MajoraControlCode.SHIFT}:{num_spaces}"

        elif code == MajoraControlCode.LINE_BREAK:
            return list("\n")

        elif code == MajoraControlCode.NEW_BOX:
            return list(f"\n<{MajoraControlCode.NEW_BOX.name}>\n")

        elif code == MajoraControlCode.NEW_BOX_CENTER:
            return list(f"\n<{MajoraControlCode.NEW_BOX_CENTER.name}>\n")

        elif code in [
            MajoraControlCode.DELAY,
            MajoraControlCode.DELAY_NEWBOX,
            MajoraControlCode.DELAY_END,
            MajoraControlCode.FADE
        ]:
            delay = self.__get_halfword()
            code_insides = f"{code.name}:{delay}"

        elif code == MajoraControlCode.SOUND:
            sound_id = self.__get_halfword()
            code_insides = f"{OcarinaControlCode.SOUND.name}:{sound_id}"

        else:
            code_insides = code.name

        code_bank.extend(f"<{code_insides}>")
        return code_bank

    def GetControlCode(self, code):
        code_bank = []
        code_insides = ""

        try:
            if code == OcarinaControlCode.COLOR:
                color = OcarinaMsgColor(self.__get_byte())
                code_insides = color.name
            
            elif code == OcarinaControlCode.ICON:
                icon_id = self.__get_byte()

                try: icon_name = OcarinaIcon(icon_id).name
                except: icon_name = str(icon_id)

                code_insides = f"{OcarinaControlCode.ICON.name}:{icon_name}"
            
            elif code == OcarinaControlCode.LINE_BREAK:
                return list("\n")
            
            elif code == OcarinaControlCode.SHIFT:
                num_spaces = self.__get_byte()
                code_insides = f"{OcarinaControlCode.SHIFT.name}:{num_spaces}"
            
            elif code == OcarinaControlCode.DELAY:
                num_frames = self.__get_byte()
                code_insides = f"{OcarinaControlCode.DELAY.name}:{num_frames}"
            
            elif code == OcarinaControlCode.FADE:
                num_frames_fade = self.__get_byte()
                code_insides = f"{OcarinaControlCode.FADE.name}:{num_frames_fade}"
            
            elif code == OcarinaControlCode.FADE2:
                num_frames_fade2 = self.__get_halfword()
                code_insides = f"{OcarinaControlCode.FADE2.name}:{num_frames_fade2}"
            
            elif code == OcarinaControlCode.SOUND:
                sound_id = self.__get_halfword()
                code_insides = f"{OcarinaControlCode.SOUND.name}:{sound_id}"
            
            elif code == OcarinaControlCode.SPEED:
                speed = self.__get_byte()
                code_insides = f"{OcarinaControlCode.SPEED.name}:{speed}"
            
            elif code == OcarinaControlCode.HIGH_SCORE:
                score_id = self.__get_byte()
                code_insides = f"{OcarinaControlCode.HIGH_SCORE.name}:{OcarinaHighScore(score_id).name if hasattr(OcarinaHighScore, str(score_id)) else str(score_id)}"
            
            elif code == OcarinaControlCode.JUMP:
                msg_id = self.__get_halfword()
                code_insides = f"{OcarinaControlCode.JUMP.name}:{msg_id:04X}"
            
            elif code == OcarinaControlCode.NEW_BOX:
                return list(f"\n<{OcarinaControlCode.NEW_BOX.name}>\n")
            
            elif code == OcarinaControlCode.BACKGROUND:
                id1 = self.__get_byte()
                id2 = self.__get_byte()
                id3 = self.__get_byte()
                background_id = int.from_bytes([id3, id2, id1, 0], byteorder='little')
                code_insides = f"{OcarinaControlCode.BACKGROUND.name}:{background_id}"
            
            else:
                code_insides = code.name
        except:
                code_bank.extend(f"<UNK:{code}>")
                return code_bank

        code_bank.extend(f"<{code_insides}>")
        return code_bank       