from xml.dom.minidom import parse
from fontTools.ttLib import TTFont
from numpy import asarray


def get_labels_by_GlyphNames(file):
    font = TTFont(file)
    return font.getGlyphNames()


def get_labels_by_glyphID(file, glyphID):
    font = TTFont(file)
    return font.getGlyphName(glyphID=glyphID)


def make_xml(file, mode='woff'):
    font = TTFont(f'{file}.{mode}')
    font.saveXML(f'{file}.xml')


# 从xml文件中拿到各个字体的坐标
def get_offset_font(filename):
    data = parse(filename)
    collection = data.documentElement
    labels = collection.getElementsByTagName("TTGlyph")
    data_list = []
    max_len = 0
    for label in labels:
        contour = label.getElementsByTagName("contour")
        # 拿到字体在woff文件中的unicode，y_max,y_min,x_max,x_min
        offset = [[label.getAttribute("name"),
                   int(label.getAttribute("yMax")) if label.getAttribute("yMax") else 0,
                   int(label.getAttribute("yMin")) if label.getAttribute("yMin") else 0,
                   int(label.getAttribute("xMax")) if label.getAttribute("xMax") else 0,
                   int(label.getAttribute("xMin")) if label.getAttribute("xMin") else 0]]
        for item in contour:
            pt = item.getElementsByTagName("pt")
            # 遍历一个字体中的所有x，y坐标
            for xy in pt:
                if xy.hasAttribute("x"):
                    offset.append(int(xy.getAttribute("x")))
                if xy.hasAttribute("y"):
                    offset.append(int(xy.getAttribute("y")))
        else:
            data_list.append(offset)
            max_len = max_len if max_len > len(offset) else len(offset)
    return data_list


# 重整理坐标，使得都从0,0开始, 并在列表的最后添加最大尺寸
def normalization(offset_list):
    new_offset = []
    max_size = {'x': 0, 'y': 0}
    for item in offset_list:
        if len(item) > 1:
            head, rear = item[0], item[1:]
            y_min, x_min = head[2], head[4]
            head[1] = head[1] - y_min
            head[2] = head[2] - y_min
            head[3] = head[3] - x_min
            head[4] = head[4] - x_min
            max_size['x'] = head[3] if head[3] > max_size['x'] else max_size['x']
            max_size['y'] = head[1] if head[1] > max_size['y'] else max_size['y']
            for i in range(len(rear)):
                if i % 2 == 0:
                    rear[i] = rear[i] - x_min
                else:
                    rear[i] = rear[i] - y_min
            new_offset.append([head[0], rear])
        else:
            new_offset.append([item[0][0], []])
    return new_offset


def matrix(offset, labels, length=0):
    data = []
    for item in offset:
        offsetList = item
        data.append(offsetList)
    for i in range(len(data)):
        data[i] = data[i] + [0] * (length - len(data[i]))
    else:
        labels = asarray(labels)
        data = asarray(data)
        return labels, data
