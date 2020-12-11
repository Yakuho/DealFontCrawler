# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2020/12/10
from xml.dom.minidom import parse
from fontTools.ttLib import TTFont
from numpy import asarray
from numpy import savez
from numpy import load


# 将.tff/.woff转为xml
def make_xml(file):
    font = TTFont(file)
    font.saveXML(f'{file[:file.index(".")]}.xml')


# 从xml文件中拿到各个字体的坐标并按x从小到大进行排序
def get_offset_font(filename):
    data = parse(filename)
    collection = data.documentElement
    labels = collection.getElementsByTagName("TTGlyph")
    unicode, offset = list(), list()
    max_len = 0
    for label in labels:
        # 拿到字体在 woff 文件中的unicode，y_max,y_min,x_max,x_min
        contour = label.getElementsByTagName("contour")
        unicode.append(label.getAttribute("name"))
        temp = [[
                int(label.getAttribute("yMax")) if label.getAttribute("yMax") else 0,
                int(label.getAttribute("yMin")) if label.getAttribute("yMin") else 0,
                int(label.getAttribute("xMax")) if label.getAttribute("xMax") else 0,
                int(label.getAttribute("xMin")) if label.getAttribute("xMin") else 0
        ]]
        # 拿到当前文字的所有坐标值
        x, y = list(), list()
        for item in contour:
            pt = item.getElementsByTagName("pt")
            for xy in pt:
                if xy.hasAttribute("x") and xy.hasAttribute("y"):
                    x.append(int(xy.getAttribute("x")))
                    y.append(int(xy.getAttribute("y")))
        else:
            temp.append(x)
            temp.append(y)
            offset.append(temp)
            max_len = max(max_len, len(x) * 2)
    return offset, unicode, max_len


# 排序 offset
def sort_offset(offset):
    data = list()
    for item in offset:
        head, x, y = item
        temp = [head]
        for i in sorted(zip(x, y)):
            temp.extend(i)
        data.append(temp)
    return data


# 统一坐标系，使得都从 0,0 开始
def normalization(offset_list):
    x = list()
    for item in offset_list:
        try:
            head, rear = item[0], item[1:]
            y_min, x_min = head[1], head[3]
            head[0] -= y_min
            head[1] -= y_min
            head[2] -= x_min
            head[3] -= x_min
            for i in range(len(rear)):
                if i % 2 == 0:
                    rear[i] = rear[i] - x_min
                else:
                    rear[i] = rear[i] - y_min
            x.append(rear)
        except IndexError:
            x.append([])
    return x


# 转为矩阵
def matrix(offset, labels, length=0, mode='load'):
    """

    :param offset: 坐标值 -> list
    :param labels: 标签值 -> list
    :param length: 统一长度的大小
    :param mode: load模式将加载的数据集转化array， train模式将向量统一长度
    :return:
    """
    if mode == 'predict':
        data = list()
        for item in offset:
            offsetList = item
            data.append(offsetList)
        for i in range(len(data)):
            data[i] = data[i] + [0] * (length - len(data[i]))
        else:
            labels = asarray(labels)
            data = asarray(data)
    else:
        labels = asarray(labels)
        data = asarray(offset)
    return data, labels


# 从npy文件保存向量
def save_npy(x, y, length, filename):
    savez(filename, x, y, length)


# 从npy文件获取向量
def load_npy(file):
    return load(file, allow_pickle=True)


# 从xml拿到labels
def get_labels_by_GlyphNames(path):
    font = TTFont(path)
    return font.getGlyphNames()


# 从xml拿到labels
def get_labels_by_glyphID(path, glyphID):
    font = TTFont(path)
    return font.getGlyphName(glyphID=glyphID)


# 完成Unicode与字符的映射
def unicode2chr(unicode, items):
    start, end = 0, 0
    for item in items:
        mode, file, n, base = item
        end += n
        if mode == 'index':
            x = [get_labels_by_glyphID(file, i) for i in range(n)]
        else:
            x = get_labels_by_GlyphNames(file)
        dictionary = dict(zip(x, base))
        for i in range(start, end):
            unicode[i] = dictionary[unicode[i]]
        start = end
