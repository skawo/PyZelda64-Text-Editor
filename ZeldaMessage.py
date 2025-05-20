import struct
import string

from ZeldaEnums import *
from PyQt6 import QtGui, QtWidgets
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
        func = self.__GetControlCodeMajora if self.mode == MessageMode.Majora else self.__GetControlCode

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
    
    def __GetControlCodeMajora(self, code):
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

    def __GetControlCode(self, code):
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
    
    def ConvertToBytes(self):
        return self.__ConvertToBytesMajora() if self.mode == MessageMode.Majora else self.__ConvertToBytesOcarina()
    
    def __ConvertToBytesMajora(self):
        return []

    def __ConvertToBytesOcarina(self):
        data = []
        self.errors = []
        
        i = 0
        while i < len(self.textData):
            # Not a control code, copy char to output buffer
            if self.textData[i] != '<' and self.textData[i] != '>':
                try:
                    # Check if character is a valid control code
                    control_code = OcarinaControlCode[self.textData[i]]
                    data.append(control_code.value)
                except:
                    if self.textData[i] == '\n':
                        data.append(OcarinaControlCode.LINE_BREAK.value)
                    elif self.textData[i] == '\r':
                        # Do nothing
                        pass
                    else:
                        data.append(ord(self.textData[i]))
                
                i += 1
                continue
                
            # Control code end tag. This should never be encountered on its own.
            elif self.textData[i] == '>':
                self.errors.append("Message formatting is not valid: found stray >")
                i += 1
            # We've got a control code
            else:
                # Buffer for the control code
                control_code = []
                
                while i < len(self.textData) - 1 and self.textData[i] != '>':
                    # Add code chars to the buffer
                    control_code.append(self.textData[i])
                    # Increase i so we can skip the code when we're done parsing
                    i += 1
                    
                if not control_code:
                    i += 1
                    continue
                    
                # Remove the < chevron from the beginning of the code
                control_code.pop(0)
                
                parsed_code = ''.join(control_code)
                parsed_fixed = parsed_code.split(':')[0].replace(" ", "_").upper()
                
                if parsed_fixed in (OcarinaControlCode.NEW_BOX.name, OcarinaControlCode.DELAY.name):
                    if data and data[-1] == 0x01:
                        data.pop()
                        
                    if len(self.textData) > i + len('\n'):
                        if len('\n') == 2:  # Windows-style newline
                            s = self.textData[i + 1:i + 3]
                        else:
                            s = self.textData[i + 1]
                            
                        if s == '\n':
                            i += len('\n')  # Skips next linebreak
                
                control_code_bytes = self.__ConvertControlCodeOcarina(parsed_code.split(':'), self.errors)
                data.extend(control_code_bytes)
                i += 1
                
        data.append(OcarinaControlCode.END.value)
        
        #if show_errors and self.errors:
        #    QtWidgets.QMessageBox.information(self, 'Error', f"Errors parsing message {self.messageId}:\n" + "\n".join(errors))
        
        return data if not self.errors else []

    def __ConvertControlCodeOcarina(self, code, errors):
        output = []
        
        try:
            # Convert all codes to uppercase and replace spaces with underscores
            code = [c.replace(" ", "_").upper() for c in code]
            
            if code[0] == "PIXELS_RIGHT":
                output.append(OcarinaControlCode.SHIFT.value)
                output.append(int(code[1]))
                
            elif code[0] == "JUMP":
                output.append(OcarinaControlCode.JUMP.value)
                jump_id = int(code[1], 16)  # Parse hex number
                jump_bytes = struct.pack(">H", jump_id)  # Big endian short
                output.extend([jump_bytes[1], jump_bytes[0]])
                
            elif code[0] in ["DELAY", "FADE", "SHIFT", "SPEED"]:
                output.append(OcarinaControlCode[code[0]].value)
                output.append(int(code[1]))
                
            elif code[0] == "FADE2":
                output.append(OcarinaControlCode[code[0]].value)
                fade_amount = int(code[1])
                fade_bytes = struct.pack(">h", fade_amount)  # Big endian short
                output.extend([fade_bytes[1], fade_bytes[0]])
                
            elif code[0] == "ICON":
                output.append(OcarinaControlCode[code[0]].value)
                output.append(OcarinaIcon[code[1]].value)
                
            elif code[0] == "BACKGROUND":
                output.append(OcarinaControlCode.BACKGROUND.value)
                background_id = int(code[1])
                background_bytes = struct.pack(">I", background_id)  # Big endian int
                output.extend([background_bytes[2], background_bytes[1], background_bytes[0]])
                
            elif code[0] == "HIGH_SCORE":
                output.append(OcarinaControlCode.HIGH_SCORE.value)
                output.append(OcarinaHighScore[code[1]].value)
                
            elif code[0] == "SOUND":
                output.append(OcarinaControlCode.SOUND.value)
                sound_value = 0
                
                try:
                    sound_value = int(code[1])
                except ValueError:
                    errors.append(f"{code[1]} is not a valid sound.")
                    sound_value = 0
                
                sound_bytes = struct.pack(">h", sound_value)  # Big endian short
                output.extend([sound_bytes[1], sound_bytes[0]])
                
            else:
                try:
                    color_value = OcarinaMsgColor[code[0]].value
                    output.append(OcarinaControlCode.COLOR.value)
                    output.append(color_value)
                except KeyError:
                    try:
                        output.append(OcarinaControlCode[code[0]].value)
                    except KeyError:
                        errors.append(f"{code[0]} is not a valid control code.")
                        
        except Exception:
            pass
            
        return output

