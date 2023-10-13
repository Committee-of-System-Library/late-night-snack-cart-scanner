import cv2
import pyzbar.pyzbar as pyzbar

from settings import Settings

from collections import deque
import winsound as ws
import time
import pandas as pd

import sys


def config_settings() -> tuple(str, int, bool, cv2.VideoCapture, pd.DataFrame, list):
    """프로그램 설정 함수

    Returns:
        tuple(str, int, bool, cv2.VideoCapture, pd.DataFrame, list): 설정된 데이터베이스 경로, 카메라 번호, 회비 납부 확인 여부, 카메라 객체, 데이터베이스, 학생의 학번 리스트
    """
    
    db_path = ''
    cam_num = 0
    stu_fee_check = ''
    
    settings = Settings(db_path, get_num_of_cam(), cam_num, stu_fee_check)
    settings.display()
    
    db_path = settings.db_path
    cam_num = settings.cam_num
    stu_fee_check = settings.stu_fee_check
    
    cap = cv2.VideoCapture(cam_num)
    
    db = pd.read_csv(db_path, usecols=[1, 2, 3]).dropna(subset=['student_id'])
    student_id_list = db['student_id'].tolist()
    
    return (db_path, cam_num, stu_fee_check, cap, db, student_id_list)


def get_num_of_cam() -> int:
    """연결된 카메라 개수 확인 함수

    Returns:
        int: 연결된 카메라 개수
    """
    
    num_of_cam = 0
    while True:
        cap = cv2.VideoCapture(num_of_cam)
        if not cap.read()[0]:
            break
        num_of_cam += 1
        cap.release()
            
    return num_of_cam

def confirm_student(student_id, scanned_id_list) -> None:
    """학생 인증 확인 함수

    Args:
        student_id (int): 학생의 학번
        scanned_id_list (deque): 인증된 학생의 학번 리스트
    """
    
    ws.Beep(1000, 100)
    
    scanned_id_list.append(student_id)
    
    with open('student_id.txt', 'a+') as f:
        f.write(student_id + '\n')
    
    print(f'학번 : {student_id}')
    print('인증되었습니다.')
    print('----------------------------------\n')
    
def deny_overlap_student(student_id) -> None:
    """학생 중복 인증 거부 함수

    Args:
        student_id (int): 학생의 학번
    """
    
    ws.Beep(500, 50)
    ws.Beep(500, 50)
    
    print(f'학번 : {student_id}')
    print('이미 배부받은 학생입니다.')
    print('----------------------------------\n')
    
def deny_unknown_student(student_id) -> None:
    """학생 미인증 거부 함수

    Args:
        student_id (int): 학생의 학번
    """
    
    ws.Beep(1500, 400)
    
    print(f'학번 : {student_id}')
    print('미등록 학생입니다.')
    print('----------------------------------\n')


if __name__ == '__main__':
    db_path, cam_num, stu_fee_check, cap, db, student_id_list = config_settings()
    
    scanned_id_list = deque()
    scan_time = 0


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
                if student_id not in scanned_id_list and student_id in student_id_list:
                    scan_time = time.time()
                    confirm_student(student_id, scanned_id_list)
                    
                elif student_id in scanned_id_list and time.time() - scan_time > 3:
                    scan_time = time.time()
                    deny_overlap_student(student_id)
                    
                elif student_id not in student_id_list and time.time() - scan_time > 3:
                    scan_time = time.time()
                    deny_unknown_student(student_id)
        
        if cv2.getWindowProperty('QR Code Scanner', cv2.WND_PROP_VISIBLE) < 1:
            break
        
        
    cap.release()
    cv2.destroyAllWindows()