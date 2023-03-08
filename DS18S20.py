from machine import Pin 
import time 
 
DQ = Pin('D4', Pin.OUT) 
 
# Reset DS18S20 
def DS18S20_Rst(): 
    DQ.init(Pin.OUT)  # set as output 
    DQ.value(0)  # DQ low level 
    time.sleep_us(750)  # 750us 
    DQ.value(1)  # DQ high level
    time.sleep_us(60);        

def DS18S20_Check(): 
    retry = 0 
    DQ.init(Pin.IN)  # set as input  
    while DQ.value() == 1 and retry < 200: 
        retry += 1 
        time.sleep_us(1) 
    if retry >= 200: 
        return 1 
    retry = 0 
    while DQ.value() == 0 and retry < 240: 
        retry += 1 
        time.sleep_us(1) 
    if retry >= 240: 
        return 20 
    return 0 

def DS18S20_Init(): 
    DS18S20_Rst() 
    DS18S20_Check() 
 
def DS18S20_Read_Bit(): 
    data = 0 
    DQ.init(Pin.OUT) # set as output 
    DQ.value(0)  
    time.sleep_us(4)  
    DQ.init(Pin.IN) # set as input  
    time.sleep_us(10) 
    if DQ.value():
        data  = 1
    else:
        data  = 0
    time.sleep_us(50) 
    return data

def DS18S20_Read_Byte():  
    dat = 0x00  
    for i in range(8):   
        j = DS18S20_Read_Bit()
        dat = (j<< 7) | (dat >> 1) # save the data in dat
    return dat  

def DS18S20_Write_Byte(dat): 
    testb = 0x00 
    DQ.init(Pin.OUT)  # set as output
    for j in range(8): 
        testb = dat & 0x01 
        dat = dat >> 1 
        if testb:  # write 1 
            DQ.value(0) 
            time.sleep_us(2)  # Between two write time slots
            DQ.value(1) 
            time.sleep_us(60)  # hold for 60us 
        else:  # write 0
            DQ.value(0) 
            time.sleep_us(60)  # hold for 60us 
            DQ.value(1) 
            time.sleep_us(2)  # Between two write time slots
    
def DS18S20_Read_Temp():   
    DS18S20_Init()
    DS18S20_Write_Byte(0xCC) 
    DS18S20_Write_Byte(0x44)
    DS18S20_Init()
    DS18S20_Write_Byte(0xCC)
    DS18S20_Write_Byte(0xBE)  
    low = DS18S20_Read_Byte() 
    #high = DS18S20_Read_Byte() 
    return low

while True: 
    tp = DS18S20_Read_Temp()    
    print(tp)  
    time.sleep(1)
