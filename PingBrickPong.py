import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
# Importing all images

imgBackground = cv2.imread("assets/background.png")
imgGameWon = cv2.imread("assets/imgGameWon.png")
imgGameOver = cv2.imread("assets/gameoverrr.png")
imgBall = cv2.imread("assets/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("assets/bat.png", cv2.IMREAD_UNCHANGED)
imgRedB = cv2.imread("assets/redbrickr.png", cv2.IMREAD_UNCHANGED)
imgYellowB = cv2.imread("assets/yellowbrickr.png", cv2.IMREAD_UNCHANGED)
imgGreenB = cv2.imread("assets/greenbrickr.png", cv2.IMREAD_UNCHANGED)




# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)


# Variables
ballPos = [615, 155]
speedX = 15
speedY = 15
gameOver = False
gameWon = False
score =  0
h1, w1, _ = imgBat1.shape
print(imgBat1.shape)
print("ball",imgBall.shape)
#no of hit remaining of a brick
redHit = [3]*10
yellowHit = [2]*10
greenHit = [1]*10
BrickHiT = False
# hitting each brick changes the direction of speedY and there might be case where the ball
#  will stuck between bricks doing zigzag motion , so to avoid that  i am using a Flag BrickHit
# so  if it hits the brick then it only changes direction onces and then tha flag is reseted to 
# false if it hits the bat again : if hit brick -> BrickHit = True 
# or if hit bat -> BrickHit = False again ,So The ball can only hit one brick at a oscillation
while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()
    
    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)  # with draw
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)
    
    # on=verlaying brick images  using for loop if the brick hit is remaining or greater 
    # than zero then only ver lay the images 
    X_rbrick = 15
    for i in redHit:
        if i>0:
            img = cvzone.overlayPNG(img, imgRedB, (X_rbrick,10))
        X_rbrick += 105
    X_ybrick= 15
    for i in yellowHit:
        if i>0:
            img = cvzone.overlayPNG(img, imgYellowB, (X_ybrick,10+41+5))
        X_ybrick += 105
    X_gbrick = 15
    for i in greenHit:
        if i>0:
            img = cvzone.overlayPNG(img, imgGreenB, (X_gbrick,10+41+5+41+5))
        X_gbrick += 105


    if BrickHiT==False:
        if (ballPos[1] < 143) & (greenHit[(ballPos[0] +25)// 104]>0):
            speedY = -speedY
            greenHit[ballPos[0] // 104] -= 1
            BrickHiT = True
#uncomment if you want print the coordiates of ball and the remaining hit , brickhit flag
            # print("greenHit",greenHit,ballPos,BrickHiT)
            if greenHit[ballPos[0] // 104] == 0:
                score += 10

    if BrickHiT==False:            
        if (ballPos[1] < 97) & (yellowHit[(ballPos[0] +25)// 104]>0):
            speedY = -speedY
            yellowHit[ballPos[0] // 104] -= 1
            BrickHiT = True
#uncomment if you want print the coordiates of ball and the remaining hit , brickhit flag
            # print("yellowHit",yellowHit,ballPos,BrickHiT)
            if yellowHit[ballPos[0] // 104] == 0:
                score += 20

    if BrickHiT==False:        
        if (ballPos[1]< 51) & (redHit[(ballPos[0] +25)// 104]>0):
            speedY = -speedY
            redHit[ballPos[0] // 104] -= 1
            BrickHiT =True
#uncomment if you want print the coordiates of ball and the remaining hit , brickhit flag            
            # print("redHit",redHit,ballPos,BrickHiT)
            if redHit[ballPos[0] // 104] == 0:
                score += 30

    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            
            x1 = x - w1 // 2
            x1 = np.clip(x1, 15, 1000)
            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (x1,650))
                if (600 < ballPos[1] < (600 + h1)) & (x1 < ballPos[0] < (x1 + w1)):
                    speedY = -speedY
                    ballPos[1] -= 30
                    score += 1
                    BrickHiT = False
                    

            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat1, (x1,650))
                if (600 < ballPos[1] < (600 + h1)) & (x1 < ballPos[0] < (x1 + w1)):
                    speedY= -speedY
                    ballPos[1] -= 30
                    score += 1
                    BrickHiT = False
                    

    # if sum of all hit is equal or less than zero than all the bricks are broken and game is won  
    if (sum(redHit) + sum(greenHit) + sum(yellowHit))<=0:
        gameWon = True

    if gameWon :
        img = imgGameWon
        cv2.putText(img, str(score).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
                    2.5, (200, 0, 200), 5)

#if ball gets out of below frame
    if ballPos[1] > 650:
        gameOver = True
    if gameOver:
        img = imgGameOver
        cv2.putText(img, str(score).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
                    2.5, (200, 0, 200), 5)
    else:
        # Move the Ball
        # if ball hit the right and left side of frame
        if ballPos[0] <= 15 or ballPos[0] >= 1000:
            speedX = -speedX
        # if wall hit the upper frame
        if ballPos[1] <= 15:
            speedY = -speedY
        ballPos[0] += speedX
        ballPos[1] += speedY

        # Draw the ball
        img = cvzone.overlayPNG(img, imgBall, ballPos)
        # showing score in the right side of game
        cv2.putText(img, str(score).zfill(2), (1100, 350), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
       
    #showing minicam of yourself in the upper right corner
    img[10:130, (1270-205):1270] = cv2.resize(imgRaw, (205, 120))

        
   
    # Overlaying the background image
    img = cvzone.overlayPNG(img, imgBall, ballPos)
    cv2.imshow("Brick-Break",img)
    key = cv2.waitKey(1)
    
    # restart the game and set all vribles to initial value
    if key == ord('r'):
        ballPos = [615, 155]
        speedX = 15
        speedY = 15
        gameOver = False
        score = 0
        imgGameOver = cv2.imread("assets/gameoverrr.png")
        # imgGameWon = cv2.imread("assets/")
        redHit = [3]*10
        yellowHit = [2]*10
        greenHit = [1]*10
    
    if key == ord('q'):
        break