import cv2
import pyzbar.pyzbar as pyzbar

from collections import deque
import winsound as ws
import time


cap = cv2.VideoCapture(0)
scanned_id_list = deque()
scan_time = 0

def confirm_student(student_id):
    ws.Beep(1000, 100)
    
    scanned_id_list.append(student_id)
    
    with open('student_id.txt', 'a+') as f:
        f.write(student_id + '\n')
    
    print(f'학번 : {student_id}')
    print('인증되었습니다.')
    print('----------------------------------\n')
    
def deny_overlap_student(student_id):
    ws.Beep(500, 50)
    ws.Beep(500, 50)
    
    print(f'학번 : {student_id}')
    print('이미 배부받은 학생입니다.')
    print('----------------------------------\n')


if __name__ == '__main__':
    try:
        with open('student_id.txt', 'r+') as f:
            for line in f.readlines():
                scanned_id_list.append(line.strip())
    except FileNotFoundError:
        with open('student_id.txt', 'w') as f:
            pass
            
            
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        
        cv2.namedWindow('QR Code Scanner', cv2.WINDOW_NORMAL)
        cv2.imshow("QR Code Scanner", frame)
        
        decodedObjects = pyzbar.decode(frame)
        key = cv2.waitKey(1)

        for obj in decodedObjects:
            if obj.type == 'QRCODE':
                student_id = obj.data.decode('utf-8')[:10]
                if student_id not in scanned_id_list:
                    scan_time = time.time()
                    confirm_student(student_id)
                    
                elif student_id in scanned_id_list and time.time() - scan_time > 3:
                    scan_time = time.time()
                    deny_overlap_student(student_id)
        
        if cv2.getWindowProperty('QR Code Scanner', cv2.WND_PROP_VISIBLE) < 1:
            break
        
        
    cap.release()
    cv2.destroyAllWindows()