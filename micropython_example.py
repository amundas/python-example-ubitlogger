import microbit
import radio
import struct
import random

"""
This function can send integers, decimal numbers and strings up to a length of 19 characters
The purpose is to format data the way that ubitlogger.com expects
"import radio", "import microbit" and "import struct" are required for it to work. 
The radio also has to be configured for a maximum packet length of at least 35.
"""
def send(data):
    pkt = bytearray(32) #placeholder for packet
    # assembly code to read out ID
    @micropython.asm_thumb
    def reg_read(r0):
        ldr(r0, [r0, 0])
    microbit_id = reg_read(0x10000064)
    time = microbit.running_time()
    pkt[0] = 0x01
    pkt[1] = 0x00
    pkt[2] = 0x01
    for i in range(0, 4):
        pkt[4+i] = (time >>(i*8)) & 0xff
    for i in range(0, 4):
        pkt[8+i] = (microbit_id >>(i*8)) & 0xff
    
    if type(data) is int:
        pkt[3] = 0 #integer
        for i in range(0, 4):
            pkt[12+i] = (data >>(i*8)) & 0xff
    elif type(data) is float:
        pkt[3] = 4 #float
        ba = bytearray(struct.pack("d", data)) 
        for i in range(0, 8):
            pkt[12+i] = ba[i]
    elif type(data) is str:
        pkt[3] = 2 #string
        ba = bytearray(data)
        if len(data) > 19: # string is too long to send
            return
        pkt[12] = len(ba)
        for i in range(0, len(ba)):
            pkt[13+i] = ba[i]
    radio.send_bytes(pkt)

radio.config(length=35, group=0) # length must be at least 35 for it to work with ubitlogger.com
radio.on()

while True:
    #flash a random LED
    ledr = random.randint(0, 4)
    ledc = random.randint(0, 4)
    microbit.display.set_pixel(ledr,ledc,9)
    microbit.sleep(20)
    microbit.display.set_pixel(ledr,ledc,0)
    microbit.sleep(20)
    #Get acellerometer data and send over radio
    ax = microbit.accelerometer.get_x()
    send(ax)