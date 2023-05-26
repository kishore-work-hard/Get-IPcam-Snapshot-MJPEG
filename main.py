#!/usr/bin/python3
# by kichu - May 2023
#
# Last update: 20230430, 20230503, 20230515



import io, sys, time
import requests, json
from PIL import Image
from requests.auth import HTTPDigestAuth


def get_mjpeg_frame(cam):
    r = requests.get('http://' + cam['ip'] + '/cgi-bin/video.cgi?type=http&cameraID=1&mjpegplay=1',
                     auth=HTTPDigestAuth(cam['user'], cam['pass']), timeout=10, stream=True)
    buf = b''
    for b in r.iter_content(65536):
        buf += b
        print('FILL:', len(buf))
        x = buf.find(b'Content-Length:')
        if x < 0: continue
        y = buf.find(b'\r', x)
        if y < 0: continue
        w = int(buf[x + 15:y])
        buf = buf[y + 4:]
        break
    for b in r.iter_content(65536):
        buf += b
        if len(buf) < w: continue
        r.close()
        return (buf[:w])


cams = json.load(open('test_Car.json'))
print(cams)


d_count= 0
while True:
    for c in cams:
        cam = cams[c]
        try:
            img = Image.open(io.BytesIO(get_mjpeg_frame(cam)))

        except Exception as e:
            print(sys.exc_info()[2].tb_lineno, e)
            time.sleep(1)
    d_count = d_count + 1



