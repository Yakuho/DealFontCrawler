# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2020/12/10
from utils.model import KnnFont


# 初始化模型
model = KnnFont()
# 导入预训练数据集 默认DataSet.npz
train_x, train_y = model.load('DaZhongDianPing')
# 加载待预测字体文件坐标向量
test_x, test_y = model.load_offset('test1.woff', mode=0)
# 获取 Unicode 与 字符的映射
result = model.predict(train_x, train_y, test_x, test_y)
print(result)

