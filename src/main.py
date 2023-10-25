from check_process import *


db_path, cam_num, student_fee_check, cap, db, student_id_list = config_settings()

scanned_id_list = set_pre_scanned_id_list()
scan_time = 0
        
        
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    cv2.namedWindow('QR Code Scanner', cv2.WINDOW_NORMAL)
    cv2.imshow("QR Code Scanner", frame)
    
    decodedObjects = pyzbar.decode(frame)
    key = cv2.waitKey(1)

    for obj in decodedObjects:
        if obj.type == 'QRCODE':
            student_id = int(obj.data.decode('utf-8')[:10])
            check_student_id(db, student_id, student_id_list, scanned_id_list, student_fee_check, scan_time)
            scan_time = time.time()
            
    if cv2.getWindowProperty('QR Code Scanner', cv2.WND_PROP_VISIBLE) < 1:
        break
    
cap.release()
cv2.destroyAllWindows()

