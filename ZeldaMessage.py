import struct
import string

from ZeldaEnums import *
from io import BytesIO

def GetMessageList(tableData, stringData):
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

            message = Message(file, record)

            if (file.tell() - start_pos > MAX_MES_SIZE):
                return None

            messageList.append(message)

    return messageList

class TableRecord:
    def __init__(self, reader):

        self.messageId = struct.unpack('>h', reader.read(2))[0] & 0xFFFF
        
        typePos = reader.read(1)[0]
        
        self.boxType = OcarinaTextboxType((typePos & 0xF0) >> 4)
        self.boxPosition = TextboxPosition(typePos & 0x0F)
    
        reader.read(1)
        self.offset = struct.unpack('>I', reader.read(4))[0] & 0x00FFFFFF


class Message:
    def __init__(self, reader, record):
        self.messageId = record.messageId & 0xFFFF
        self.boxType = record.boxType
        self.boxPosition = record.boxPosition

        self.textData = self.GetStringData(reader)

    def GetStringData(self, reader):
        char_data = []
        cur_byte = int.from_bytes(reader.read(1))

        while cur_byte != OcarinaControlCode.END:
            read_control_code = False

            if cur_byte < 0x7F or cur_byte > 0x9E:
                if (cur_byte in OcarinaControlCode):
                    char_data.extend(self.GetControlCode(OcarinaControlCode(cur_byte), reader))
                    read_control_code = True

            if not read_control_code:
                if cur_byte == 0x7F:
                    # Never actually used in-game. Appears blank.
                    char_data.append(' ')
                # Stressed characters
                elif 0x80 <= cur_byte <= 0x9E:
                    char_data.append(OcarinaControlCode(cur_byte).name[0])
                # ASCII-mapped characters
                elif ((0x20 <= cur_byte < 0x7F) or 
                    chr(cur_byte).isalnum() or 
                    chr(cur_byte).isspace() or 
                    chr(cur_byte) in string.punctuation):
                    char_data.append(chr(cur_byte))
                else:
                    char_data.extend(f"<UNK {cur_byte:X}>")

            if reader.tell() != len(reader.getvalue()):
                cur_byte = int.from_bytes(reader.read(1))
            else:
                cur_byte = 0x02

        return ''.join(char_data)

    def GetControlCode(self, code, reader):
        code_bank = []
        code_insides = ""

        try:
            if code == OcarinaControlCode.COLOR:
                color = OcarinaMsgColor(int.from_bytes(reader.read(1)))
                code_insides = color.name
            
            elif code == OcarinaControlCode.ICON:
                icon_id = int.from_bytes(reader.read(1))
                code_insides = f"{OcarinaControlCode.ICON.name}:{OcarinaIcon(icon_id).name if hasattr(OcarinaIcon, str(icon_id)) else str(icon_id)}"
            
            elif code == OcarinaControlCode.LINE_BREAK:
                return list("\n")
            
            elif code == OcarinaControlCode.SHIFT:
                num_spaces = int.from_bytes(reader.read(1))
                code_insides = f"{OcarinaControlCode.SHIFT.name}:{num_spaces}"
            
            elif code == OcarinaControlCode.DELAY:
                num_frames = int.from_bytes(reader.read(1))
                code_insides = f"{OcarinaControlCode.DELAY.name}:{num_frames}"
            
            elif code == OcarinaControlCode.FADE:
                num_frames_fade = int.from_bytes(reader.read(1))
                code_insides = f"{OcarinaControlCode.FADE.name}:{num_frames_fade}"
            
            elif code == OcarinaControlCode.FADE2:
                num_frames_fade2 = struct.unpack('>h', reader.read(2))[0]
                code_insides = f"{OcarinaControlCode.FADE2.name}:{num_frames_fade2}"
            
            elif code == OcarinaControlCode.SOUND:
                sound_id = int.from_bytes(reader.read(1))
                code_insides = f"{OcarinaControlCode.SOUND.name}:{sound_id}"
            
            elif code == OcarinaControlCode.SPEED:
                speed = int.from_bytes(reader.read(1))
                code_insides = f"{OcarinaControlCode.SPEED.name}:{speed}"
            
            elif code == OcarinaControlCode.HIGH_SCORE:
                score_id = int.from_bytes(reader.read(1))
                code_insides = f"{OcarinaControlCode.HIGH_SCORE.name}:{OcarinaHighScore(score_id).name if hasattr(OcarinaHighScore, str(score_id)) else str(score_id)}"
            
            elif code == OcarinaControlCode.JUMP:
                msg_id = struct.unpack('>h', reader.read(2))[0]
                code_insides = f"{OcarinaControlCode.JUMP.name}:{msg_id:04X}"
            
            elif code == OcarinaControlCode.NEW_BOX:
                return list(f"\n<{OcarinaControlCode.NEW_BOX.name}>\n")
            
            elif code == OcarinaControlCode.BACKGROUND:
                id1 = int.from_bytes(reader.read(1))
                id2 = int.from_bytes(reader.read(1))
                id3 = int.from_bytes(reader.read(1))
                background_id = int.from_bytes([id3, id2, id1, 0], byteorder='little')
                code_insides = f"{OcarinaControlCode.BACKGROUND.name}:{background_id}"
            
            else:
                code_insides = code.name
        except:
                code_bank.extend(f"<UNK:{code}>")
                return code_bank

        code_bank.extend(f"<{code_insides}>")
        return code_bank       