import struct
import string

from zeldaEnums import *
from PyQt6 import QtGui, QtWidgets
from io import BytesIO

def getMessageList(tableData, stringData, mode):
    messageRecordList = []
    messageList = []

    with BytesIO(tableData) as file:
        while True:
            peek_bytes = file.read(2)
            if not peek_bytes or struct.unpack('>h', peek_bytes)[0] == -1:
                file.seek(-2, 1)
                break
                
            file.seek(-2, 1)
            record = tableRecord(file, mode)
            
            if any(x.messageId == record.messageId for x in messageRecordList):
                return None
                
            messageRecordList.append(record)

    with BytesIO(stringData) as file:
        for record in messageRecordList:
            if record.offset >= len(stringData):      
                continue     

            file.seek(record.offset)    
            start_pos = file.tell()

            mes = message(file, record, mode)

            if (file.tell() - start_pos > MAX_MES_SIZE):
                return None

            messageList.append(mes)

    return messageList

def convertMessageList(messagelist, mode):
    records = []
    strings = []
    padding = 0

    offset = 0x08000000 if mode == messageMode.Majora else 0x07000000

    for mes in messagelist:

        if mode == messageMode.Majora:
            return (None, None)
        else:
            typePos = mes.boxType
            typePos <<= 4
            typePos |= mes.boxPosition

            records.append(mes.messageId.to_bytes(2, 'big'))
            records.append(typePos.to_bytes(1, 'big'))
            records.append(padding.to_bytes(1, 'big'))
            records.append(offset.to_bytes(4, 'big'))

            stringD = bytes(mes.convertToBytes())
            total_length = len(stringD)
            padding_needed = (4 - (total_length % 4)) % 4
        
            if padding_needed > 0:
                stringD = stringD + bytes([0] * padding_needed)
            
            strings.append(stringD)
            offset += total_length + padding_needed

    records.append(bytes([0xFF] * 2))
    records.append(bytes([0] * 6))

    # Pad strings to be divisible by 16
    total_strings_length = sum(len(string) for string in strings)
    strings_padding_needed = (16 - (total_strings_length % 16)) % 16
    if strings_padding_needed > 0:
        strings.append(bytes([0] * strings_padding_needed))

    return (b''.join(records), b''.join(strings))


def formatMessageID(messageId):
    return '0x' + format(messageId & 0xFFFF, '04X')

class tableRecord:
    def __init__(self, reader, mode):

        self.mode = mode

        if reader is None:
            self.messageId = 0
            self.boxType = 0
            self.boxPosition = 0
            self.offset = 0
            return
            
        self.messageId = struct.unpack('>h', reader.read(2))[0] & 0xFFFF
        
        typePos = reader.read(1)[0]
        
        self.boxType = ocarinaTextboxType((typePos & 0xF0) >> 4)
        self.boxPosition = textboxPosition(typePos & 0x0F)
    
        reader.read(1)
        self.offset = struct.unpack('>I', reader.read(4))[0] & 0x00FFFFFF

