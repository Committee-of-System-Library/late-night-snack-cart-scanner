from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog

class Settings:
    def __init__(self, db_path, num_of_cam, cam_num, student_fee_check):
        self.db_path = db_path
        self.num_of_cam = num_of_cam
        self.cam_num = cam_num
        self.student_fee_check = student_fee_check
        
        self.db_path_entry = None
        self.cam_num_cb = None
        self.student_fee_check_cb = None
        
        
    def browse_db_path(self):
        self.db_path = filedialog.askopenfilename(initialdir = "./", title = "Select a File", filetypes = (("csv files", "*.csv"), ("xml files", "*.xml"), ("all files", "*.*")))
        self.db_path_entry.delete(0, END)
        self.db_path_entry.insert(0, self.db_path)
        
    def set_window(self):
        self.window = Tk()
        self.window.title("QR Code Scanner")
        self.window.geometry("350x200+100+100")
        self.window.resizable(False, False)
        
        
        # 데이터베이스 경로
        db_path_frame = LabelFrame(self.window, text="데이터베이스 경로")
        db_path_frame.pack(fill="both", expand=True)
        
        self.db_path_entry = Entry(db_path_frame, width=30)
        self.db_path_entry.pack(side="left", fill="both", expand=True, pady=7)
        
        browse_btn = Button(db_path_frame, text="찾아보기", command=self.browse_db_path)
        browse_btn.pack(side="right", fill="both", expand=True)
        
        
        # 카메라 번호 선택
        cam_num_frame = LabelFrame(self.window, text="카메라 번호 선택")
        cam_num_frame.pack(fill="both", expand=True, pady=7)
        
        cam_num = [i for i in range(self.num_of_cam)]
        self.cam_num_cb = ttk.Combobox(cam_num_frame, height=5, state="readonly", values=cam_num)
        self.cam_num_cb.pack()
        self.cam_num_cb.current(0)
        
        
        # 회비 납부 확인 여부
        student_fee_check_frame = LabelFrame(self.window, text="회비 납부 확인 여부")
        student_fee_check_frame.pack(fill="both", expand=True)
        
        student_fee_check = ["미납", "납부"]
        self.student_fee_check_cb = ttk.Combobox(student_fee_check_frame, height=5, state="readonly", values=student_fee_check)
        self.student_fee_check_cb.pack()
        self.student_fee_check_cb.current(0)
        
        
        # 프로그램 실행 버튼
        start_btn_frame = Label(self.window)
        start_btn_frame.pack(fill="both", expand=True)
        
        start_btn = Button(start_btn_frame, text="실행", width=10, height=2, command=self.start)
        start_btn.pack()
        
    def display(self):
        self.set_window()
        self.window.mainloop()
        
    def start(self):
        self.db_path = self.db_path_entry.get()
        self.cam_num = int(self.cam_num_cb.get())
        self.student_fee_check = False if self.student_fee_check_cb.get() == "미납" else True
        
        self.window.destroy()
        