import struct
import string

from zeldaEnums import *
from zeldaDicts import *
from io import BytesIO
from PyQt6 import  QtGui, QtWidgets

def getMessageList(tableData, stringData, mode):
    messageRecordList = []
    messageList = []

    with BytesIO(tableData) as tableReader, BytesIO(stringData) as stringReader:
        while True:
            peek_bytes = tableReader.read(2)
            if not peek_bytes or struct.unpack('>H', peek_bytes)[0] == 0xFFFF:
                tableReader.seek(-2, 1)
                break
                
            tableReader.seek(-2, 1)
            record = TableRecord(tableReader, mode)
            
            if any(x.messageId == record.messageId for x in messageRecordList):
                return None
            
            if record.offset >= len(stringData): 
                continue
                
            stringReader.seek(record.offset)
            start_pos = stringReader.tell()

            if mode == MessageMode.Majora:
                mes = MessageMajora(stringReader, record, mode)
            else:
                mes = MessageOcarina(stringReader, record, mode)

            if stringReader.tell() - start_pos >= MAX_MES_SIZE:
                return None

            messageList.append(mes)
            
    return messageList

def convertMessageList(messagelist, mode, progress_callback=None):
    records = []
    strings = []
    padding = 0

    offset = 0x08000000 if mode == MessageMode.Majora else 0x07000000

    numMes = len(messagelist)
    processedNum = 0

    for mes in messagelist:

        if mode == MessageMode.Majora:
            records.append(mes.messageId.to_bytes(2, 'big'))
            records.append(padding.to_bytes(2, 'big'))
            records.append(offset.to_bytes(4, 'big'))
        else:
            typePos = (mes.boxType << 4) | mes.boxPosition
            records.append(mes.messageId.to_bytes(2, 'big'))
            records.append(typePos.to_bytes(1, 'big'))
            records.append(padding.to_bytes(1, 'big'))
            records.append(offset.to_bytes(4, 'big'))

        stringData = mes.save()

        if stringData is None:
            return (1, mes.messageId, mes.errors)

        totalLen = len(stringData)
        paddingNeeded = (4 - (totalLen % 4)) % 4

        if paddingNeeded > 0:
            stringData += b'\x00' * paddingNeeded
        
        strings.append(stringData)
        offset += totalLen + paddingNeeded

        if progress_callback:
            processedNum += 1
            progress_callback(processedNum, numMes)

    records.append(b'\xFF' * 2)
    records.append(b'\x00' * 6)

    # Pad strings to be divisible by 16
    totalStringsLen = sum(len(string) for string in strings)
    stringsPaddingNeeded = (16 - (totalStringsLen % 16)) % 16
    if stringsPaddingNeeded > 0:
        strings.append(b'\x00' * stringsPaddingNeeded)

    return (0, b''.join(records), b''.join(strings))


def formatMessageID(messageId):
    return f'0x{messageId & 0xFFFF:04X}'

class TableRecord:
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
        
        self.boxType = MajoraTextboxType(typePos >> 4) if self.mode == MessageMode.Majora else OcarinaTextboxType(typePos >> 4)
        self.boxPosition = TextboxPosition(typePos & 0x0F)
    
        reader.read(1)
        self.offset = struct.unpack('>I', reader.read(4))[0] & 0x00FFFFFF

class Message:
    def __init__(self, reader, record, mode):
        self.mode = mode
        self.reader = reader
        self.record = record
        self.messageId = 0
        self.boxType = 0
        self.boxPosition = 0
        self.textData = ""

    def _get_u8(self):
        return self.reader.read(1)[0]
    
    def _get_u16(self):
        return struct.unpack('>H', self.reader.read(2))[0]
    
    def _get_u32(self):
        return struct.unpack('>I', self.reader.read(4))[0]
    
    def _get_s16(self):
        return struct.unpack('>h', self.reader.read(2))[0]
    
    def _get_s32(self):
        return struct.unpack('>i', self.reader.read(4))[0]  

