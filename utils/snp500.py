import datetime
import pandas_datareader as pdr


def get_snp500(start_date: datetime.datetime, end_date: datetime.datetime) -> float:
    close_datas = pdr.get_data_yahoo('^GSPC', start_date, end_date)['Close']

    ## For check datas from yahoo finance.
    # for data in close_datas:
    #     print(data)

    first_value = close_datas[0]
    last_value = close_datas[close_datas.size - 1]

    print(f'start date\'s value is {first_value} ({start_date})')
    print(f'last date\'s value is {last_value} ({end_date})')

    revenue = last_value - first_value

    return revenue


# Test codes.
# revenue = get_snp500(start_date= datetime.datetime(2010, 1, 4), end_date= datetime.datetime(2022, 6, 12))
# print('')
# print('revenue')
# print(revenue)
