import cv2
import os.path
import sqlite3

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")

def InsertOrUpdate(mssv, name, lop, email):
    conn = sqlite3.connect('sv.db')
    query = "SELECT * FROM sinhvien where MSSV="+str(mssv)
    curr = conn.execute(query)
    isRecordExit = 0
    for row in curr:
        isRecordExit = 1
    if(isRecordExit == 0):
        query = "INSERT INTO sinhvien VALUES("+str(mssv) + \
            ",'"+str(name)+"','"+str(lop)+"','"+str(email)+"')"
    else:
        query = "UPDATE sinhvien SET Name = '" + \
            str(name)+"',Class ='"+str(lop)+"',Email ='" + \
            str(email)+"' WHERE MSSV ="+str(mssv)
    conn.execute(query)
    conn.commit()
    conn.close()


# input data
mssv = input("Nhap MSSV: ")
name = input("Nhap Ten: ")
lop = input("Nhap Lop: ")
email = input("Email: ")
InsertOrUpdate(mssv, name, lop, email)

video = cv2.VideoCapture(2)
smlNum = 0
while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        frame_crop  = gray[y: y+ h, x: x+w]
        if not os.path.exists('Dataset'):
            os.makedirs('Dataset')
        smlNum += 1
        if smlNum >200 :
            break
        if frame_crop is not None:
            frame_crop = cv2.resize(frame_crop,(256,256))
            cv2.imwrite('Dataset/'+str(name)+'.'+str(mssv) +'.'+str(smlNum)+'.jpg', frame_crop)
    if ret:
        cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
