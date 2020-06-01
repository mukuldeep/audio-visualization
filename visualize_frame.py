import pyaudio
import wave
import sys
import numpy as np
import cv2
from numpy import *

height=1000
width=1000
vframe=np.zeros((height,width,3), np.uint8)

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

CHUNK = 1024
data = wf.readframes(CHUNK)
cnt=0
try:
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
        print(cnt)
        cnt=cnt+1
except KeyboardInterrupt:
    pass
print(cnt)
stream.stop_stream()
stream.close()
p.terminate()

#display
lent=len(list(data))
compress_factor=1
curr_data_bit=0
for i in range(int(width)):#lent changed to width
    #printing line for seperate stream in the image data
    cv2.line(vframe,((i%width),height-700-10),((i%width),height-700-int(list(data)[curr_data_bit*compress_factor*4])-10),(0,255,0),1)
    cv2.line(vframe,((i%width),height-500-10),((i%width),height-500-int(list(data)[curr_data_bit*compress_factor*4+1])-10),(0,0,255),1)
    cv2.line(vframe,((i%width),height-200-10),((i%width),height-200-int(list(data)[curr_data_bit*compress_factor*4+2])-10),(255,0,0),1)
    cv2.line(vframe,((i%width),height-10),((i%width),height-int(list(data)[curr_data_bit*compress_factor*4+3])-10),(0,255,255),1)
    curr_data_bit=curr_data_bit+1
    if curr_data_bit==int(1024/compress_factor):
        cv2.line(vframe,((i%width),height-10),((i%width),0),(255,255,255),1)
        curr_data_bit=0
        data = wf.readframes(CHUNK)
        
#image is shown in window named sound show
cv2.imshow('sound show',vframe)
while(True):#wait for press, exit on pressing q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#destroy all window
cv2.destroyAllWindows()
