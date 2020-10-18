import speech_recognition as sr
import queue 
import threading 

message_queue = queue.Queue()
is_running = True
lock = threading.Lock()

def runner(): 
    global message_queue, is_running
    credentials = r""" 
    DATA FROM SERVICE API KEY
    """
    # obtain audio from the microphone
    recognizer = sr.Recognizer()
    source = sr.Microphone()
    audio = None
    with sr.Microphone() as source:
        audio = recognizer.adjust_for_ambient_noise(source)
    print("Starting Program")
    while(is_running): 
        with sr.Microphone() as source:
            audio = recognizer.listen(source, phrase_time_limit = 5)
        try:
            message = recognizer.recognize_google_cloud(audio, credentials_json=credentials)
            message = message.lower()
            print("The Message is " + message)
            if("end" in message): 
                message_queue.put("End Call")
                with lock:
                    is_running = False
            elif("start" in message):
                message_queue.put("Activate Video")
            elif("stop" in message): 
                message_queue.put("Stop Video")
        except Exception as e:
            print("Program Error:\n {0}".format(e))
            with lock:
                is_running = False

if __name__ == "__main__": 
    runner()