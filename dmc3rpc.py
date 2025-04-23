#Program was developed by rostikq


from ReadWriteMemory import ReadWriteMemory
import time
from pypresence import Presence

#Set up the program
rwm = ReadWriteMemory()
process = rwm.get_process_by_name('dmc3.exe')
process.open()

#Set up the DiscordRPC
app_id = 1364618966223421460
RPC = Presence(app_id)
RPC.connect()
rpcTime = int(time.time())

#Cooldown settings
cooldown = 0.5

#Mission settings
mission_address = 0x006E1904
mission_offsets = [0x0]
mission_info = ""
mission_ingame = 0


#Difficulty settings
difficulty_address = process.get_base_address() + 0xC8F25C
difficulty_hoh_address = process.get_base_address() + 0xC8F260 

difficulty_offsets = [0x0]
difficulty_list = ["Easy", "Normal", "Hard", "Very Hard", "Dante Must Die", "Heaven or Hell"]
difficulty_info = ""

#Character settings
character_address = process.get_base_address() + 0xD5C930
character_offsets = [0x0]
character_list = ["Dante", "Vergil"]
character_current = 0

#Image settings
image_current = "dmc3rpc_icon"

#Battle settings
battle_address = process.get_base_address() + 0xD5C708
battle_offsets = [0x0]
battle_current = 0

#Stylish settings
stylish_rank_address = 0x046E0790
stylish_rank_offsets = [0x0]
stylish_rank_current = 0
stylish_rank_list = ["Dope!", "Crazy!", "Blast!", "Alright!", "Sweet", "SShowtime!!", "SSStylish!!!"]

style_address = 0x2428A100C68
style_list = ["Trickster", "Swordmaster", "Gunslinger", "Royalguard", "Quicksilver", "Doppelganger"]
style_2_list = ["Dark Slayer"]
style_info_list = ["Dodging effortlessly away", "Slicing with precision", "Unloading relentless fire", "Absorbing every blow", "Slashing after flashing", "Fighting in Unison"]
style_2_info_list = ["Vanishing between lunges"]
style_offsets = [0x0]
style_current = 0
style_info = ""
style_info_details = ""

def _mission():
    mission_pointer = process.get_pointer(mission_address, mission_offsets) 

    if mission_pointer != 0:
        global mission_info
        global mission_ingame
        mission_info = "Playing Mission: " + str(mission_pointer)
        mission_ingame = 1
    else:
        mission_ingame = 0
        mission_info = "In Menu"

def _difficulty():
    difficulty_pointer = process.get_pointer(difficulty_address, difficulty_offsets)
    difficulty_hoh = int(process.readByte(difficulty_address + 0x4, 1)[0], 16)
    global difficulty_info
    if difficulty_hoh == 1 and difficulty_pointer == 2: #Checks for Heaven or Hell
        difficulty_info = difficulty_list[5]
    else:
        difficulty_info = difficulty_list[difficulty_pointer]
        
def _character():
    if mission_ingame == False:
        return
    character_pointer = process.get_pointer(character_address, character_offsets)

    global character_current
    character_current = character_pointer


def _image():
    global image_current
    if mission_ingame == False:
        image_current = "dmc3rpc_icon"
    else:
        if battle_current == 0:
            if character_current == 0:
                image_current = "dmc3rpc_dante"
            else:
                image_current = "dmc3rpc_vergil"
        else:
            if stylish_rank_current == 0: image_current = "dmc3rpc_dope"
            if stylish_rank_current == 1: image_current = "dmc3rpc_crazy"
            if stylish_rank_current == 2: image_current = "dmc3rpc_blast"
            if stylish_rank_current == 3: image_current = "dmc3rpc_alright"
            if stylish_rank_current == 4: image_current = "dmc3rpc_sweet"
            if stylish_rank_current == 5: image_current = "dmc3rpc_showtime"
            if stylish_rank_current == 6: image_current = "dmc3rpc_stylish"
            
            
def _battle():
    battle_pointer = process.get_pointer(battle_address, battle_offsets)

    global battle_current
    battle_current = battle_pointer

def _style():
    stylish_rank_pointer = process.get_pointer(stylish_rank_address, stylish_rank_offsets)
    style_pointer = process.get_pointer(style_address, style_offsets)

    global stylish_rank_current
    global style_current
    stylish_rank_current = stylish_rank_pointer
    style_current = style_pointer

    global style_info
    global style_info_details
    if character_current == 0:
        style_info = style_list[style_current]
        style_info_details = style_info_list[style_current]
    else:
        style_info = style_2_list[0]
        style_info_details = style_2_info_list[0]

if __name__ == "__main__":
    while True: 
        if process == 0: exit()
        time.sleep(cooldown)
        print(rpcTime)

        _mission()
        _difficulty()

        _battle()
        _style()

        _character()

        _image()

        if battle_current == 1:
            RPC.update(details=style_info, state=style_info_details, large_image=image_current, start=rpcTime)
        else:
            RPC.update(details=mission_info, state=difficulty_info, large_image=image_current, start=rpcTime)
