# 파이썬에서 제공되는 라이브러리
import sys
import datetime

# PyQt5 라이브러리
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

# 금융처리를 위한 라이브러리
import FinanceDataReader as fdr

# UI 불러오기
try:
    form_class = uic.loadUiType("finance_main.ui")[0]
except:
    print("UI 파일을 찾을 수 없습니다. UI 파일이 있는지 확인하세요.")
    sys.exit()
    
# 전역변수
tickets = ['005930', '003550', '000880', '000150', '035720']

# 현재 값 가져오기 ( 숫자에 , 넣은 값을 리턴)
def get_current_ticker(df_data):
    iClose = df_data[-1:]['Close'].values[0]
    return format(iClose, ',')

# 5일 평균 가져오기 ( 숫자에 , 넣은 값을 리턴)
def get_5day_avg(df_data, day=5):
    # 5일 평균 구하기
    ma5 = df_data['Close'].rolling(window=day).mean()
    # 5일 평균 실수 형태의 정수의 , 값으로 변환
    day5 = int(ma5[-2])

    today_data = df_data[-1:]['Close'].values[0]
    # 5일 평균과 현재가 비교하여 상승 하락 여부 판단
    if today_data < day5:
        updown = "하락중"
    elif today_data == day5:
        updown = "보합"
    else:
        updown = "상승중"
    return format(day5, ','), updown

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnClose.clicked.connect(self.close_clicked)
        self.get_stock_data()

        # 타임함수 설정
        timer = QTimer(self)
        timer.start(5000)
        timer.timeout.connect(self.timer_show)

        # 테이블 넓이 데이터에 맞게 조절
        self.tbl_finance.resizeColumnsToContents()

    def timer_show(self):
        # print("타이머 작동중..")
        self.get_stock_data()
        
    # 주식정보 불러오는 함수
    def get_stock_data(self):
        for idx, ticker in enumerate(tickets):
            # 셀에 값 변경
            self.tbl_finance.setItem(idx, 0, QTableWidgetItem(ticker))
            # 리스트의 주가정보 가져오기(현재값)
            df_ticker = fdr.DataReader(ticker, '2025-01-01')
            self.tbl_finance.setItem(idx, 1, QTableWidgetItem(get_current_ticker(df_ticker)))
            #5일 평균, 상승, 하락 함수
            day5, updown = get_5day_avg(df_ticker)
            self.tbl_finance.setItem(idx, 2, QTableWidgetItem(str(day5)))
            self.tbl_finance.setItem(idx, 3, QTableWidgetItem(updown))
        # 오늘 날짜 가져오기
        now = datetime.datetime.now()    
        self.lb_date.setText('갱신일자 : ' + now.strftime("%Y-%m-%d %H:%M:%S"))

    def close_clicked(self):
        btnResult = QMessageBox.question(self, "종료", "정말 종료하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if btnResult == QMessageBox.Yes:
            self.close()
        else:
            pass

app = QApplication(sys.argv)
win = MyWindow()
win.show()
app.exec_()

