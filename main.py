import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

check_date_List = list()
compare_list = list()
pre_list = list()

update_period = 2  # 포트폴리오 정비 주기
check_term = 6  # 조사 주기
seed_money = 100

target_date = datetime(2022, 6, 7) # 기준 날짜 설정, 최대 22/06/07

start_date = target_date
# check_date = date + relativedelta(months=check_term)


def date_to_string(date: datetime) -> str:  # 날짜 스트링 형태로 변경
    return date.strftime('%y/%m/%d')

while '05/06/07' < date_to_string(start_date):    # 기준 날짜와 정비 주기 기준으로 시작 날짜 설정
    start_date = start_date + relativedelta(months=-update_period)

check_date = start_date + relativedelta(months=update_period)

def cal_gap(new_val: float, old_val: float):  # 전 시점 대비 수익률 계산
    if old_val != '' and new_val != '':
        # print('')
        # print("entered")
        # print(old_val, " -> ", new_val)
        # print("<", str((float(new_val) / float(old_val) - 1) * 100), ">")
        exp = (float(new_val) / float(old_val) - 1) * 100
        return exp
        # (float(new_val) / float(old_val) - 1) * 100 if float(old_val) != '' and float(new_val) != '' else ''
    else:
        return ''

def cal_highest_stock(check_date, check_term):
    pre_date= {} # No reason to use `None` when you even want to use as empty value.
    g = 1
    best_stock: str
    p_found = c_found = 0
    num_max =-1;
    check_date = check_date + relativedelta(months=-check_term)
    check_date_string = date_to_string(check_date)
    print(check_date_string)

    with open('resources/List_csv3.csv', 'r') as f:
        reader = csv.reader(f)
        name_list = next(reader) # 종목명 열 패스

        for i in reader:
            if i[0] == check_date_string and p_found ==0 :   # 날짜를 찾은 경우
                pre_list.append(i)
                check_date = check_date + relativedelta(months=check_term)
                check_date_string = date_to_string(check_date)
                p_found = 1;
                # print(check_date_string)
            elif i[0] >= check_date_string and p_found ==0:
                if len(pre_date) != 0:
                    pre_list.append(pre_date)
                    check_date = check_date + relativedelta(months=check_term)
                    check_date_string = date_to_string(check_date)
                    p_found =1;

                    # print(pre_date[0])
            pre_date = i # 마지막 조회 날짜 저장

            if i[0] == check_date_string and c_found == 0:  # 날짜를 찾은 경우
                check_date_List.append(i)
                break;
                # print(check_date_string)
            elif i[0] >= check_date_string and c_found == 0:
                if pre_date != 0:
                    check_date_List.append(pre_date)
                    break;
            pre_date = i  # 마지막 조회 날짜 저장
    name_list[0] = "no winner"

    for num in check_date_List:
        # print('')
        # print("compare :")
        # print(pre_list)
        today = num[0]
        if num[0] != check_date_string:   # 수익률 compare_list에 저장
            i=0
            for price in num:
                if len(pre_list)!= 0 :
                    compare_list.append(cal_gap(price, pre_list[i]))
                i+=1
            # i = 0
            # for price in num:
            #     if g == 1:
            #         g = 0
            #         continue
            #     if len(pre_list) == len(num) - 1:  # 두번째 달부터
            #         if len(compare_list) == len(num) - 1:  # 세번째 달부터
            #             compare_list[i] = cal_gap(price, pre_list[i])
            #         else:  # 두번째 달일 경우
            #             compare_list.append(cal_gap(price, pre_list[i]))
            #         pre_list[i] = price
            #     else:  # 첫번째 달일 경우
            #         pre_list.append(price)
            #     i += 1
            # g = 1

        if len(compare_list)!= 0:   # max값을 지정
            print("not empty")
            count_max = 0
            max = -1
            num_max = -1
            for value in compare_list:
                if value != '' and value > max:
                    num_max = count_max
                    max = value
                count_max += 1
            best_stock = name_list[num_max + 1] ;
            print("date:", today, "win=", best_stock, "max:", max)
    check_date_List.clear()
    compare_list.clear()
    pre_list.clear()

while date_to_string(check_date) <= '22/06/07':
    print("\n\n", "start date:", check_date)
    check_date = check_date + relativedelta(months=update_period)
    cal_highest_stock(check_date,check_term);

# if num_max != -1 and compare_list[num_max] != '':  # TODO: 마지막 수익률 못 구해 코드 위치 수정 필요
#     money = money * float(compare_list[num_max] + 100) / 100
#     print(compare_list[num_max])
#     print("money:", money);