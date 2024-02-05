import cv2
import mediapipe as mp
import serial
import time

#Setting up the serial port at 9600 baud rate
ser = serial.Serial("COM7", 9600,8,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE) 

#Image processing algorithm with cv2 and mediapipe libraries used to identify body parts
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

IMAGE_FILES = []
with mp_hands.Hands(static_image_mode=True,
                    max_num_hands=2,
                    min_detection_confidence=0.5) as hands:
                    for idx, file in enumerate(IMAGE_FILES):
                        image = cv2.flip(cv2.imread(file), 1)
                        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    )

# Print handedness and draw hand landmarks on the image.
print('Handedness:', results.multi_handedness)
if not results.multi_hand_landmarks:
    continue
image_height, image_width, _ = image.shape
annotated_image = image.copy()

for hand_landmarks in results.multi_hand_landmarks:
    print('hand_landmarks:', hand_landmarks)
    print(f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
          )
    mp_drawing.draw_landmarks(
        annotated_image,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style())
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    
#For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                    ) as hands:
        
#Activating the camera and performing the necessary operations on it
while cap.isOpened():
    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        continue

# Flip the image horizontally for a later selfie-view display, and convert
# the BGR image to RGB.
image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
image.flags.writeable = False
results = hands.process(image)

# Draw the hand annotations on the image.
image.flags.writeable = True
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        
        # After the image is processed, the desired limb data is extracted from the sequence of limbs recorded as numbered points.
        # Printing to the screen with hand open and closed
        x_basg, y_basg = hand_landmarks.landmark[1].x, hand_landmarks.landmark[1].y
        x_isaretg, y_isaretg = hand_landmarks.landmark[5].x, hand_landmarks.landmark[5].y
        x_ortag, y_ortag = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
        x_yuzukg, y_yuzukg = hand_landmarks.landmark[13].x, hand_landmarks.landmark[13].y
        x_serceg, y_serceg = hand_landmarks.landmark[17].x, hand_landmarks.landmark[17].y
        x_bilek, y_bilek = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y

        x_basuc, y_basuc = hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y
        x_isaretuc, y_isaretuc = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
        x_ortauc, y_ortauc = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y
        x_yuzukuc, y_yuzukuc = hand_landmarks.landmark[16].x, hand_landmarks.landmark[16].y
        x_serceuc, y_serceuc = hand_landmarks.landmark[20].x, hand_landmarks.landmark[20].y

        x_basort, y_basort = hand_landmarks.landmark[2].x, hand_landmarks.landmark[2].y
        x_isaretort, y_isaretort = hand_landmarks.landmark[6].x, hand_landmarks.landmark[6].y
        x_ortaort, y_ortaort = hand_landmarks.landmark[10].x, hand_landmarks.landmark[10].y
        x_yuzukort, y_yuzukort = hand_landmarks.landmark[14].x, hand_landmarks.landmark[14].y
        x_serceort, y_serceort = hand_landmarks.landmark[18].x, hand_landmarks.landmark[18].y

        font = cv2.FONT_HERSHEY_PLAIN
      
#Function that enables the mathematical calculation of the degree information between 0 and 180 to be sent to the servo motors according to the captured pixel point coordinate data.
def   pixels_to_servodegree(uc,g,orta,bilek,tamoran1,tamoran2):
    maxuzama=2*3.14*(g-uc)/4+2*3.14*(orta-uc)/4
    ort=(bilek-g)/(bilek-uc)
    tamoran=tamoran2-tamoran1
            
    optuzama=maxuzama*((ort-tamoran1)/tamoran)
    servodegree=180*(optuzama/maxuzama)
    servodegree=int(round((servodegree),-1)/20)

    if(servodegree<0):
        servodegree=0
    if(servodegree>9):
        servodegree=9
    return servodegree
        
#Servo degree calculator processing of this function by appropriate parameters
servo_bas_degree=pixels_to_servodegree(x_basuc,x_basg,x_basort,x_bilek,0.35,0.95)
servo_isaret_degree=pixels_to_servodegree(y_isaretuc,y_isaretg,y_isaretort,y_bilek,0.53,1.25)
servo_orta_degree=pixels_to_servodegree(y_ortauc,y_ortag,y_ortaort,y_bilek,0.5,1.3)
servo_yuzuk_degree=pixels_to_servodegree(y_yuzukuc,y_yuzukg,y_yuzukort,y_bilek,0.51,1.55)
servo_serce_degree=pixels_to_servodegree(y_serceuc,y_serceg,y_serceort,y_bilek,0.55,1.4)
          
#Printing servo degree information to the screen
cv2.putText(image, "degree : "+str(servo_orta_degree), (10, 50), font, 4, (0, 0, 0), 3)

#Write the servo degree data to the serial port for processing in the microcontroller and wait 100ms after each write.
ser.write((('a'+str(servo_orta_degree))).encode("ASCII"))
time.sleep(0.1)
          
mp_drawing.draw_landmarks(image,
                          hand_landmarks,
                          mp_hands.HAND_CONNECTIONS,
                          mp_drawing_styles.get_default_hand_landmarks_style(),
                          mp_drawing_styles.get_default_hand_connections_style()
                         )
          
#Show the camera on the windows screen. 
cv2.imshow('MediaPipe Hands', image)

if cv2.waitKey(5) & 0xFF == 27:
    ser.close()
    break
    
cap.release()