class MessageOcarina(Message):
    def __init__(self, reader, record, mode):

        super().__init__(reader, record, mode)

        if self.reader is not None and self.record is not None:
            self.messageId = record.messageId & 0xFFFF
            self.boxType = record.boxType
            self.boxPosition = record.boxPosition
            self.textData = self._getStringData()
        
        del self.reader 
        del self.record

    def _getStringData(self):
        char_data = []
        cur_byte = self._get_u8()

        while cur_byte != OcarinaControlCode.END:
            read_control_code = False

            if cur_byte < 0x7F or cur_byte > 0x9E:
                if cur_byte in OcarinaControlCode:
                    char_data.extend(self._getControlCode(OcarinaControlCode(cur_byte)))
                    read_control_code = True

            if not read_control_code:
                # Never actually used in-game. Appears blank.
                if cur_byte == 0x7F:
                    char_data.append(' ')
                # Stressed characters
                elif 0x80 <= cur_byte <= 0x9E:
                    char_data.append(OcarinaControlCode(cur_byte).name[0])
                # ASCII-mapped characters
                elif (
                    (0x20 <= cur_byte < 0x7F)
                    or chr(cur_byte).isalnum()
                    or chr(cur_byte).isspace()
                    or chr(cur_byte) in string.punctuation
                ):
                    char_data.append(chr(cur_byte))
                else:
                    char_data.extend(f"<UNK {cur_byte:X}>")

            if self.reader.tell() != len(self.reader.getvalue()):
                cur_byte = self._get_u8()
            else:
                cur_byte = OcarinaControlCode.END

        return ''.join(char_data)
    
    def _getControlCode(self, code):
        code_bank = []
        code_insides = ""

        try:
            if code == OcarinaControlCode.COLOR:
                color = OcarinaMsgColor(self._get_u8())
                code_insides = color.name
            
            elif code == OcarinaControlCode.ICON:
                icon_id = self._get_u8()

                try: icon_name = OcarinaIcon(icon_id).name
                except: icon_name = str(icon_id)

                code_insides = f"{OcarinaControlCode.ICON.name}:{icon_name}"
            
            elif code == OcarinaControlCode.LINE_BREAK:
                return list("\n")
            
            elif code == OcarinaControlCode.SHIFT:
                num_spaces = self._get_u8()
                code_insides = f"{OcarinaControlCode.SHIFT.name}:{num_spaces}"
            
            elif code == OcarinaControlCode.DELAY:
                num_frames = self._get_u8()
                code_insides = f"{OcarinaControlCode.DELAY.name}:{num_frames}"
            
            elif code == OcarinaControlCode.FADE:
                num_frames_fade = self._get_u8()
                code_insides = f"{OcarinaControlCode.FADE.name}:{num_frames_fade}"
            
            elif code == OcarinaControlCode.FADE2:
                num_frames_fade2 = self._get_u16()
                code_insides = f"{OcarinaControlCode.FADE2.name}:{num_frames_fade2}"
            
            elif code == OcarinaControlCode.SOUND:
                sound_id = self._get_u16()
                sound_name = sfxOcarina.get(sound_id)

                if sound_name:
                    code_insides = f"{OcarinaControlCode.SOUND.name}:{sound_name[0]}"
                else:
                    code_insides = f"{OcarinaControlCode.SOUND.name}:{sound_id}"
            
            elif code == OcarinaControlCode.SPEED:
                speed = self._get_u8()
                code_insides = f"{OcarinaControlCode.SPEED.name}:{speed}"
            
            elif code == OcarinaControlCode.HIGH_SCORE:
                score_id = self._get_u8()

                try: score_name = OcarinaHighScore(score_id).name
                except: score_name = str(score_id)

                code_insides = f"{OcarinaControlCode.HIGH_SCORE.name}:{score_name}"
            
            elif code == OcarinaControlCode.JUMP:
                msg_id = self._get_u16()
                code_insides = f"{OcarinaControlCode.JUMP.name}:{msg_id:04X}"
            
            elif code == OcarinaControlCode.NEW_BOX:
                return list(f"\n<{OcarinaControlCode.NEW_BOX.name}>\n")
            
            elif code == OcarinaControlCode.BACKGROUND:
                id1 = self._get_u8()
                id2 = self._get_u8()
                id3 = self._get_u8()

                background_id = (id1 << 16) | (id2 << 8) | id3
                code_insides = f"{OcarinaControlCode.BACKGROUND.name}:{background_id}"
            
            else:
                code_insides = code.name
        except Exception:
                code_bank.extend(f"<UNK:{code}>")
                return code_bank

        code_bank.extend(f"<{code_insides}>")
        return code_bank       
    
    def save(self):
        data = bytearray()
        self.errors = []
        
        i = 0
        while i < len(self.textData):
            # Not a control code, copy char to output buffer
            if self.textData[i] not in '<>':
                try:
                    # Check if character is a valid control code
                    controlCode = OcarinaControlCode[self.textData[i]]
                    data.append(controlCode.value)
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
                controlCode = []
                
                while i < len(self.textData) - 1 and self.textData[i] != '>':
                    # Add code chars to the buffer
                    controlCode.append(self.textData[i])
                    # Increase i so we can skip the code when we're done parsing
                    i += 1
                    
                if not controlCode:
                    i += 1
                    continue
                    
                # Remove the < chevron from the beginning of the code
                controlCode.pop(0)
                
                parsedCode = ''.join(controlCode)
                parsedFixed = parsedCode.split(':')[0].replace(" ", "_").upper()
                
                if parsedFixed in (OcarinaControlCode.NEW_BOX.name, OcarinaControlCode.DELAY.name):
                    if data and data[-1] == 0x01:
                        data.pop()
                        
                    if len(self.textData) > i + len('\n'):
                        s = self.textData[i + 1]
                            
                        if s == '\n':
                            i += len('\n')  # Skips next linebreak
                
                controlCodeBytes = self._convertControlCode(parsedCode.split(':'), self.errors)
                data.extend(controlCodeBytes)
                i += 1
                
        data.append(OcarinaControlCode.END.value)

        return bytes(data) if not self.errors else None

    def _convertControlCode(self, code, errors):
        output = []
        
        try:
            # Convert all codes to uppercase and replace spaces with underscores
            code = [c.replace(" ", "_").upper() for c in code]
            
            if code[0] == "PIXELS_RIGHT":
                output.append(OcarinaControlCode.SHIFT.value)
                output.append(int(code[1]))
                
            elif code[0] == "JUMP":
                output.append(OcarinaControlCode.JUMP.value)
                jumpId = int(code[1], 16) 
                jumpBytes = struct.pack(">H", jumpId)  
                output.extend(jumpBytes)
                
            elif code[0] in ["DELAY", "FADE", "SHIFT", "SPEED"]:
                output.append(OcarinaControlCode[code[0]].value)
                output.append(int(code[1]))
                
            elif code[0] == "FADE2":
                output.append(OcarinaControlCode[code[0]].value)
                fade_amount = int(code[1])
                fadeBytes = struct.pack(">h", fade_amount) 
                output.extend(fadeBytes)
                
            elif code[0] == "ICON":
                output.append(OcarinaControlCode[code[0]].value)
                output.append(OcarinaIcon[code[1]].value)
                
            elif code[0] == "BACKGROUND":
                output.append(OcarinaControlCode.BACKGROUND.value)
                backgroundId = int(code[1])
                backgroundBytes = struct.pack(">I", backgroundId) 
                output.extend(backgroundBytes[1:])
                
            elif code[0] == "HIGH_SCORE":
                output.append(OcarinaControlCode.HIGH_SCORE.value)
                output.append(OcarinaHighScore[code[1]].value)
                
            elif code[0] == "SOUND":
                output.append(OcarinaControlCode.SOUND.value)
                soundValue = findSFXByname(sfxOcarina, code[1])

                if soundValue == None:
                    try:
                        soundValue = int(code[1])
                    except ValueError:
                        errors.append(f"{code[1]} is not a valid sound.")
                        soundValue = 0
                
                output.extend(struct.pack(">H", soundValue))
                
            else:
                try:
                    colorValue = OcarinaMsgColor[code[0]].value
                    output.append(OcarinaControlCode.COLOR.value)
                    output.append(colorValue)
                except KeyError:
                    try:
                        output.append(OcarinaControlCode[code[0]].value)
                    except KeyError:
                        errors.append(f"{code[0]} is not a valid control code.")
                        
        except Exception:
            pass
            
        return output

