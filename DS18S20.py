from machine import Pin 
import time 
 
# GPIO port 
 
DQ = Pin('D4', Pin.OUT) 
 
# Reset DS18S20 
def DS18S20_Rst(): 
    DQ.init(Pin.OUT)  # set as output 
    DQ.value(0)  # DQ low level 
    time.sleep_us(750)  # 750us 
    DQ.value(1)  # DQ high level
    time.sleep_us(60);   
     
 
# Waiting for the response from DS18S20 
# After DS18S20 is reset, it will pull down the bus for 60-240us to indicate the existence
# Return 1: The existence of DS18S20 is not detected
# return 0: exists
def DS18S20_Check(): 
    #DS18S20_Rst() 
    retry = 0 
     
    DQ.init(Pin.IN)  # set as input  
     
    while DQ.value() == 1 and retry < 180: 
        retry += 1 
        time.sleep_us(1) 
    if retry >= 200: 
        return 1 
    print(DQ.value()) 
    retry = 0 
    while DQ.value() == 0 and retry < 240: 
        retry += 1 
        time.sleep_us(1) 
    if retry >= 240: 
        return 20 
    print(DQ.value()) 
    return 0 

 
def DS18S20_Init(): 
    DS18S20_Rst() 
    DS18S20_Check() 
 
 
# Write a byte to the DS18S20
# dat: bytes to write
def DS18S20_Write_Byte(dat): 
    testb = 0 
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
 
 
# Read a byte from DS18S20
# Return: the bytes read
def DS18S20_Read_Byte():  
    testb = 0  
    dat = 0  
    DQ.init(Pin.OUT) # set as output  
    for j in range(8):  
        DQ.init(Pin.OUT) # set as output 
        DQ.value(0)  
        time.sleep_us(2)  
        DQ.init(Pin.IN) # set as input  
        testb = DQ.value() # read data 
        dat = (dat >> 1) | (testb << 7) # save the data in dat
        time.sleep_us(60)  
    return dat  
  
# start DS18S20  
def DS18S20_Start():  
    DQ.init(Pin.OUT) # set as output  
    DQ.value(0) # The host pulls the bus low to issue a start signal 
    time.sleep_us(750) # hold for 750us  
    DQ.value(1) # The master pulls the bus high and waits for the slave to respond 
    DQ.init(Pin.IN) # set as input   
    while DQ.value() == 1: # Waiting for the slave to pull the bus low 
        pass  
    time.sleep_us(250) # Delay 250us, waiting for the slave to complete the preparation work    

def DS18S20_Read_Temp():   
    DS18S20_Start() # start DS18S20   
    DS18S20_Write_Byte(0xCC) # Skip ROM operation, directly convert   
    DS18S20_Write_Byte(0x44) # Start temperature conversion   
    while DS18S20_Read_Byte() == 0xFF: # 等待转换完成   
        time.sleep_us(100)   
    DS18S20_Start() # start DS18S20   
    DS18S20_Write_Byte(0xCC) # Skip ROM operation, read directly   
    DS18S20_Write_Byte(0xBE) # read temperature register  
 
    low = DS18S20_Read_Byte() # read temperature low  
    high = DS18S20_Read_Byte() # read temperature high  

    low &= 0xF8 # clear the lower three bits 
    high = DS18S20_Read_Byte() # read temperature high   
    if high > 1: 
        high = ~high 
        low = ~low 
        sig = 0 
    else: 
        sig = 1 
    temp = high 
    temp<<=8   
    temp+=low 
    temp=temp*0.5 
    if sig==1: 
        return temp 
    else: 
        return -temp 
while True: 
    tp = DS18S20_Read_Temp()  # Call the function to get the temperature value and assign it to the variable tp  
    print(tp)  # Reference variable tp to output temperature value 
    time.sleep(1)
