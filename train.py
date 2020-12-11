# -*- coding: utf-8 -*-
# Author: Yakuho
# Date  : 2020/12/10
from utils import model


font_index = ' .1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老' \
              '艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫二容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿' \
              '衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明' \
              '器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤' \
              '网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青' \
              '镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里三管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉' \
              '附近层旁对巷栋环省桥湖段乡厦府铺內侧元购前幢滨处向座下噥凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜' \
              '本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹' \
              '央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位' \
              '能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶' \
              '打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差' \
              '像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'

# 初始化对象
m = model.KnnFont()
# 将 dataset 文件夹内的 woff文件或ttf文件 自动转化 xml 并提取（坐标向量，对应unicode值）
train_x, train_y = m.load_offset('dataset', mode=1)
# 查看字体文件 unicode 排序情况
print('GlyphNames:', m.get_labels_by_GlyphNames('dataset/000001.woff'))
print('GlyphID:', m.get_labels_by_glyphID('dataset/000001.woff', 603))
# 将 unicode 转换成真正的字符串映射
items = [
    # 字体文件排序方法， 文件路径， 文件内字符数，  映射的字符
    # index/names   dataset/...   int       string
    ['index', 'dataset/000001.woff', 603, font_index],
    ['index', 'dataset/000002.woff', 603, font_index],
    ['index', 'dataset/000003.woff', 603, font_index],
    ['index', 'dataset/000004.woff', 603, font_index],
]
m.unicode2chr(unicode=train_y, items=items)
# 训练并保存模型
m.fit(train_x, train_y, filename='DaZhongDianPing')