class MessageMajora(Message):
    
    def __init__(self, reader, record, mode):

        super().__init__(reader, record, mode)

        if self.reader is None or self.record is None:
            self.majoraIcon = 0
            self.majoraJumpTo = 0
            self.majoraFirstPrice = 0
            self.majoraSecondPrice = 0
        else:
            self.reader = reader
            self.messageId = record.messageId & 0xFFFF
            self.boxType = self._get_u8()
            self.boxPosition = self._get_u8() 
            self.majoraIcon = self._get_u8()
            self.majoraJumpTo = self._get_u16()
            self.majoraFirstPrice = self._get_s16()
            self.majoraSecondPrice = self._get_s16()
            self._get_u16() # Padding
            self.textData = self._getStringData()

        del self.reader 
        del self.record 

    def _getStringData(self):
        char_data = []
        cur_byte = self._get_u8()

        while cur_byte != MajoraControlCode.END:
            read_control_code = False

            if cur_byte < 0x7F or cur_byte > 0xAF:
                if cur_byte in MajoraControlCode:
                    char_data.extend(self._getControlCode(MajoraControlCode(cur_byte)))
                    read_control_code = True

            if not read_control_code:
                # Never actually used in-game. Appears blank.
                if cur_byte == 0x7F:
                    char_data.append(' ')
                # Stressed characters
                elif 0x80 <= cur_byte <= 0xAF:
                    if cur_byte == '¡':
                        char_data.append(0xAD)
                    elif cur_byte == '¿':
                        char_data.append(0xAE)
                    elif cur_byte == 'ª':
                        char_data.append(0xAF)
                    else:
                        char_data.append(MajoraControlCode(cur_byte).name[0])
                # ASCII-mapped characters
                elif (
                    (0x20 <= cur_byte < 0x7F)
                    or chr(cur_byte).isalnum()
                    or chr(cur_byte).isspace()
                    or chr(cur_byte) in string.punctuation
                ):
                    char_data.append(chr(cur_byte))
                else:
                    char_data.extend(f"<UNK {cur_byte:X}>")

            if self.reader.tell() != len(self.reader.getvalue()):
                cur_byte = self._get_u8()
            else:
                cur_byte = MajoraControlCode.END

        return ''.join(char_data)
    
    def _getControlCode(self, code):
        code_bank = []
        code_insides = ""

        try:
            if code in [
                MajoraControlCode.COLOR_DEFAULT,
                MajoraControlCode.COLOR_RED,
                MajoraControlCode.COLOR_GREEN,
                MajoraControlCode.COLOR_BLUE,
                MajoraControlCode.COLOR_YELLOW,
                MajoraControlCode.COLOR_NAVY,
                MajoraControlCode.COLOR_PINK,
                MajoraControlCode.COLOR_SILVER,
                MajoraControlCode.COLOR_ORANGE,
            ]:
                code_insides = MajoraMsgColor(code.value).name

            elif code == MajoraControlCode.SHIFT:
                num_spaces = self._get_u8()
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
                MajoraControlCode.FADE,
            ]:
                delay = self._get_u16()
                code_insides = f"{code.name}:{delay}"

            elif code == MajoraControlCode.SOUND:
                sound_id = self._get_u16()
                sound_name = sfxMajora.get(sound_id)

                if sound_name:
                    code_insides = f"{MajoraControlCode.SOUND.name}:{sound_name[0]}"
                else:
                    code_insides = f"{MajoraControlCode.SOUND.name}:{sound_id}"

            else:
                code_insides = code.name
        except Exception:
                code_bank.extend(f"<UNK:{code}>")
                return code_bank
        
        code_bank.extend(f"<{code_insides}>")
        return code_bank

    def save(self):
        data = bytearray()
        self.errors = []

        # Add initial data
        data.append(self.boxType)
        data.append(self.boxPosition)
        data.append(self.majoraIcon)

        data.extend(struct.pack('>H', self.majoraJumpTo))
        data.extend(struct.pack('>h', self.majoraFirstPrice))
        data.extend(struct.pack('>h', self.majoraSecondPrice))

        data.extend([0xFF, 0xFF])

        i = 0
        while i < len(self.textData):
            # Not a control code, copy char to output buffer
            if self.textData[i] not in '<>':
                try:
                    data.append(MajoraControlCode[self.textData[i]].value)
                except:
                    if self.textData[i] == '¡':
                        data.append(0xAD)
                    elif self.textData[i] == '¿':
                        data.append(0xAE)
                    elif self.textData[i] == 'ª':
                        data.append(0xAF)
                    elif self.textData[i] == '\n':
                        data.append(MajoraControlCode.LINE_BREAK.value)
                    elif self.textData[i] != '\r':
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
                controlCode = []
                
                while i < len(self.textData) - 1 and self.textData[i] != '>':
                    # Add code chars to the buffer
                    controlCode.append(self.textData[i])
                    # Increase i so we can skip the code when we're done parsing
                    i += 1
                    
                if not controlCode:
                    i += 1
                    continue
                    
                # Remove the < chevron from the beginning of the code
                controlCode.pop(0)
                
                parsedCode = ''.join(controlCode)
                pasedFixed = parsedCode.split(':')[0].replace(" ", "_").upper()
                
                if pasedFixed in [
                    MajoraControlCode.NEW_BOX.name, 
                    MajoraControlCode.DELAY_END.name,
                    MajoraControlCode.NEW_BOX_CENTER.name         
                    ]:
                    if data and data[-1] == 0x11:
                        data.pop()
                        
                    if len(self.textData) > i + len('\n'):
                        s = self.textData[i + 1]

                        if s == '\n':
                            i += len('\n')
                
                controlCodeBytes = self._convertControlCode(parsedCode.split(':'), self.errors)
                data.extend(controlCodeBytes)
                i += 1
                
        data.append(MajoraControlCode.END.value)
        
        return bytes(data) if not self.errors else None

    def _convertControlCode(self, code, errors):
        output = []

        try:
            # Convert all codes to uppercase and replace spaces with underscores
            code = [c.replace(" ", "_").upper() for c in code]

            if code[0] == "SHIFT":
                output.append(MajoraControlCode.SHIFT.value)
                output.append(int(code[1]))

            elif code[0] in ["DELAY", "DELAY_NEWBOX", "DELAY_END", "FADE"]:
                output.append(MajoraControlCode[code[0]].value)
                output.extend(struct.pack('>H', int(code[1])))

            elif code[0] == "SOUND":
                output.append(MajoraControlCode.SOUND.value)
                soundValue = findSFXByname(sfxMajora, code[1])

                if soundValue == None:
                    try:
                        soundValue = int(code[1])
                    except ValueError:
                        errors.append(f"{code[1]} is not a valid sound.")
                        soundValue = 0

                output.extend(struct.pack('>H', soundValue))

            else:
                try:
                    output.append(MajoraMsgColor[code[0]].value)
                except KeyError:
                    try:
                        output.append(MajoraControlCode[code[0]].value)
                    except KeyError:
                        errors.append(f"{code[0]} is not a valid control code.")

        except Exception:
            pass

        return output
