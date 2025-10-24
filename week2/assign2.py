# Task 1
def func1(name):
    obj1 = {
        "悟空": {"x": 0, "y": 0, "z": 0},
        "丁滿": {"x": -1, "y": 4, "z": 2},
        "辛巴": {"x": -3, "y": 3, "z": 0},
        "貝吉塔": {"x": -4, "y": -1, "z": 0},
        "特南克斯": {"x": 1, "y": -2, "z": 0},
        "弗利沙": {"x": 4, "y": -1, "z": 2},
    }

    target = obj1[name]
    result = {}

    for key, val in obj1.items():
        if key == name:
            continue
        dist = abs(target["x"] - val["x"]) + abs(target["y"] - val["y"])
        if target["z"] != val["z"]:
            dist += 2
        result[key] = dist

    min_dist = min(result.values())
    max_dist = max(result.values())

    nearest = [k for k, v in result.items() if v == min_dist]
    farthest = [k for k, v in result.items() if v == max_dist]

    print(f'最遠{"、".join(farthest)}；最近{"、".join(nearest)}')

func1("辛巴") # print 最遠弗利沙；最近丁滿、貝吉塔
func1("悟空") # print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙") # print 最遠辛巴，最近特南克斯
func1("特南克斯") # print 最遠丁滿，最近悟空


# Task 2
import re
import math

bookings = {}

def func2(ss, start, end, criteria):
    #
    regex = r"([a-zA-Z]+)(>=|<=|=)([a-zA-Z0-9.]+)"
    match = re.match(regex, criteria)
    if not match:
        print("Invalid criteria")
        return

    field = match.group(1)
    operator = match.group(2)
    value = match.group(3)

    #
    candidates = []
    for s in ss:
        isMatch = False
        if field == "name":
            isMatch = s[field] == value
        else:
            numValue = float(value)
            if operator == ">=":
                isMatch = s[field] >= numValue
            elif operator == "<=":
                isMatch = s[field] <= numValue

        if isMatch:
            if s["name"] not in bookings:
                bookings[s["name"]] = []
            available = True
            for p in bookings[s["name"]]:
                if not (end <= p["start"] or start >= p["end"]):
                    available = False
                    break
            if available:
                candidates.append(s)

    #
    bestService = None
    if candidates:
        if operator == "=":
            bestService = candidates[0]
        elif operator == ">=":
            minDiff = math.inf
            numValue = float(value)
            for s in candidates:
                diff = s[field] - numValue
                if diff >= 0 and diff < minDiff:
                    minDiff = diff
                    bestService = s
        elif operator == "<=":
            maxVal = -math.inf
            numValue = float(value)
            for s in candidates:
                if s[field] <= numValue and s[field] > maxVal:
                    maxVal = s[field]
                    bestService = s

    #
    if bestService:
        bookings[bestService["name"]].append({"start": start, "end": end})
        print(bestService["name"])
    else:
        print("Sorry")

services = [
    {"name": "S1", "r": 4.5, "c": 1000},
    {"name": "S2", "r": 3, "c": 1200},
    {"name": "S3", "r": 3.8, "c": 800},
]

func2(services, 15, 17, "c>=800")   # S3
func2(services, 11, 13, "r<=4")     # S3
func2(services, 10, 12, "name=S3")  # Sorry
func2(services, 15, 18, "r>=4.5")   # S1
func2(services, 16, 18, "r>=4")     # Sorry
func2(services, 13, 17, "name=S1")  # Sorry
func2(services, 8, 9, "c<=1500")    # S2
func2(services, 8, 9, "c<=1500")    # S1

# Task 3
def func3(index):
    arr = [25]

    if index == 0:
        print(arr[index])
        return

    for i in range(1, index + 1):
        if i % 4 == 1:
            arr.append(arr[i - 1] - 2)
        elif i % 4 == 2:
            arr.append(arr[i - 1] - 3)
        elif i % 4 == 3:
            arr.append(arr[i - 1] + 1)
        else:  # i % 4 == 0
            arr.append(arr[i - 1] + 2)

    print(arr[index])

func3(1) # print 23
func3(5) # print 21
func3(10) # print 16
func3(30) # print 6

# Task 4
def func4(sp, stat, n):

    stat_num_arr = [int(s) for s in stat]

    pair = [{'index': i, 'space': sp[i], 'stat': stat_num_arr[i]} for i in range(len(sp))]

    available_cars = [car for car in pair if car['stat'] == 0]

    min_diff = float('inf')
    best_car_index = -1
    for car in available_cars:
        diff = abs(car['space'] - n)
        if diff < min_diff:
            min_diff = diff
            best_car_index = car['index']

    print(best_car_index)

func4([3, 1, 5, 4, 3, 2], "101000", 2) # print 5
func4([1, 0, 5, 1, 3], "10100", 4) # print 4
func4([4, 6, 5, 8], "1000", 4) # print 2

