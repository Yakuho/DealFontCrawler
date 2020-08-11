from sklearn.neighbors import KNeighborsClassifier
from utils.base import get_offset_font
from utils.base import normalization
from utils.base import make_xml
from utils.base import get_labels_by_GlyphNames
from utils.base import get_labels_by_glyphID
from utils.base import matrix


class KnnFont:
    def __init__(self, trainFontMode):
        self.trainDataSetPath = './dataset/dataBase.json'
        self.trainFontMode = trainFontMode
        self.Y = list()

    @classmethod
    def viewFontFileCodeByGlyphsNames(cls, path, mode):
        return get_labels_by_GlyphNames(f'{path}.{mode}')

    @classmethod
    def viewFontFileCodeByGlyphsId(cls, path, mode):
        glyphName = cls.viewFontFileCodeByGlyphsNames(path, mode)
        return [get_labels_by_glyphID(f'{path}.{mode}', glyphID) for glyphID in range(len(glyphName))]

    def initFontXML(self, path):
        make_xml(path, self.trainFontMode)

    def read(self):
        data = list()
        label = list()
        with open(self.trainDataSetPath, 'r') as f:
            while True:
                item = f.readline().strip()
                if item:
                    item = eval(item)
                    try:
                        label.append(item[0])
                        data.append(item[1])
                    except TypeError:
                        length = item
                else:
                    break
        return data, label, length

    def save(self):
        with open(self.trainDataSetPath, 'w') as f:
            length = 0
            for item in self.Y:
                if len(item[1]) > length:
                    length = len(item[1])
                f.write(f'{item}\n')
            else:
                f.write(f'{length}')

    def fit(self, pathList, labelList):
        for path in pathList:
            self.initFontXML(path)

        for path, label in zip(pathList, labelList):
            offset = get_offset_font(f'{path}.xml')
            offset = normalization(offset)
            for i in offset:
                self.Y.append([label[i[0]], i[1]])
        else:
            self.save()

    def predict(self, fontFile, n_neighbors):
        trainData, trainLabel, trainLength = self.read()
        self.initFontXML(fontFile)
        offset = get_offset_font(f'{fontFile}.xml')
        offset = normalization(offset)
        testData, testLength = list(), 0
        testLabel = list()
        for item in offset:
            if len(item[1]) > testLength:
                testLength = len(item[1])
            testData.append(item[1])
            testLabel.append(item[0])
        trainLabel, trainData = matrix(trainData, trainLabel, max(trainLength, testLength))
        testLabel, testData = matrix(testData, testLabel, max(trainLength, testLength))
        model = KNeighborsClassifier(n_neighbors=n_neighbors)
        model.fit(trainData, trainLabel)
        result = model.predict(testData)
        return dict(zip(testLabel, result))


if __name__ == '__main__':
    a = KnnFont(trainFontMode='ttf')
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
    # a.fit(paths, labels)

    a.predict('ickey', n_neighbors=3)
    # print(KnnFont.viewFontFileCodeByGlyphsNames('dataset/base3', 'ttf'))
