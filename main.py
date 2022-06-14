import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import pandas_datareader as pdr

update_period = 6  # 포트폴리오 정비 주기
check_term = 12  # 조사 주기
seed_money = 50
file_name = 'resources/List_csv3.csv'
snp_file_name = 'resources/S&P 500 내역.csv'
target_date = datetime(2022, 6, 7)  # 기준 날짜 설정, 최대 22/06/07

start_date = target_date
date_list = list()
snp_data = list()

def date_to_string_month(date: datetime) -> str:  # 날짜 스트링 형태로 변경
    return date.strftime('%y/%m')

def date_to_string(date: datetime) -> str:  # 날짜 스트링 형태로 변경
    return date.strftime('%y/%m/%d')

while '05/06/07' < date_to_string(start_date):  # 기준 날짜와 정비 주기 기준으로 시작 날짜 설정
    date_list.append(date_to_string_month(start_date))
    start_date = start_date + relativedelta(months=-update_period)

temp = date_list[::-1]
date_list =temp
check_date = start_date + relativedelta(months=update_period)


def cal_gap(new_val: float, old_val: float):  # 전 시점 대비 수익률 계산
    if old_val != '' and new_val != '':
            # and type(old_val) is not str and type(new_val) is not str:
        exp = ((float(new_val) / float(old_val) )- 1) * seed_money
        return exp
        # (float(new_val) / float(old_val) - 1) * 100 if float(old_val) != '' and float(new_val) != '' else ''
    else:
        return ''

def load_snp_list():
    data = list()
    with open(snp_file_name , 'r') as f:
        reader = csv.reader(f)
        next(reader)  # 종목명 열 패스
        for i in reader:
            rate = i[6].split("%")[0]
            data.append(rate)
    return data

# def get_snp500(start_date: datetime.datetime, end_date: datetime.datetime) -> float:
#     close_datas = pdr.get_data_yahoo('^GSPC', start_date, end_date)['Close']
#
#     ## For check datas from yahoo finance.
#     # for data in close_datas:
#     #     print(data)
#
#     first_value = close_datas[0]
#     last_value = close_datas[close_datas.size - 1]
#
#     print(f'start date\'s value is {first_value} ({start_date})')
#     print(f'last date\'s value is {last_value} ({end_date})')
#
#     revenue = last_value - first_value
#
#     return revenue

def create_compare_list(date, term):
    mcheck_term = term
    check_date= date
    check_date_List = list()
    compare_list = list()
    check_date_string = date_to_string(check_date)
    pre_list = list()
    p_found = c_found = 0
    pre_date = None

    with open(file_name , 'r') as f:
        reader = csv.reader(f)
        next(reader)  # 종목명 열 패스

        for i in reader:
            if i[0] == check_date_string and p_found == 0:  # 날짜를 찾은 경우
                pre_list.append(i)
                check_date = check_date + relativedelta(months=mcheck_term)  # TODO: Assigning values to parameter is awkward.
                check_date_string = date_to_string(check_date)
                p_found = 1
            elif i[0] >= check_date_string and p_found == 0:
                if pre_date != None and len(pre_date) != 0:
                    pre_list.append(pre_date)
                    # TODO: What is different with line 64-66? - 해당 날짜에 없을 경우 (6월 7일 휴장인 경우) 그 이전 데이터 가져오도록 구분했습니다
                    check_date = check_date + relativedelta(months=mcheck_term)
                    check_date_string = date_to_string(check_date)
                    p_found = 1

                    # print(pre_date[0])
            pre_date = i  # 마지막 조회 날짜 저장

            if i[0] == check_date_string and c_found == 0:  # 날짜를 찾은 경우
                check_date_List.append(i)
                break
                # print(check_date_string)
            elif i[0] >= check_date_string and c_found == 0:
                if pre_date != 0:
                    check_date_List.append(pre_date)
                    break
            pre_date = i  # 마지막 조회 날짜 저장

    # print(check_date_List)
    # print(pre_list)
    for num in check_date_List:
        i = 0
        for price in num:
            if len(pre_list) != 0 and i!=0:  # To prevent out of index of `pre_list`.
                compare_list.append(cal_gap(price, pre_list[0][i]))
            i += 1

    return compare_list


