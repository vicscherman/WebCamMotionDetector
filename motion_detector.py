import cv2, time, pandas
from datetime import datetime

first_frame= None
#triggering primary webcam
video= cv2.VideoCapture(0)
motion_list =[None,None]
times=[]
df=pandas.DataFrame(columns=["Start", "End"])

#frame counter
frames=0

while True:
   
    frames= frames+1
    check, frame = video.read()
    #flip everything on x axis so it's mirror imaged
    frame = cv2.flip(frame, 1)
    #our motion detected status(0 is no motion detected, 1 is motion detected)
    motion_detected=0
    # render in black and white, w/ blur, mirrored in x axis
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray= cv2.GaussianBlur(gray, (21,21), 0)
   
    
    
    if first_frame is None:
        first_frame = gray
        continue
    #  We'll calibrate this by initializing the webcam with no motion, therefore any pixel changes after frame 1 are stored in this variable   
    delta_frame=cv2.absdiff(first_frame,gray)
    #setting motion threshold, difference of 30 gets white pixel assigned. Returns second item of tuple( actual returned frame)
    thresh_frame= cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # smoothing out the white areas in our threshold frame using the dilate method
    thresh_frame = cv2.dilate(thresh_frame, None, iterations= 10)
   
    #all the contours of our threshold frames
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #our contour filter, if the movement area is greater than 10000 pixels, we draw a square rectangle around it. Greater values means less sensitivity. This value depends on your webcam resolution, view distance etc
    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        else:
            motion_detected=1
            (x,y,w,h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

    motion_list.append(motion_detected)
    
    if motion_list[-1]==1 and motion_list[-2]==0:
        times.append(datetime.now())

    if motion_list[-1]==0 and motion_list[-2]==1:
        times.append(datetime.now())

    cv2.imshow("Gray frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Green Rectangle", frame)


    #re render every 1 milliscecond
    key=cv2.waitKey(1)
    
    #to exit
    if key==ord('q'):
        if motion_detected ==1:
            times.append(datetime.now())
        break
    
print(motion_list)
print(times)
# going through our datetimestamp list jumping 2 values each iteration. This is to log the start and end times of motion appearing in our dataframe
for i in range(0, len(times),2):
    df=df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)

#creating csv file of motion log
df.to_csv("MotionLog.csv")
    

print(frames)
video.release()
cv2.destroyAllWindows