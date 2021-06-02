import cv2
import sqlite3
import datetime

now = datetime.datetime.now()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.EigenFaceRecognizer_create()
recognizer.read('recongniger\\trainningdata.yml')

def getProfile(mssv):
    conn = sqlite3.connect('sv.db')
    query = "SELECT * FROM sinhvien WHERE MSSV="+str(mssv)
    curror = conn.execute(query)
    profile = None 
    for row in curror:
        profile = row
    conn.close()
    return profile
index = None
cap = cv2.VideoCapture(0)
fontFace = cv2.FONT_ITALIC
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale( # detect khuôn mặt
        gray,
        scaleFactor = 2,
        minNeighbors=5,
        flags = 0,
        minSize = (50, 50)
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3) 
        roi_color = frame[y:y+h, x:x+w] # xắt ảnh theo khung khuôn mặt vừa vẽ
        roi_gray = gray[y:y+h, x:x+w] # chuyeenr thành màu xám
        roi_gray = cv2.resize(roi_gray,(256,256)) #thay đổi kích thước cùng với tệp dataset
        MSSV, confidence = recognizer.predict(roi_gray) #tiến hành nhận dạng bằng model vừa train được trả về ID và độ tin cậy
        check = False
        
        if True:
            if confidence >=10000:
                profile = getProfile(MSSV)
                if(profile != None):
                    check = True
                    print(confidence,"phan tram la "+str(profile[1]))
                    cv2.putText(
                        frame, ""+str(profile[1]), (x+10, y+h+30), fontFace, 1, (0, 255, 0), 2)
                conn = sqlite3.connect('sv.db')
                query = "SELECT * FROM diemdanh WHERe MSSV="+str(MSSV)
                curr = conn.execute(query)
                isRecordExit = 0
                for row in curr:
                    if row[3] == now.day: #nếu trong database chưa ghi nhận điểm danh trong ngày hôm nay của SV đó thì tiến hành điểm danh nếu nhận đc khuôn mawtjphuf hợp
                        isRecordExit = 1
                if(isRecordExit == 0):
                    query = "INSERT INTO diemdanh VALUES("+str(MSSV) + \
                        ",'"+str(now)+"','" + \
                        str(check) + "','"+str(now.day)+"')"
                    cv2.putText(frame, "Done !", (x, y+h-60),
                            fontFace, 1, (241, 175, 0), 3)
                else:
                    if now.hour > 6: # nếu giờ điểm danh lớn hơn 6 thì là đi muộn
                        check = False
                        cv2.putText(frame, "Too Late", (x, y+h+60),
                            fontFace, 1, (72, 150, 32), 2)
                    else:
                        cv2.putText(frame, "OK", (x, y+h+60),
                            fontFace, 1, (72, 150, 32), 2)

                conn.execute(query)
                conn.commit()
                conn.close()
            else:
                print(confidence," phan tram cung co the la",MSSV) # nếu độ chính xác chưa đủ thì có thể gần đúng với ID nào
                cv2.putText(frame, "Unknow", (x+10, y+h+30),
                        fontFace, 1, (0, 0, 255), 2)
    frame = cv2.resize(frame, (900, 680))
    cv2.imshow('image', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
