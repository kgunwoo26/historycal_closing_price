import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

price_List = list()
compare_list = list()
pre_list = list()

pre_date = None
g = 1
update_period = 6
check_term = 6
money = 100_000

check_date = datetime(2005, 6, 7)


# check_date = date + relativedelta(months=check_term)

def date_to_string(date):  # 날짜 스트링 형태로 변경
    d_year = str(date.year)
    year = d_year[2:]
    month = date.month
    day = date.day
    if date.month < 10:
        month = f"0{date.month}"
    if date.day < 10:
        day = f"0{date.day}"
    return f"{year}/{month}/{day}"


def cal_gap(new_val, old_val):  # 전 시점 대비 수익률 계산
    # print("\nentered")
    # if old_val != '' and new_val !='':
    #     print(float(old_val)," -> ",float(new_val))
    #     print("<",(float(new_val) / float(old_val) - 1) * 100,">")
    return (float(new_val) / float(old_val) - 1) * 100 if old_val != '' and new_val != '' else ''


check_date_string = date_to_string(check_date)
print(check_date_string)

with open('resources/List_csv3.csv', 'r') as f:
    reader = csv.reader(f)
    name_list = next(reader)

    for i in reader:
        if i[0] == check_date_string:
            price_List.append(i)
            check_date = check_date + relativedelta(months=check_term)
            check_date_string = date_to_string(check_date)
            # print(check_date_string)
        if i[0] >= check_date_string:
            if pre_date is None:
                price_List.append(pre_date)
                check_date = check_date + relativedelta(months=check_term)
                check_date_string = date_to_string(check_date)
                # print(pre_date[0])
        pre_date = i

name_list[0] = "no winner"

for num in price_List:
    # print("\ncompare :")
    # print(pre_list)
    today = num[0]
    if num[0] != check_date_string:

        i = 0
        for price in num:
            if g == 1:
                g = 0
                continue
            if len(pre_list) == len(num) - 1:  # 두번째 달부터
                if len(compare_list) == len(num) - 1:  # 세번째 달부터
                    compare_list[i] = cal_gap(price, pre_list[i])
                else:  # 두번째 달일 경우
                    compare_list.append(cal_gap(price, pre_list[i]))
                pre_list[i] = price
            else:  # 첫번째 달일 경우
                pre_list.append(price)
            i += 1
        g = 1

    if len(compare_list) != 0:
        count_max = 0
        max = -1
        num_max = -1
        for value in compare_list:
            if value != '' and value > max:
                num_max = count_max
                max = value
            count_max += 1

        print("date:", today, "win=", name_list[num_max + 1], "max:", max)