class message:
    def __init__(self, reader, record, mode):

        self.mode = mode

        if reader is None or record is None:
            self.messageId = 0
            self.boxType = 0
            self.boxPosition = 0
            self.textData = ""

            if mode == messageMode.Majora:
                self.majoraIcon = 0
                self.majoraJumpTo = 0
                self.majoraFirstPrice = 0
                self.majoraSecondPrice = 0
            return

        self.reader = reader

        if mode == messageMode.Majora:
            self.messageId = record.messageId & 0xFFFF
            self.boxType = self._get_byte()
            self.boxPosition = self._get_byte() 
            self.majoraIcon = self._get_byte()
            self.majoraJumpTo = self._get_halfword()
            self.majoraFirstPrice = self._get_halfword()
            self.majoraSecondPrice = self._get_halfword()
            self._get_halfword() # Padding
        else:
            self.messageId = record.messageId & 0xFFFF
            self.boxType = record.boxType
            self.boxPosition = record.boxPosition

        self.textData = self._getStringData()

    def _get_byte(self):
        return int.from_bytes(self.reader.read(1))
    
    def _get_halfword(self):
        return struct.unpack('>h', self.reader.read(2))[0]
    
    def _get_word(self):
        return struct.unpack('>w', self.reader.read(4))[0]

    def _getStringData(self):
        char_data = []
        cur_byte = self._get_byte()

        controlCodeType = majoraControlCode if self.mode == messageMode.Majora else ocarinaControlCode
        func = self._getControlCodeMajora if self.mode == messageMode.Majora else self._getControlCode

        boundByte = 0xAF if self.mode == messageMode.Majora else 0x9E

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
                cur_byte = self._get_byte()
            else:
                cur_byte = controlCodeType.END

        return ''.join(char_data)
    
    def _getControlCodeMajora(self, code):
        code_bank = []
        code_insides = ""

        if code in [
            majoraControlCode.COLOR_DEFAULT,
            majoraControlCode.COLOR_RED,
            majoraControlCode.COLOR_GREEN,
            majoraControlCode.COLOR_BLUE,
            majoraControlCode.COLOR_YELLOW,
            majoraControlCode.COLOR_NAVY,
            majoraControlCode.COLOR_PINK,
            majoraControlCode.COLOR_SILVER,
            majoraControlCode.COLOR_ORANGE
        ]:
            code_insides = majoraMsgColor(code.value).name

        elif code == majoraControlCode.SHIFT:
            num_spaces = self._get_byte()
            code_insides = f"{majoraControlCode.SHIFT}:{num_spaces}"

        elif code == majoraControlCode.LINE_BREAK:
            return list("\n")

        elif code == majoraControlCode.NEW_BOX:
            return list(f"\n<{majoraControlCode.NEW_BOX.name}>\n")

        elif code == majoraControlCode.NEW_BOX_CENTER:
            return list(f"\n<{majoraControlCode.NEW_BOX_CENTER.name}>\n")

        elif code in [
            majoraControlCode.DELAY,
            majoraControlCode.DELAY_NEWBOX,
            majoraControlCode.DELAY_END,
            majoraControlCode.FADE
        ]:
            delay = self._get_halfword()
            code_insides = f"{code.name}:{delay}"

        elif code == majoraControlCode.SOUND:
            sound_id = self._get_halfword()
            code_insides = f"{ocarinaControlCode.SOUND.name}:{sound_id}"

        else:
            code_insides = code.name

        code_bank.extend(f"<{code_insides}>")
        return code_bank

    def _getControlCode(self, code):
        code_bank = []
        code_insides = ""

        try:
            if code == ocarinaControlCode.COLOR:
                color = ocarinaMsgColor(self._get_byte())
                code_insides = color.name
            
            elif code == ocarinaControlCode.ICON:
                icon_id = self._get_byte()

                try: icon_name = ocarinaIcon(icon_id).name
                except: icon_name = str(icon_id)

                code_insides = f"{ocarinaControlCode.ICON.name}:{icon_name}"
            
            elif code == ocarinaControlCode.LINE_BREAK:
                return list("\n")
            
            elif code == ocarinaControlCode.SHIFT:
                num_spaces = self._get_byte()
                code_insides = f"{ocarinaControlCode.SHIFT.name}:{num_spaces}"
            
            elif code == ocarinaControlCode.DELAY:
                num_frames = self._get_byte()
                code_insides = f"{ocarinaControlCode.DELAY.name}:{num_frames}"
            
            elif code == ocarinaControlCode.FADE:
                num_frames_fade = self._get_byte()
                code_insides = f"{ocarinaControlCode.FADE.name}:{num_frames_fade}"
            
            elif code == ocarinaControlCode.FADE2:
                num_frames_fade2 = self._get_halfword()
                code_insides = f"{ocarinaControlCode.FADE2.name}:{num_frames_fade2}"
            
            elif code == ocarinaControlCode.SOUND:
                sound_id = self._get_halfword()
                code_insides = f"{ocarinaControlCode.SOUND.name}:{sound_id}"
            
            elif code == ocarinaControlCode.SPEED:
                speed = self._get_byte()
                code_insides = f"{ocarinaControlCode.SPEED.name}:{speed}"
            
            elif code == ocarinaControlCode.HIGH_SCORE:
                score_id = self._get_byte()

                try: score_name = ocarinaHighScore(score_id).name
                except: score_name = str(score_id)

                code_insides = f"{ocarinaControlCode.HIGH_SCORE.name}:{score_name}"
            
            elif code == ocarinaControlCode.JUMP:
                msg_id = self._get_halfword()
                code_insides = f"{ocarinaControlCode.JUMP.name}:{msg_id:04X}"
            
            elif code == ocarinaControlCode.NEW_BOX:
                return list(f"\n<{ocarinaControlCode.NEW_BOX.name}>\n")
            
            elif code == ocarinaControlCode.BACKGROUND:
                id1 = self._get_byte()
                id2 = self._get_byte()
                id3 = self._get_byte()
                background_id = int.from_bytes([id3, id2, id1, 0], byteorder='little')
                code_insides = f"{ocarinaControlCode.BACKGROUND.name}:{background_id}"
            
            else:
                code_insides = code.name
        except:
                code_bank.extend(f"<UNK:{code}>")
                return code_bank

        code_bank.extend(f"<{code_insides}>")
        return code_bank       
    
    def convertToBytes(self):
        return self._convertToBytesMajora() if self.mode == messageMode.Majora else self._convertToBytesOcarina()
    
    def _convertToBytesMajora(self):
        return []

    def _convertToBytesOcarina(self):
        data = []
        self.errors = []
        
        i = 0
        while i < len(self.textData):
            # Not a control code, copy char to output buffer
            if self.textData[i] != '<' and self.textData[i] != '>':
                try:
                    # Check if character is a valid control code
                    control_code = ocarinaControlCode[self.textData[i]]
                    data.append(control_code.value)
                except:
                    if self.textData[i] == '\n':
                        data.append(ocarinaControlCode.LINE_BREAK.value)
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
                
                if parsed_fixed in (ocarinaControlCode.NEW_BOX.name, ocarinaControlCode.DELAY.name):
                    if data and data[-1] == 0x01:
                        data.pop()
                        
                    if len(self.textData) > i + len('\n'):
                        if len('\n') == 2:  # Windows-style newline
                            s = self.textData[i + 1:i + 3]
                        else:
                            s = self.textData[i + 1]
                            
                        if s == '\n':
                            i += len('\n')  # Skips next linebreak
                
                control_code_bytes = self._convertControlCodeOcarina(parsed_code.split(':'), self.errors)
                data.extend(control_code_bytes)
                i += 1
                
        data.append(ocarinaControlCode.END.value)
        
        #if show_errors and self.errors:
        #    QtWidgets.QMessageBox.information(self, 'Error', f"Errors parsing message {self.messageId}:\n" + "\n".join(errors))
        
        return data if not self.errors else []

    def _convertControlCodeOcarina(self, code, errors):
        output = []
        
        try:
            # Convert all codes to uppercase and replace spaces with underscores
            code = [c.replace(" ", "_").upper() for c in code]
            
            if code[0] == "PIXELS_RIGHT":
                output.append(ocarinaControlCode.SHIFT.value)
                output.append(int(code[1]))
                
            elif code[0] == "JUMP":
                output.append(ocarinaControlCode.JUMP.value)
                jump_id = int(code[1], 16) 
                jump_bytes = struct.pack(">H", jump_id)  
                output.extend([jump_bytes[0], jump_bytes[1]])
                
            elif code[0] in ["DELAY", "FADE", "SHIFT", "SPEED"]:
                output.append(ocarinaControlCode[code[0]].value)
                output.append(int(code[1]))
                
            elif code[0] == "FADE2":
                output.append(ocarinaControlCode[code[0]].value)
                fade_amount = int(code[1])
                fade_bytes = struct.pack(">h", fade_amount) 
                output.extend([fade_bytes[0], fade_bytes[1]])
                
            elif code[0] == "ICON":
                output.append(ocarinaControlCode[code[0]].value)
                output.append(ocarinaIcon[code[1]].value)
                
            elif code[0] == "BACKGROUND":
                output.append(ocarinaControlCode.BACKGROUND.value)
                background_id = int(code[1])
                background_bytes = struct.pack(">I", background_id) 
                output.extend([background_bytes[1], background_bytes[2], background_bytes[3]])
                
            elif code[0] == "HIGH_SCORE":
                output.append(ocarinaControlCode.HIGH_SCORE.value)
                output.append(ocarinaHighScore[code[1]].value)
                
            elif code[0] == "SOUND":
                output.append(ocarinaControlCode.SOUND.value)
                sound_value = 0
                
                try:
                    sound_value = int(code[1])
                except ValueError:
                    errors.append(f"{code[1]} is not a valid sound.")
                    sound_value = 0
                
                sound_bytes = struct.pack(">h", sound_value) 
                output.extend([sound_bytes[0], sound_bytes[1]])
                
            else:
                try:
                    color_value = ocarinaMsgColor[code[0]].value
                    output.append(ocarinaControlCode.COLOR.value)
                    output.append(color_value)
                except KeyError:
                    try:
                        output.append(ocarinaControlCode[code[0]].value)
                    except KeyError:
                        errors.append(f"{code[0]} is not a valid control code.")
                        
        except Exception:
            pass
            
        return output

