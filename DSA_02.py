import cv2
from datetime import datetime
import pyautogui
#import matplotlib
import os
import time
import keyboard
import tkinter as tk
#matplotlib.use("TkAgg")
import os
import numpy as np
from datetime import datetime
#import RPi.GPIO as GPIO
import time
import atexit
# Set the GPIO pin numbering mode
#GPIO.setmode(GPIO.BCM)

# Set the GPIO pin to output mode
#GPIO.setup(17, GPIO.OUT)
camera = cv2.VideoCapture(0)                   # Initialize the video capture object to access the default camera, if not accessible change index
# Set the frame size of the camera capture object to 1280x720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
camera.set(cv2.CAP_PROP_FPS, 20)

if not camera.isOpened():                      # if webcam cannot be accessed
   raise IOError("Webcam cannot be opened! Change index!")
ret, live=camera.read()
gray=cv2.cvtColor(live,cv2.COLOR_BGR2GRAY)
# Set a flag to indicate if the 'r' key is pressed or not

def cleanup():
    if camera.isOpened():
        camera.release()
        cv2.destroyAllWindows()

# Register cleanup function to be called on exit
atexit.register(cleanup)

# create the opencv window
cv2.namedWindow("angio sim", cv2.WND_PROP_FULLSCREEN)
cv2.namedWindow('angio sim', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('angio sim', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# Function to display the message box
# Function to display the message box
# Create a Tkinter window as notification for start
import tkinter as tk
#function for notificaTION#
def show_notification(text):
    window = tk.Tk()
    window.overrideredirect(True)
    window.geometry("+{}+{}".format(window.winfo_screenwidth() // 2 - 100, window.winfo_screenheight() // 2 - 50))
    window.attributes("-alpha", 0.7)
    window.attributes("-topmost", True)

    # Create a frame to hold the label
    frame = tk.Frame(window, bg="black")
    frame.pack(fill="both", expand=True)

    # Create a label with the specified font and text, set it to wrap text and fill available space
    label = tk.Label(frame, text=text, font=("Arial", 20), bg='black', fg='white', wraplength=500, justify="center")
    label.pack(fill="both", expand=True)

    # Destroy the window after 3 seconds
    window.after(3000, window.destroy)
    window.mainloop()



#for recording video of aufnahme
fourcc = cv2.VideoWriter_fourcc(*'X264')
filename2 = 'output_{}.avi'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
# Set the screen size
screen_size = (1920, 1080)
fps = 24
        
# Create a video writer object
video_writer = cv2.VideoWriter(filename2, fourcc, fps, screen_size)
# To show a notification, call the function with the desired text
show_notification("DSA mode, press r and release to take background, then d for subtraction sequence which is automatically recorded, and 8 for replaying subtraction sequence")
#necessary flags and variables#
key=cv2.waitKey(1)
count=0
show_video=False
key_pressed=False

while True:           
                 ret, live = camera.read()  #read live feed
                 gray = cv2.cvtColor(live, cv2.COLOR_BGR2GRAY)
                 key=cv2.waitKey(1) & 0xFF
                
                  # Get the current screen frame
                 screen_frame = pyautogui.screenshot()
                 

                 # Convert the screen frame to a numpy array
                 screen_frame_np = cv2.cvtColor(np.array(screen_frame), cv2.COLOR_RGB2BGR)

                 if ret:
                     # Display the frame if the 'r' key is pressed
                    key=cv2.waitKey(1)  & 0xFF #to run live feed smoothly
                    if key ==ord('7'):
                      exit() 
                    if key==ord('s'):
                          path = r'C:/Users/Smit/Desktop/Dsa Simulator' #change directoryr
                          os.chdir(path) #change to above path to save file
                          target = pyautogui.getActiveWindow()
                          location = (
                          target.left,
                          target.top,
                          target.width,
                          target.height
                          )
                          image = pyautogui.screenshot(region=location)
                          now = datetime.now() #get current date and time
                          dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
                          #image.show()
                          filename1 = 'Screenshot_DSA_Mode_' + dt_string  +'.jpg'
                          image=image.save(filename1)
                          show_notification("Screenshot saved, please view in folder Dsa Simulator")                        
            
                    if show_video:
                         cv2.imshow('angio sim', gray)  #create a blank window7
                         
                         key=cv2.waitKey(1)  & 0xFF #for making the live feed run smoothly
                    if key == ord('r'): #if condition for keypress r
                         show_video = True  #change value of flag
                         bg=None
                         key_pressed=True
                         now = datetime.now() #get current date and time
                         #dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
                         #filename = 'Backgroundat1fps_'+ dt_string +'.jpg'
                         #key=cv2.waitKey(1)           
                    if key_pressed and  not keyboard.is_pressed('r'):
                         bg=gray
                         #print(bg.shape)
                         font = cv2.FONT_HERSHEY_PLAIN
                         now_without_ms= now.strftime('%Y-%m-%d %H:%M:%S')

                         cv2.putText(bg, str(now_without_ms), (20, 40), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
                         maske=live
                         gray_mask=cv2.cvtColor(live, cv2.COLOR_BGR2GRAY)
                         key_pressed=False# to freeze live feed
                    if key==ord('3'):
                         show_notification("Already in DSA mode, background reset successfully, please take new Background.")                               
                    elif not keyboard.is_pressed('r'):
                         show_video = False
                    if key == ord('d'):
                         #GPIO.output(17, GPIO.HIGH)
                         start_time1=time.monotonic()
                         diff = cv2.absdiff(gray, bg)
                         inverted_diff = cv2.bitwise_not(diff)
                         diff_colormap = cv2.applyColorMap(diff, cv2.COLORMAP_BONE)
    
                         # create a light gray background image with the same shape as inverted_diff
                         background = np.full(inverted_diff.shape, 0, dtype=np.uint8)
    
                         # blend the inverted_diff and background images
                         alpha = 0.8
                         blended_image = cv2.addWeighted(inverted_diff, alpha, background, 1-alpha, 0)
    
                         cv2.imshow('angio sim', blended_image)
                         key=cv2.waitKey(1)
                         # Write the current screen frame to the output video
                         screen_frame = pyautogui.screenshot()

                         # Convert the screen frame to a numpy array
                         screen_frame_np = cv2.cvtColor(np.array(screen_frame), cv2.COLOR_RGB2BGR)

                         video_writer.write(screen_frame_np)  
                    #elif time.monotonic-start_time1>=30:
                         #GPIO.output(17, GPIO.LOW)
                         # Clean up the GPIO pins
                         #GPIO.cleanup()      
                    if key == ord('8'):
                            
                            # Open the saved video file
                            saved_video = cv2.VideoCapture(filename2)
                            saved_video.set(cv2.CAP_PROP_FPS, fps)
                            frame_count = 0


                            while True:
                                # Read the next frame from the saved video file
                                ret, frame5 = saved_video.read()
                                if not ret:
                                    break

                                cv2.imshow('angio sim', frame5)

                                # Wait for a short time between frames
                                key = cv2.waitKey(1)

                                if key == ord('7'):
                                  exit()

                            frame_count += 1

                            # End of video file
                            saved_video.release()
                            print("End of video file ({} frames)".format(frame_count))

                            print('8_released')
                    else:
                      key=cv2.waitKey(1) 
                 else:
                      key=cv2.waitKey(1)      

video_writer.release()                 