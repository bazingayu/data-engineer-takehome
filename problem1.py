import os
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# This is a basic face detector with opencv
# In my previous job, I took in charge of lots of detection, segmentation and landmarks of human body.
# I think my experiences fits the job well.

def face_detection(image_path, target_dir):
    # if the target_dir not exist, make the target dir
    os.makedirs(target_dir, exist_ok=True)
    # read and grayscale the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # draw & save the cropped image
    for index, (x, y, w, h) in enumerate(faces):
        # draw rectangle
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # crop face & save face to target folder
        crop_face = image[y: y+h, x: x+w]
        target = os.path.join(target_dir, "face_" + str(index) + ".jpg")
        cv2.imwrite(target, crop_face)
    # show the faces in original image
    cv2.imshow("win", image)
    cv2.waitKey()

face_detection(image_path="test.png", target_dir="output")