def create_snp_list(date, term):
    mcheck_term = term
    check_date= date
    check_date_string = date_to_string(check_date)
    p_found = c_found = 0

    pre_value = None
    new_value = None

    pre_date = None

    with open(snp_file_name , 'r') as f:
        reader = csv.reader(f)
        next(reader)  # 종목명 열 패스

        for i in reader:
            if i[0] == check_date_string and p_found == 0:  # 날짜를 찾은 경우
                if len(i[1].split(",")) > 1:
                    value = i[1].split(",")
                    pre_value = float(value[0]) * 1000 + float(value[1])
                else:
                    pre_value = i[1]
                check_date = check_date + relativedelta(months=mcheck_term)  # TODO: Assigning values to parameter is awkward.
                check_date_string = date_to_string(check_date)
                p_found = 1
            elif i[0] >= check_date_string and p_found == 0:
                if pre_date != None and len(pre_date) != 0:
                    if len(pre_date.split(",")) >1:
                        value = pre_date.split(",")
                        pre_value =float(value[0]) *1000 + float(value[1])
                    else :
                        pre_value = pre_date
                    # TODO: What is different with line 64-66? - 해당 날짜에 없을 경우 (6월 7일 휴장인 경우) 그 이전 데이터 가져오도록 구분했습니다
                    check_date = check_date + relativedelta(months=mcheck_term)
                    check_date_string = date_to_string(check_date)
                    p_found = 1

                    # print(pre_date[0])
            pre_date = i[1]  # 마지막 조회 날짜 저장

            if i[0] == check_date_string and c_found == 0:  # 날짜를 찾은 경우
                if pre_date != None and len(pre_date) != 0:
                    if len(i[1].split(",")) > 1:
                        value = i[1].split(",")
                        new_value = float(value[0])* 1000 + float(value[1])
                    else :
                        new_value = i[1]
                break
                # print(check_date_string)
            elif i[0] >= check_date_string and c_found == 0:
                if pre_date != 0:
                    if len(pre_date.split(",")) >1:
                        value = pre_date.split(",")
                        new_value = float(value[0])  * 1000 + float(value[1])
                    else :
                        new_value = pre_date
                    break
            pre_date = i[1]  # 마지막 조회 날짜 저장

    if new_value == None:
        return 1
    else:
        result = float(cal_gap(new_value, pre_value))
        return result


def find_stock_name(num):
    with open(file_name , 'r') as f:
        reader = csv.reader(f)
        name_list = next(reader)  # 종목명 열 패스
    return name_list[num]


def cal_highest_stock(date, term ):
    check_date = date
    check_term = term
    best_stock: str

    num_max = -1
    check_date = check_date + relativedelta(months=-check_term)
    compare_list = create_compare_list(check_date,check_term)

    if len(compare_list) != 0:  # max값을 지정
        count_max = 0
        max = -100
        for value in compare_list:
            if value != '' and value > max:
                num_max = count_max
                max = value
            count_max += 1
        best_stock = num_max + 1;
        # print( "win=", find_stock_name(best_stock), "max:", max)
    return num_max +1



result_list = list()
result_snp_list = list()

def check_earning_dual(date, period ,count):
    check_date = date
    update_period = period
    check_date_string = date_to_string(check_date)
    list_count = count


    with open(file_name , 'r') as f:
        reader = csv.reader(f)

        next(reader)  # 종목명 열 패스

        pre_price = None
        now_price = None

        for i in reader:
            if i[0] == check_date_string :  # 날짜를 찾은 경우

                check_date = check_date + relativedelta(months=update_period)
                check_date_string = date_to_string(check_date)
                now_price = i[result_list[list_count]]
                if pre_price != None and result_list[list_count] != 0:
                    earn_rate = cal_gap(now_price, pre_price)
                    return earn_rate
                pre_price = now_price

            elif i[0] >= check_date_string :
                if len(pre_date) != 0:
                    now_price = pre_date[result_list[list_count]]
                    check_date = check_date + relativedelta(months=update_period)
                    check_date_string = date_to_string(check_date)

                    if pre_price != None and result_list[list_count] != 0:
                        earn_rate = cal_gap(now_price, pre_price)

                        return earn_rate
                    pre_price = now_price

            pre_date = i







