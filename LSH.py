# -*- coding:utf-8 -*-

import cv2
import os
import time

#计算颜色直方图
def cal_RGB(filename):
    img = cv2.imread(filename,cv2.IMREAD_COLOR)
    half_height = len(img) / 2
    half_width = len(img[0]) / 2
    p = []
    for i in range(2):
        for j in range(2):
            R = 0.0
            G = 0.0
            B = 0.0
            for k in range(half_height):
                for l in range(half_width):
                    R += img[i*half_height + k][j*half_width + l][0]
                    G += img[i*half_height + k][j*half_width + l][1]
                    B += img[i*half_height + k][j*half_width + l][2]
            total = R + G + B
            p = p + [R/total , G/total , B/total]

    for i in range(12):
        if p[i] < 0.33:
            p[i] = 0
        elif p[i]< 0.66:
            p[i] = 1
        else:
            p[i] = 2
    return p

#哈希函数
def g(filename,I):
    p = cal_RGB(filename)
    d = len(p)
    c = 2
    I_i =[[] for i in range(d)]

    # 求 I|i
    for index in I:
        I_i[(index-1)/c].append(index)

    #计算投影
    result = []
    for i in range(d):
        if len(I_i[i])>0:
            result_i = [0]*len(I_i[i])
            num = 0
            for obj in I_i[i]:
                if obj-i*c <= p[i]:
                    num += 1
            for j in range(num):
                result_i[j] = 1
            result += result_i
    return result
'''
#将数据库中的图像哈希化
def hash_all(path,I):
    file_list = os.listdir(path)
    print "数据库中共有",len(file_list),"幅图像"
    print "采用的初始列表为",I
    hash_map = {}
    for i in file_list:
        hash_pic = g(path+i,I)
        if str(hash_pic) in hash_map.keys():
            hash_map[str(hash_pic)] += [i]
        else:
            hash_map[str(hash_pic)] = [i]
    x = 0
    f = open('hash_result.txt', 'w')
    for i in hash_map:
        x = x + 1
        f.write(i+'#')
        for j in hash_map[i]:
            f.write(j+'*')
        f.write('\n')

    f.close()
    print "盒子数目：",x
    return  hash_map
'''
#导入哈希txt
def import_map():
    hash_file = open('/home/lds/Documents/django_project/Helloworld/myword/hash_result.txt', 'r')
    map_result = {}
    for line in hash_file:
 	maplist = line.split('#')
	map_key = maplist[0]
        mapvalue = maplist[1]
        map_value = mapvalue.split('*')
	map_value.pop()
	map_result[map_key] = map_value
    return map_result

#匹配算法
def match_pic(img1,img2):
    # 创建orb特征检测器和描述符
    orb = cv2.ORB()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # 暴力匹配
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    return len(matches)

def search_pic(filename,path,I):

    pic_input = str(g(filename,I))
    dataset = import_map()#hash_all(path,I)
    max_match_num = -1
    print "数据库建立已经完成\n"
    start = time.clock()
    final_result = []
    if pic_input in dataset.keys():
        print "搜索范围已缩小至",len(dataset[pic_input]),"个"
        img1 = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
	
	match_map = {}
        
	for i in dataset[pic_input]:
            img2 = cv2.imread('/home/lds/Documents/django_project/Helloworld/myword/Dataset/'+i, cv2.IMREAD_GRAYSCALE)
            match_num =  match_pic(img1, img2)

            match_map[i] = match_num

            if match_num > max_match_num:
                max_match_num = match_num
                most_match = i
        match_sort_map = sorted(match_map.iteritems(),key = lambda d:d[1], reverse = True)
	#print match_sort_map
        match_list = []
        #final_result = []
	for i in match_sort_map:
	   match_list.append(i)
        if len(match_list)>20:
	    match_result = match_list[0:20]
        else:
	    match_result = match_list
        for i in match_result:
	    final_result.append(i[0])
        #print "最佳结果匹配:",most_match
        #print "前十:",match_result
    else:
        print "无匹配项"
    end = time.clock()
    print '运行时间: %s 秒' % (end - start)
    return final_result

def LSH(filename):
    path = "/home/hduser/Desktop/LSH/Dataset/"
    print(filename)
    print "使用LSH方法"
    I = [2, 5, 7, 10 , 12, 15, 17, 19, 21 ,23]
    return search_pic(filename, path, I)

'''
def baoli():
    print "使用全部匹配方法"
    I = [2, 5, 7, 10 , 12, 15, 17, 19, 21 ,23]
    filename = "target.jpg"
    path = "/home/hduser/Desktop/LSH/Dataset/"
    file_list = os.listdir(path)
    print "数据库中共有", len(file_list), "幅图像"
    print "采用的初始列表为", I

    max_match_num = -1
    img1 = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    for i in file_list:
        img2 = cv2.imread('Dataset/' + i, cv2.IMREAD_GRAYSCALE)
        match_num = match_pic(img1, img2)
        if match_num > max_match_num:
            max_match_num = match_num
            most_match = i
    print "最佳结果匹配:", most_match
'''
#LSH("/home/lds/Documents/django_project/Helloworld/media/search_file/2.jpg")


