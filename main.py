from huskylib import HuskyLensLibrary #Huskylens lib
import json
import time
import serial #Pyserial lib for connect to Arduino
import stepper
import wave
import pyaudio
Husky = HuskyLensLibrary('SERIAL', '/dev/ttyUSB0', 3000000) #KeonWoo PARK; Connect to huskylens through USB Serial
Arduino=serial.Serial(port='/dev/ttyUSB1', baudrate=9600, timeout=.5) #KeonWoo PARK; Connect to Arduino
Arduino.flush()
Arduino.flushInput()
Arduino.flushOutput()
step1 = stepper.stepper(9,10,700)
step2 = stepper.stepper(14,15,700)
loc = '/home/pi/Desktop/Voice'


def read():
    if Arduino.readable():
        res = Arduino.readline().decode()[:len(res)-1]
        return res
    else:
        return False
def send(a):
    Arduino.write(a.encode('utf-8'))

def check(what):
    if what=="isfront": #KeonWoo PARK; Check user.
        send("isfront")
        time.sleep(0.5)
        for i in range(3):
            g = read()
            if g == False:
                time.sleep(1)
                continue
            else:
                return g
        print("Timeout occurred While get ",what)
        exit()
    elif what=='temp':
        send('temp')
        time.sleep(0.5)
        for i in range(3):
            g = read()
            if g == False:
                time.sleep(1)
                continue
            else:
                return g
        print("Timeout occurred While get ",what)
        exit()
    elif what=='mask':
        t = [0,0,0]
        for i in range(5):
            v = Husky.requestAll()
            time.sleep(0.75)
            t[v[0].ID] = t[v[0].ID] + 1
        if t[0]<t[1]:
            if t[1]<t[2]:
                return 2
            else:
                return 1
        else:
            if t[0]<t[2]:
                return 2
            else:
                return 0

def play(file):
    chunk = 1024
    path = loc + file
    with wave.open(path, 'rb') as f:
        p = pyaudio.PyAudio()  
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
        data = f.readframes(chunk)  
        while data:  
            stream.write(data)  
            data = f.readframes(chunk)  
        stream.stop_stream()  
        stream.close()  
        p.terminate()
def givemask():
    #do something
    return

def __main__():
    while True:
        time.sleep(1)
        print("?????? ????????? ??????")
        result = check("isfront")
        if result!="yes":
            print("????????????")
            continue

        print("?????? ??????")
        play('???????????????.wav')
        play('??????.wav')
        time.sleep(1)
        play('?????????_??????????????????_?????????_??????????????????.wav')
        print("?????? ?????? ??????")
        result = check('temp')
        if result > 37.5:
            print("????????????")
            play('????????????.wav')
            print("????????????")
            play('??????.wav')
            continue
        print("????????????")
        play('????????????.wav')
        print("????????? ?????? ??????")
        play('?????????.wav')
        q=0
        v=0
        while True:
            q=check('mask')
            if q == 0:
                play('??????X.wav')
            if q == 0 and v==2:
                play('3???X_????????????.wav')
            if q==1:
                play('?????????X_??????.wav')
                givemask()
            if q==1 and v==1:
                play('?????????X.wav')
            if q==1 and v==2:
                play('3???X_????????????.wav')
                break
            if q==2:
                break
        if q==1 and v==2:
            continue
        
        