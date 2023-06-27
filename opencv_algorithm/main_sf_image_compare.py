import cv2
import face_recognition

img1 = cv2.imread("Messi1.webp")
rgb_img = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img_encoding = face_recognition.face_encodings(rgb_img)[0]

img2 = cv2.imread("images/Victoire.jpg")
rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]

result = face_recognition.compare_faces([img_encoding], img_encoding2)
print("Result: ", result)

# on ouvre la premier frame
cv2.imshow("Img 1", img1)
cv2.imshow("Img 2", img2)
cv2.waitKey(0)