import FinanceDataReader as fdr
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime, timedelta
# Pandas 표기 설정
pd.options.display.float_format = '{:.1f}'.format # 소수점 4자리까지 표기
pd.set_option('display.max_columns', None) # Dataframe 출력시 컬럼 생략없이 전체 표기

df_nasdaq = fdr.StockListing('NASDAQ')
nasdaq = df_nasdaq.Symbol.tolist() # 나스닥 상장 종목명 로드
nasdaq_list = nasdaq[:1000] # 1000번째 종목까지 가져옴
start_day = datetime(2005,6,8) # 시작일
end_day = datetime(2022,6,8) # 종료일

def get_price_data(x):
    df_price = pd.DataFrame(columns=x)
    for ticker in x:
        try:
            df_price[ticker] = pdr.get_data_yahoo(ticker, start_day, end_day)['Adj Close']
        except:
            df_price[ticker] =None # 해당 일자에 종가가 존재하지 않을 경우 None을 표시
    return df_price

closing_price = get_price_data(nasdaq_list)
closing_price.to_csv('closing_Price(Nasdaq).csv',float_format= '%.4f') # 소수점 4번째 자리까지만 출력
print(nasdaq_list)






