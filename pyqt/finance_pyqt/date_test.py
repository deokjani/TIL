import datetime

# 오늘 날짜 구하기
now = datetime.datetime.now()
print("오늘 날짜:", now)

# 2025년 1월 1일 12시 12분 12초
print(now.strftime("%Y년 %m월 %d일 %H시 %M분 %S초"))