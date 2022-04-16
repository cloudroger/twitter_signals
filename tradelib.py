import csv

#Getting Data from CSV files
def csv_get(filename, position_list, skipto_truenum_index=False, **kwargs):
    with open(filename, "r+", encoding="utf-8", errors="ignore") as file:
        skiptype = type(skipto_truenum_index)
        reader = csv.reader(file)
        next(reader)
        nested_list = []
        for _ in position_list:
            nested_list.append([])
        for row in reader:
            if skiptype == int:
                try:
                    float(row[skipto_truenum_index])
                except:
                    continue
            for i, pos in enumerate(position_list):
                nested_list[i].append(float(row[pos]))
    return(nested_list)


def moving_average_list(ma, value_list, lagged=False, **kwargs):
    ma_list = []
    if lagged:
        offset = 0
    else:
        offset = 1
    for i in range(ma-offset):
        ma_list.append(None)
    for i, value in enumerate(value_list[ma-offset:], start=ma-offset):
        ma_list.append((sum(value_list[i-ma+offset:i+offset]))/ma)
    return ma_list





