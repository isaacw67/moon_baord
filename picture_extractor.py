from tracemalloc import start
import numpy as np
import pandas as pd
import pathlib as fl
import os as os
from PIL import Image
import pytesseract
import tensorflow

def read_pic(path = "C:/Users/isaac/Documents/code/ml_22/moon/testing/FAR FROM THE MADDING CROWD.png"):
    p = fl.Path(path)
    #print(p.exists())
    startX, startY = (169, 333)
    horzGap = 89
    vertGap = 89
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    # Col: 434, 275
    # orig: 434, 333
    # across 524
    # down: 422
    # 
    with Image.open(path) as im:
        route = []
        for row in range(18):
            for col in range(11):
                color = im.getpixel((startX + horzGap*col, startY + vertGap*row - 58))
                color2 = im.getpixel((startX + horzGap*col, startY + vertGap*row - 61))
                color3 = im.getpixel((startX + horzGap*col, startY + vertGap*row - 55))
                #print(((startX + horzGap*col, startY + vertGap*row - 58)))
                if color == red or color2 == red or color3 == red:
                    #print("Finish: ", (18-row), col)
                    route.append([18-row, col, 'F'])
                elif color == green or color2 == green or color3 == green:
                    #print("Start: ", (18-row), col)
                    route.append([18-row, col,'S'])
                elif color == blue or color2 == blue or color3 == blue:
                    #print("Uses: ", (18-row), col)
                    route.append([18-row, col,'U'])
    return route

def route_to_arr(route):
    ret = []
    appended = False
    for i in range(1,19):
        for j in range(11):
            appended = False
            for hold in route:
                if hold[0] == i and hold[1] == j:
                    ret.append(hold[2])
                    appended = True
                    break
            if not appended:
                ret.append('N')
    return ret

def create_names(n1, n2):
    ret = []
    for i in range(1,n1+1):
        for j in range(n2):
            ret.append('{0}x{1}'.format(i, j))
    return ret


def create_pd_frame(routes):
    cols = ['Name']
    cols.extend(create_names(18,11))
    ret = pd.DataFrame(routes, columns= cols)
    ret.to_csv("routes.csv")
    return ret

def read_in(path):
    p = fl.Path(path)
    p.resolve
    pos_fls = os.listdir(p)
    routes = []
    for file_name in pos_fls:
        ar = [file_name.removesuffix('.png')]
        ar.extend(route_to_arr(read_pic(path + '/' + file_name)))
        routes.append(ar)
    df = create_pd_frame(routes)
    return routes


def has_start_end(route):
    end = False
    start = False
    for tup in route:
        if tup[2] == 'F':
            end = True
        elif tup[2] == 'S':
            start = True

    return (end and start)

def check_valid(df):
    df['valid'] = np.where(has_start_end(df['Route']), 1, 0)
    return df


if __name__ == "__main__":
    create_pd_frame(read_in("C:/Users/isaac/Documents/code/ml_22/moon/pictures"))
    #r = [[18, 4, 'F'], [13, 7, 'U']]
    #r2 = route_to_arr(r)
    #cn = create_names(18,11)
    #print(r2)
    #print(cn)
    #print(len(cn), len(r2))
    #df = pd.read_csv("routes.csv")
    #df = check_valid(df)
    #print(create_names(18,11)) 