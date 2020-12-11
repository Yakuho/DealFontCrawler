# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2020/12/10
from sklearn.neighbors import KNeighborsClassifier
from utils.base import get_labels_by_GlyphNames
from utils.base import get_labels_by_glyphID
from utils.base import normalization
from utils.base import sort_offset
from utils.base import get_offset_font
from utils.base import make_xml
from utils.base import matrix
from utils.base import save_npy
from utils.base import load_npy
from utils.base import unicode2chr
from os.path import abspath
from os import listdir


class KnnFont:
    def __init__(self):
        self.length = 0

    @staticmethod
    def get_labels_by_GlyphNames(path):
        """
        从字体文件中 根据GlyphNames排序拿到unicode值
        :param path: 字体文件路径
        :return:
        """
        return get_labels_by_GlyphNames(path)

    @staticmethod
    def get_labels_by_glyphID(path, n):
        """
        从字体文件中 根据glyphIndex排序拿到unicode值
        :param path: 字体文件路径
        :param n: 字体文件总字数
        :return:
        """
        return [get_labels_by_glyphID(path, glyphID) for glyphID in range(n)]

    @staticmethod
    def font2xml(path='dataset', mode=1):
        """
        将 dataset 文件夹内的未转换的woff文件和ttf文件转化为xml格式
        :param path: woff、ttf存放的路径(默认存放在名为dataset的文件夹中)
        :param mode: 1训练集， 0测试集
        :return:
        """
        if mode:
            file_list = listdir(path)
            count = 0
            for file in file_list:
                file_name, file_type = file.split(".")
                if 'woff' == file_type and f'{file_name}.xml' not in file_list:
                    make_xml(file=f'{path}/{file}')
                    count += 1
                elif 'ttf' == file_type and f'{file_name}.xml' not in file_list:
                    make_xml(file=f'{path}/{file}')
                    count += 1
            else:
                print(f'converted {count} train font file.')
        else:
            file_list = listdir(abspath(''))
            count = 0
            file_name, file_type = path.split(".")
            if 'woff' == file_type and f'{file_name}.xml' not in file_list:
                make_xml(file=path)
                count += 1
            elif 'ttf' == file_type and f'{file_name}.xml' not in file_list:
                make_xml(file=path)
                count += 1
            else:
                print(f'converted {count} test font file.')

    @staticmethod
    def xml2offset(file):
        """
        将 file.xml文件取出坐标和编码值 (x：坐标, y：Unicode值)
        :param file: 文件路径
        :return:
        """
        offset, labels, max_len = get_offset_font(file)
        offset = sort_offset(offset)
        offset = normalization(offset)
        return offset, labels, max_len

    @staticmethod
    def unicode2chr(unicode, items):
        """
        传入train unicode列表，对应的items对应映射方法长度
        train_x, train_y = m.load_offset('dataset', mode=1)
        font_index = "年少的你说的交警萨拉....021那边"
        font_name = "电脑上都啊是觉得好...asd123"
        如:
        items = [
            ['index', 'dataset/000001.woff', 603, font_index],
            ['index', 'dataset/000002.woff', 603, font_index],
            ['index', 'dataset/000003.woff', 603, font_index],
            ['name', 'dataset/000004.woff', 603, font_name],
        ]
        train_y = m.unicode2chr(unicode=train_y, items=items)
        :param unicode:
        :param items:
        :return: 映射过后的y
        """
        return unicode2chr(unicode, items)

    def load_offset(self, path, mode=1):
        """
        导入 path 路径内的所有字体文件坐标
        :param path: 字体文件路径
        :param mode: 1训练集， 0测试集
        :return:
        """
        if mode:
            self.font2xml(path)
            file_list = listdir(path)
            x, y = list(), list()
            count = 0
            for file in file_list:
                file_name, file_type = file.split(".")
                if file_type == 'xml':
                    x0, y0, max_len0 = self.xml2offset(f'{path}/{file}')
                    self.length = max(self.length, max_len0)
                    x.extend(x0)
                    y.extend(y0)
                    count += 1
            else:
                print(f'loaded {count} font data.')
                return x, y
        else:
            self.font2xml(path, mode=0)
            file_name, file_type = path.split(".")
            x, y, max_len = self.xml2offset(f'{file_name}.xml')
            self.length = max(self.length, max_len)
            return x, y

    def fit(self, x, y, filename='DataSet'):
        """
        训练即保存向量 按照默认名称保存
        :param x: 坐标向量
        :param y: 坐标向量对应的字符
        :param filename: 保存模型的文件名字 不填默认DataSet.npz
        :return:
        """
        self.save(x, y, filename)
        print('success save train DataSet to DataSet.npz')

    def predict(self, train_x, train_y, test_x, test_y):
        """
        对未知的 Unicode 进行对训练集字符的映射
        :param train_x: 训练集坐标向量组
        :param train_y: 训练集坐标向量对应字符组
        :param test_x: 测试集坐标向量组
        :param test_y: 测试集坐标向量对应 Unicode 组
        :return: 映射结果 {Unicode: 字符}
        """
        train_x, train_y = matrix(train_x, train_y, self.length, mode='predict')
        test_x, test_y = matrix(test_x, test_y, self.length, mode='predict')
        model = KNeighborsClassifier(n_neighbors=3)
        model.fit(train_x, train_y)
        result = model.predict(test_x)
        return dict(zip(test_y, result))

    def save(self, x, y, filename='DataSet'):
        """
        保存训练集时候的向量组和字符组的向量文件
        :param x: 训练集坐标向量组
        :param y: 训练集坐标向量对应字符组
        :param filename: 保存文件的名字 default: DataSet.npz
        :return:
        """
        save_npy(x, y, self.length, filename)

    def load(self, filename='DataSet'):
        """

        :param filename:
        :return:
        """
        file = load_npy(f'{filename}.npz')
        x = file['arr_0']
        y = file['arr_1']
        self.length = max(file['arr_2'], self.length)
        print(f'load DataSet from {filename}.npz')
        return x, y
