from re import search
from subprocess import Popen, PIPE
import time, datetime, os, sys, requests
from PIL import Image, ImageFont, ImageDraw
from data_folder import epd2in9_V2

delay = 1  #60 = 1 min

refresh = 1800

wifi_icon_size = 96, 96

# Folder directory
basedir = os.path.dirname(os.path.realpath(__file__))
icondir = os.path.join(basedir, 'icons')
fontdir = os.path.join(basedir, 'fonts')
tempdir = os.path.join(basedir, 'temp')

# Font setting
fonts = 'FreeSans.ttf'
font12 = ImageFont.truetype(os.path.join(fontdir, fonts), 12)
font18 = ImageFont.truetype(os.path.join(fontdir, fonts), 18)

def get_wifi_siginal():
    proc = Popen(['iwconfig'], stdout=PIPE, stderr=PIPE)
    intext=str(proc.communicate()[0])
    # print(intext)

    m2=search('ESSID:".*" ',intext)
    ESSID=m2.group(0).split('"')[1]
    # print ('ESSID :',ESSID)

    m3=search('Link Quality=[ABCDEF0123456789:]*',intext)
    lq=m3.group(0).split(' ')[1]
    # print(lq)
    w_quality =int(lq[8:])
    # print('Link Quality :', w_quality)
    w_percent = str(round(w_quality/70*100))+'%'
    # print('Wifi Percent :', w_percent)

    m4=search('Signal level=[-ABCDEF0123456789:]*',intext)
    sl=m4.group(0).split(' ')[1]
    # print(sl)
    w_level =int(sl[6:])
    # print('Signal Level :', str(w_level)+'dBm')

    if w_level <= -55: # Good
        w_strength = 3
        w_icon = 'wifi_3.bmp'
    elif w_level <= -40 : # Middle
        w_strength = 2
        w_icon = 'wifi_2.bmp'
    elif w_level <= -30 : # Weak
        w_strength = 1
        w_icon = 'wifi_1.bmp'
    else: # Very weak
        w_strength = 0
        w_icon = 'wifi_0.bmp'
    # print (w_strength)
    # print (w_icon)
    return ESSID, w_quality, w_percent, w_level, w_strength, w_icon

def print_wifi_signal():
    ssid, wifi_quality, wifi_percent, wifi_level, wifi_strength, wifi_icon = get_wifi_siginal()
    print(get_wifi_siginal())
    print('SSID          :', ssid)
    print('Link Quality  :', wifi_quality)
    print('Wifi Percent  :', wifi_percent)
    print('Signal Level  :', wifi_level)
    print('Wifi Strength :', wifi_strength)
    print('Wifi Icon     :', wifi_icon)

def draw_frame():
    ssid, wifi_quality, wifi_percent, wifi_level, wifi_strength, wifi_icon = get_wifi_siginal()
    draw.rectangle((0, 0, 296, 128), fill=1)
    draw.rounded_rectangle((5, 5, 168, 123), fill=1, outline=0, width=2, radius=15)
    draw.rounded_rectangle((173, 5, 291, 123), fill=1, outline=0, width=2, radius=15)
    draw.text((15,15), 'SSID : ' + ssid, font = font18, fill = 0)
    draw.text((15,40), 'Level :' , font = font18, fill = 0)
    draw.text((15,65), 'Qty    :' , font = font18, fill = 0)    
    draw.text((15,90), 'Icon   :' , font = font18, fill = 0) 

def draw_WiFi():
    ssid, wifi_quality, wifi_percent, wifi_level, wifi_strength, wifi_icon = get_wifi_siginal()
    wifi_logo = Image.open(os.path.join(icondir, wifi_icon))         
    wifi_logo = wifi_logo.resize(wifi_icon_size)
    draw.rectangle((184, 15, 280, 111), fill = 1, outline = 1)
    Himage.paste(wifi_logo, (184, 11))

    draw.rectangle((75, 40, 140, 60), fill = 1, outline = 1)
    draw.text((75, 40), str(wifi_level) +'dBm', font=font18, fill=0)

    draw.rectangle((75, 65, 140, 85), fill = 1, outline = 1)
    draw.text((75, 65), wifi_percent, font=font18, fill=0)

    draw.rectangle((75, 90, 160, 110), fill = 1, outline = 1)
    draw.text((75, 90), wifi_icon, font=font18, fill=0)

def epaper_Clear():
    epd.init()
    epd.Clear(0xFF)

def epaper_Exit():
    epd = epd2in9_V2.EPD()
    epd.init()
    epd.Clear(0xFF)
    epd2in9_V2.epdconfig.module_exit()

try:
    epd = epd2in9_V2.EPD()
    epaper_Clear()
    max_Width, max_Height = 296, 128            
    Himage = Image.new('1', (max_Width, max_Height), 255)
    draw = ImageDraw.Draw(Himage)
    draw_frame()
    draw_WiFi()
    epd.display_Base(epd.getbuffer(Himage))
    
    counter = 0
    while True:

        draw_WiFi()

        epd.display_Partial(epd.getbuffer(Himage))
        Himage.save(os.path.join(tempdir, 'Temp_Wifi_info.bmp'))

        time.sleep(delay)

        # print(counter)
        counter += 1
        if counter > refresh :
            print('Refresh...')
            epaper_Clear()
            epd.display_Base(epd.getbuffer(Himage))
            counter = 0
           
except KeyboardInterrupt:
    print('leaning...')
    epaper_Exit()
    print("Exit!")
    exit()
