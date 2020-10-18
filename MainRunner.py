import cv2
import speech_recognition as sr
from live import process_frame
from playsound import playsound
import queue 
import threading 
import numpy as np

message_queue = queue.Queue()
is_running = True
lock = threading.Lock()
credentials = r""" 
    DATA FROM A SERVICE API KEY
"""

def add_toolbar(frame, muted): 
    if not muted:
        toolbar_image = cv2.imread("Working_Image.jpg")
    else:
        toolbar_image = cv2.imread("MutedBar.jpg")
    frame_width = frame.shape[1]
    scale_factor = (1.0 * frame_width)/toolbar_image.shape[1]
    copy = cv2.resize(toolbar_image, None, fx = scale_factor, fy = scale_factor)
    copy_width = copy.shape[1]
    if(frame_width > copy_width):
        copy = cv2.copyMakeBorder(copy, 0, 0, frame_width - copy_width, 0, cv2.BORDER_CONSTANT, None, (0, 0, 0))
    elif(copy_width > frame_width): 
        frame = cv2.copyMakeBorder(frame, 0, 0, copy_width - frame_width, 0, cv2.BORDER_CONSTANT, None, (0, 0, 0))
    combined_image = np.vstack((frame, copy))
    return combined_image

def stop_running(): 
    global is_running
    with lock: 
        is_running = False

def voice_processor(): 
    global message_queue, is_running
    # obtain audio from the microphone
    recognizer = sr.Recognizer()
    source = sr.Microphone()
    audio = None
    with sr.Microphone() as source:
        audio = recognizer.adjust_for_ambient_noise(source)
    print("Starting voice processor")
    while(is_running): 
        with sr.Microphone() as source:
            audio = recognizer.listen(source, phrase_time_limit = 3)
        try:
            message = recognizer.recognize_google_cloud(audio, credentials_json=credentials)
            if(len(message) == 0): 
                continue
            message = message.lower()
            print("Message is " + message)
            if("leave" in message): 
                display_image = np.zeros((100,400,3))
                cv2.putText(display_image, "Please say confirm if", (20, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (255, 255, 255), 1)
                cv2.putText(display_image, "you want to leave the call", (20, 70), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (255, 255, 255), 1)
                cv2.imshow("Exit Message", display_image)
                cv2.waitKey(2)
                message = ""
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, phrase_time_limit = 3) 
                    message = recognizer.recognize_google_cloud(audio, credentials_json=credentials)
                if("confirm" in message):
                    message_queue.put(0)
                else: 
                    print("You didn't say confirm so the program is continuing")
                cv2.destroyWindow("Exit Message")
            elif("start" in message):
                message_queue.put(1)
            elif("stop" in message):
                message_queue.put(2)
            elif("unmute" in message): 
                message_queue.put(4)
            elif("mute" in message):
                message_queue.put(3)
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))
            stop_running()

cap = cv2.VideoCapture(0)
to_show = True
emptyFrameCount= 0

emptyFrameLimiter = 60
processor_thread = threading.Thread(target = voice_processor)
processor_thread.start()
mutedFlag = False

# button dimensions (y1,y2,x1,x2)
button = [400,550,0,150]

def process_click (event, x, y, flags, params):
    global mutedFlag, button
    if event == cv2.EVENT_LBUTTONDOWN:
        if y > button[0] and y < button[1] and x > button[2] and x < button[3]:   
            mutedFlag = not mutedFlag

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', process_click)
paused_image = cv2.imread("VideoOffImage.jpg")

while(is_running):
    # Capture frame-by-frame
    ret, frame = cap.read()

    display_frame, emptyFrame = process_frame(frame)
    if (emptyFrame):
        emptyFrameCount+=1
    else:
        if emptyFrameCount > emptyFrameLimiter:
            emptyFrameCount = 0
            #Plays happy Rejoined sound
            playsound("HappySound.mp3", False)
        else:
            emptyFrameCount = 0
    
    if (emptyFrameCount !=0 and emptyFrameCount% emptyFrameLimiter == 0):
        #Plays sad out of frame sound every emptyFrameLimiter count
        playsound("SadSound.mp3", False)
    
    # Display the resulting frame
    if to_show:
        display_frame = add_toolbar(display_frame, mutedFlag)
        cv2.imshow('frame', display_frame)
    else: 
        cv2.imshow('frame', paused_image)
    key_pressed = cv2.waitKey(2) & 0xFF
    if key_pressed == ord('q'):
        stop_running()
    if key_pressed == ord('p'): 
        to_show = not to_show
    #Read from queue (Toggle to_show)
    while(message_queue.qsize() > 0): 
        text = message_queue.get()
        if(text == 0): 
            stop_running()
        elif(text == 1): 
            to_show = True
        elif text == 2: 
            to_show = False
        elif text == 3:
            mutedFlag = True
        else:
            mutedFlag = False
        print("Muted Flag is Now " + str(mutedFlag))
cap.release()
cv2.destroyAllWindows()
