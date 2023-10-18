import cv2
import pyzbar.pyzbar as pyzbar

import pandas as pd
import openpyxl
import winsound as ws
import time

from settings import Settings

from collections import deque
import sys


def config_settings() -> tuple:
    """프로그램 설정 함수

    Returns:
        tuple(str, int, bool, cv2.VideoCapture, pd.DataFrame, list): 설정된 데이터베이스 경로, 카메라 번호, 회비 납부 확인 여부, 카메라 객체, 데이터베이스, 학생의 학번 리스트
    """
    
    db_path = ''
    cam_num = 0
    student_fee_check = ''
    
    settings = Settings(db_path, get_num_of_cam(), cam_num, student_fee_check)
    settings.display()
    
    db_path = settings.db_path
    cam_num = settings.cam_num
    student_fee_check = settings.student_fee_check
    
    cap = cv2.VideoCapture(cam_num)
    
    db = pd.read_csv(db_path, usecols=[1, 2, 3]).dropna(subset=['student_id'])
    student_id_list = db['student_id'].tolist()
    
    for i in range(len(student_id_list)):
        if student_id_list[i].isdigit():
            student_id_list[i] = int(student_id_list[i])
        else:
            student_id_list[i] = 0

    return (db_path, cam_num, student_fee_check, cap, db, student_id_list)

def set_pre_scanned_id_list() -> deque:
    """이전에 인증된 학생의 학번 리스트 설정 함수

    Returns:
        deque: 이전에 인증된 학생의 학번 리스트
    """
    
    scanned_id_list = deque()
    
    try:
        student_data = pd.read_excel('student_data.xlsx', sheet_name=time.strftime('%Y-%m-%d'), engine='openpyxl')
        scanned_id_list = deque(student_data['학번'].tolist())
    except FileNotFoundError:
        wb = openpyxl.Workbook()
        sheet = wb.create_sheet(time.strftime('%Y-%m-%d'))
        sheet.append(['학번', '이름'])
        wb.save('student_data.xlsx')
            
    return scanned_id_list

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

def is_dues_checked(db: pd.DataFrame, student_fee_check: bool, student_id: int) -> bool:
    """회비 납부 확인 함수

    Args:
        db (pd.DataFrame): 데이터베이스
        student_fee_check (bool): 회비 납부 확인 여부
        student_id (int): 학생의 학번

    Returns:
        bool: 회비 납부 여부
    """
    
    if not student_fee_check:
        return True
    else:
        return True if db[db['student_id'] == student_id]['dues'].tolist()[0] == 1 else False

def confirm_student(db: pd.DataFrame, student_id: int, scanned_id_list: deque) -> None:
    """학생 인증 확인 함수

    Args:
        db (pd.DataFrame): 데이터베이스
        student_id (int): 학생의 학번
        scanned_id_list (deque): 인증된 학생의 학번 리스트
    """
    
    ws.Beep(1000, 100)
    
    scanned_id_list.append(student_id)
    
    wb = openpyxl.load_workbook('student_data.xlsx')
    sheet = wb[time.strftime('%Y-%m-%d')]
    sheet.append([student_id, db[db['student_id'] == str(student_id)]['name'].tolist()[0]])
    wb.save('student_data.xlsx')
    
    print(f'학번 : {student_id}')
    print('인증되었습니다.')
    print('----------------------------------\n')
    
def deny_dues_not_paid(student_id: int) -> None:
    """미납 회비 거부 함수

    Args:
        student_id (int): 학생의 학번
    """
    
    ws.Beep(1500, 50)
    ws.Beep(1500, 50)
    
    print(f'학번 : {student_id}')
    print('회비 미납부 학생입니다.')
    print('----------------------------------\n')
    
def deny_overlap_student(student_id: int) -> None:
    """학생 중복 인증 거부 함수

    Args:
        student_id (int): 학생의 학번
    """
    
    ws.Beep(500, 50)
    ws.Beep(500, 50)
    
    print(f'학번 : {student_id}')
    print('이미 배부받은 학생입니다.')
    print('----------------------------------\n')
    
def deny_unknown_student(student_id: int) -> None:
    """학생 미인증 거부 함수

    Args:
        student_id (int): 학생의 학번
    """
    
    ws.Beep(1500, 400)
    
    print(f'학번 : {student_id}')
    print('미등록 학생입니다.')
    print('----------------------------------\n')
    
def check_student_id(db: pd.DataFrame, student_id: int, student_id_list: list, \
    scanned_id_list: deque, student_fee_check: bool, scan_time: time) -> None:
    """학생 인증 확인 함수

    Args:
        db (pd.DataFrame): 데이터베이스
        student_id (int): 학생의 학번
        student_id_list (list): 학생의 학번 리스트
        scanned_id_list (deque): 인증된 학생의 학번 리스트
        student_fee_check (bool): 회비 납부 확인 여부
        scan_time (time): QR코드 스캔 시간
    """
    
    is_registered = student_id in student_id_list
    
    if is_registered:
        is_dues_paid = is_dues_checked(db, student_fee_check, student_id)
        is_scanned = student_id in scanned_id_list
        
        if is_dues_paid:
            if not is_scanned:
                confirm_student(db, student_id, scanned_id_list)
            elif time.time() - scan_time > 3:
                deny_overlap_student(student_id)
        else:
            if time.time() - scan_time > 3:
                deny_dues_not_paid(student_id)
    else:
        if time.time() - scan_time > 3:
            deny_unknown_student(student_id)