def check_earning_relative(date, period ,count):
    check_date = date
    update_period = period
    check_date_string = date_to_string(check_date)
    list_count = count

    with open(file_name , 'r') as f:
        reader = csv.reader(f)

        next(reader)  # 종목명 열 패스

        pre_price = None
        now_price = None

        for i in reader:

            if i[0] == check_date_string :  # 날짜를 찾은 경우

                check_date = check_date + relativedelta(months=update_period)
                check_date_string = date_to_string(check_date)
                now_price = i[result_list[list_count]]
                if pre_price != None and result_list[list_count] != 0:
                    earn_rate = cal_gap(now_price, pre_price)
                    return earn_rate
                pre_price = now_price

            elif i[0] >= check_date_string :
                if len(pre_date) != 0:
                    now_price = pre_date[result_list[list_count]]
                    check_date = check_date + relativedelta(months=update_period)
                    check_date_string = date_to_string(check_date)

                    if pre_price != None and result_list[list_count] != 0:
                        earn_rate = cal_gap(now_price, pre_price)
                        return earn_rate
                    pre_price = now_price

            pre_date = i


date = check_date

while date_to_string(date) <= '22/06/07':
    date = date + relativedelta(months=update_period)
    # print("\n\n", "start date:", check_date)
    result_list.append(cal_highest_stock(date, check_term))



money_list = list()
money_list_snp = list()
money_list_dual = list()
snp_data = load_snp_list()
date = check_date

money =seed_money

for i in snp_data:
    earing = float(i)
    money = money * (earing + 100) / 100
    money_list_snp.append(money)



list_count =0
money =seed_money
date = check_date

penalty =False

while date_to_string(date) <= '22/06/07':   # 듀얼 모멘텀
    # print("\n\n", "start date:", check_date)
    date = date + relativedelta(months=update_period)
    earn_rate =check_earning_dual(date,update_period, list_count)
    snp_rate = float(create_snp_list(date, update_period))
    if type(earn_rate) == float:
        print(money, " ", snp_rate, " ",earn_rate, ":", date)
        if penalty != True:
            money = money* (earn_rate + 100 ) /100
        if snp_rate > earn_rate:
            penalty = True
        else :
            penalty = False
        # else:
        #     print("keep money", earn_rate)

    list_count +=1
    money_list.append(money)



list_count =0
money =seed_money
date = check_date
money_list.clear()

while date_to_string(date) <= '22/06/07':   # 상대 모멘텀
    # print("\n\n", "start date:", check_date)
    date = date + relativedelta(months=update_period)
    earn_rate =check_earning_relative(date,update_period, list_count)
    if type(earn_rate) == float:
        money = money* (earn_rate + 100 ) /100
    list_count +=1
    money_list.append(money)


print(find_stock_name(cal_highest_stock(target_date,check_term)))


total_result =list()
term = 1
period = 1

# while term <=12 and period <= 12:    # 주기별 수익률 계산
#
#
#     while '05/06/07' < date_to_string(start_date):  # 기준 날짜와 정비 주기 기준으로 시작 날짜 설정
#         start_date = start_date + relativedelta(months=-period)
#     date = start_date + relativedelta(months=period)
#
#     while date_to_string(date) <= '22/06/07':
#         date = date + relativedelta(months=period)
#         # print("\n\n", "start date:", check_date)
#         result_list.append(cal_highest_stock(date, term))
#
#     list_count = 0
#     money = seed_money
#     date = check_date
#
#     penalty = False
#
#     while date_to_string(date) <= '22/06/07':  # 듀얼 모멘텀
#         # print("\n\n", "start date:", check_date)
#         date = date + relativedelta(months=period)
#         earn_rate = check_earning_dual(date, period, list_count)
#         snp_rate = float(create_snp_list(date, period))
#         if type(earn_rate) == float:
#             if penalty != True:
#                 money = money * (earn_rate + 100) / 100
#             if snp_rate > earn_rate:
#                 penalty = True
#             else:
#                 penalty = False
#             # else:
#             #     print("keep money", earn_rate)
#
#     print(term,",",period,",",money)
#     list_count += 1
#     period += 1
#     result_list.clear()
#     if period >12:
#         term += 1
#         period = 1
#




size_of_snp_list = len(money_list_snp)
p_num = int(size_of_snp_list / len(money_list))
snp_list = list()

i=0
for i in range(len(money_list)):
    snp_list.append(money_list_snp[p_num*i])

plt.plot(date_list,money_list, label = 'Dual momentum')
plt.plot(date_list,snp_list, label = 'S&P')
plt.legend(loc='best', ncol =1, fontsize =10, frameon=True, shadow = True)
plt.xlabel("date")
plt.ylabel("money")
plt.show()


