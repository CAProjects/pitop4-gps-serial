import queue, threading, io, serial, pynmea2
from time import sleep
import logging
from pitop.miniscreen import Miniscreen
from PIL import Image, ImageDraw, ImageFont

gpsSerial = serial.Serial('/dev/ttyS0', 9600, timeout=1.)
gpsIO = io.TextIOWrapper(io.BufferedRWPair(gpsSerial, gpsSerial))
gpsSerial.write(b'$PMTK314,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1*34\r\n')

ms = Miniscreen()
image = Image.new(ms.mode, ms.size,)
canvas = ImageDraw.Draw(image)
ms.set_max_fps(60)

nmea_list = ['GGA', 'GSA', 'RMC', 'ZDA']
nmea_dict = {
    'latitude' : "",
    'longitude' : "",
    'speed' : "",
    'date_time' : "",
    'satelites' : 0,
    'altitude' : "",
    'fix' : True,
    'fix_type': ""}

q = queue.Queue()

def SensorThread(q,name):
    while True:
        try:
            line = gpsIO.readline()
            msg = pynmea2.parse(line)
            if msg.sentence_type in nmea_list:
                q.put(msg)
        except serial.SerialException as e:
            print('Device error: {}'.format(e))
            break
        except (pynmea2.ParseError, AttributeError) as e:
            continue


def PrintThread(q,name, nmeadict):
    while True:

        if not q.empty():
            msg = q.get()
            if msg.sentence_type == 'GGA':
                nmea_dict['satelites'] = msg.num_sats
                nmea_dict['altitude'] = msg.altitude
            elif msg.sentence_type == 'GSA':
                nmea_dict['fix'] = 'Yes' if int(msg.mode_fix_type) > 1 else 'No'
                nmea_dict['fix_type'] = f'{msg.mode_fix_type}D' if int(msg.mode_fix_type) > 1 else ''
            elif msg.sentence_type == 'RMC':
                pole = 'N' if float(msg.latitude) > 0 else 'S'
                nmea_dict['latitude'] = f" {'%02d' % (msg.latitude)}{pole} %02dm %07.4fs" % (msg.latitude_minutes, msg.latitude_seconds)
                pole = 'E' if float(msg.longitude) > 0 else 'W'
                lon = str(abs(int('%02d' % (msg.longitude)))).zfill(3)
                nmea_dict['longitude'] = f"{lon}{pole} %02dm %07.4fs" % (msg.longitude_minutes, msg.longitude_seconds)
                nmea_dict['speed'] = f'{round((float(msg.spd_over_grnd) * 1.150779448),1)} MPH'
            elif msg.sentence_type == 'ZDA':
                nmea_dict['date_time'] = f'{str(int(msg.day)).zfill(2)}/{str(int(msg.month)).zfill(2)}/{str(msg.year)[-2:]} {str(int(msg.datetime.hour)).zfill(2)}:{str(int(msg.datetime.minute)).zfill(2)}:{str(int(msg.datetime.second)).zfill(2)}'
        else:
            canvas.rectangle(ms.bounding_box, fill=0)
            canvas.text((0, 0),f"Lat:{nmeadict['latitude']}",font=ImageFont.load_default(),fill=1)
            canvas.text((0, 13),f"Lon:{nmeadict['longitude']}",font=ImageFont.load_default(),fill=1)
            canvas.text((0, 26),f"Spd:{nmeadict['speed']}",font=ImageFont.load_default(),fill=1)
            canvas.text((0, 39),f"Fix:{'Yes' if nmeadict['fix'] else 'No'}, {nmeadict['fix_type']}, {nmeadict['satelites']} Sats",font=ImageFont.load_default(),fill=1)
            canvas.text((0, 52),f"UTC:{nmeadict['date_time']}",font=ImageFont.load_default(),fill=1)
            ms.display_image(image)
            sleep(0.1)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    #logging.basicConfig(format=format, level=logging.INFO,
    #                    datefmt="%H:%M:%S")
    qt = threading.Thread(target=SensorThread, args=(q,'Sensor'))
    pt = threading.Thread(target=PrintThread, args = (q,'Print', nmea_dict))
    qt.start()
    pt.start()
