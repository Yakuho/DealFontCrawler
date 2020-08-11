# DealFontCrawler
解决字体反爬的简单通用模型


### 技术点
1. 自动获取字体坐标

2. 自动匹配不同大小的字体坐标矩阵

3. 使用相对坐标归一化来应对坐标处于坐标不同位置的情况

4. 直接产生键值对便于调用

### 优点

1. 只需进行少量的数据标注工作就能建立字体映射模型

2. 直接写入需要解密的woff文件或ttf文件即可获得映射

### 不足

1. 建立训练集的字体映射的时候可能会比较麻烦，不能做到自动化


### 训练的代码示例以及步骤介绍
训练步骤

1. 在dataset文件夹放入训练集文件.(woff / ttf)

2. 在代码写好训练集的路径，多少个训练文件对应多少个路径 **(并不用写上后缀名)**

3. 在每个对应的训练集标注好字体映射关系

4. 定义好训练集的字体文件类型如： woff， ttf

5. 进行训练，然后自动在dataset文件夹保存训练后的向量(训练完以后，在dataset文件夹内的字体文件和xml文件可根据需要进行删除)

在获取字体映射的过程中，类KnnFont封装好2个获取映射编码的函数分别是 KnnFont.viewFontFileCodeByGlyphsNames 和
KnnFont.viewFontFileCodeByGlyphsId， 这两种方法对应的是Font字体编辑器上的两种排序 Glyph Name和
Glyph Index。这样就可便于根据需要标注训练集的映射。

注意：Font字体编辑器看到的编码名字对应到程序上可能不是这个名称。例如在目录ickey.ttf文件中，在字体编辑器查看的编码
**".null"** 在程序中却是 **".notdef"**; **"uni0001"** 在程序中却是 **"uni0000"**; 
**"uniFFFD"** 在程序中却是 **"uni0001"** 等等现象。所以作者建议先使用内置的那两种方法中的其中一种，先查看对应
的编码名再建立映射。 

```python
from Model import KnnFont


paths = [
    'dataset/base1',
    'dataset/base2',
    'dataset/base3'
]
labels = [
    {'u115D5': '5', 'u69921': '2', 'u6F365': '6', 'u9B7D8': '8', 'uA4E70': '3', 'uB194D': '7', 'uC2D3D': '.',
     'uC511C': '9', 'uDB77F': '0', 'uDEE4A': '1', 'uF943D': '4', '.notdef': '', 'space': ' ', 'uni0000': '',
     'uni0001': ''},
    {'u15FA1': '9', 'u172A4': '.', 'u266DB': '0', 'u3CAF0': '2', 'u7CBCE': '1', 'u823F9': '8', 'uB0891': '5',
     'uB6A1B': '3', 'uBD774': '6', 'uEA641': '4', 'uF2D43': '7', '.notdef': '', 'space': ' ', 'uni0000': '',
     'uni0001': ''},
    {'u155BA': '8', 'u1AD7B': '2', 'u2E093': '7', 'u4FF4F': '6', 'u6D990': '4', 'u86D44': '9', 'u8F418': '3',
     'uA3D11': '0', 'uAB1B1': '1', 'uCF187': '5', 'uF1C20': '.', '.notdef': '', 'space': ' ', 'uni0000': '',
     'uni0001': ''}
]
print(KnnFont.viewFontFileCodeByGlyphsNames('dataset/base3', 'ttf'))
print(KnnFont.viewFontFileCodeByGlyphsId('dataset/base3', 'ttf'))

model = KnnFont(trainFontMode='ttf')
model.fit(paths, labels)
```

### 预测的代码示例
预测步骤分为2步：
1. 传入待预测的字体文件路径,(不带文件后缀)
2. n_neighbors 定义n的个数，一般是设为训练字体文件的数目

```python
from Model import KnnFont


model = KnnFont(trainFontMode='ttf')
result = model.predict('ickey', n_neighbors=3)
print(result)
```
```
>> {'.notdef': '', 'space': '', 'u33C3E': '.', 'u630D5': '3', 'u71DEA': '6', 'u77B76': '2', 'u7BB58': '5', 'u8941E': '8', 'uA7174': '4', 'uB83C0': '0', 'uBF8F2': '1', 'uDD740': '9', 'uE8F4A': '7', 'uni0000': '', 'uni0001': ''}
```

### 依赖库
```
pip install fontTools xml numpy sklearn 
```

