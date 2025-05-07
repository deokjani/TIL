import FinanceDataReader as fdr
import pandas as pd

# 국내주식
df_krx = fdr.StockListing('KRX')
print(df_krx)

# 미국 S&P500
df_nasdaq = fdr.StockListing('NASDAQ')
print(df_nasdaq)

# 삼성전자 조회
df_samsung = fdr.DataReader('005930', '2025-01-01')
print(df_samsung)
print(df_samsung[-1:]['Close'].values[0])