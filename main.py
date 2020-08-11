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

model = KnnFont(trainFontMode='ttf')
# model.fit(paths, labels)

result = model.predict('ickey', n_neighbors=3)

print(result)

# print(KnnFont.viewFontFileCodeByGlyphsNames('dataset/base3', 'ttf'))
# print(KnnFont.viewFontFileCodeByGlyphsId('ickey', 'ttf'))
