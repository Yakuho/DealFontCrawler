# DealFontCrawler
解决字体反爬的简单通用模型

ps: 由于操作问题，最新版本的代码不能直接clone， 请在release对应下载zip压缩包文件


### 功能
1. 自动处理字体坐标

2. 自动匹配不同大小的字体坐标矩阵

3. 使用相对坐标归一化来应对坐标处于坐标不同位置的情况

4. 直接产生Unicode键值对便于调用

### 优点

1. 前期训练只需进行少量的数据标注工作就能建立字体映射模型

2. 直接写入需要解密的woff文件或ttf文件即可自动获得映射

### 训练的代码示例以及步骤介绍
训练步骤

- 在dataset文件夹放入训练集文件。格式：(woff / ttf)

- 在代码写好训练集的导入路径。
    ```python
    # 初始化对象
    m = model.KnnFont()
    # 将 dataset 文件夹内的 woff文件或ttf文件 自动转化 xml 并提取（坐标向量，对应unicode值）
    # mode模式： 1为训练模式， 0为预测模式
    train_x, train_y = m.load_offset('dataset', mode=1)
    ```

-  通过内置方法, 找到字体文件Unicode所对应的字符。PS: 字体文件的查看可百度在线查看或者下载TTfont工具

    在获取字体映射的过程中，类KnnFont封装好2个获取映射编码的函数分别是 KnnFont.get_labels_by_GlyphNames 和
KnnFont.get_labels_by_glyphID， 这两种方法对应的是Font字体编辑器上的两种排序 Glyph Name和
Glyph Index。这样就可便于根据需要标注训练集的映射。

    注意：Font字体编辑器看到的编码名字对应到程序上可能不是这个名称。例如在目录ickey.ttf文件中，在字体编辑器查看的编码
**".null"** 在程序中却是 **".notdef"**; **"uni0001"** 在程序中却是 **"uni0000"**; 
**"uniFFFD"** 在程序中却是 **"uni0001"** 等等现象。所以作者建议先使用内置的那两种方法中的其中一种，先查看对应
的编码名再建立映射。 如何查看字体文件可在各大引擎进行搜索。

    ```python
    # 根据Names进行排序的顺序
    print('GlyphNames:', m.get_labels_by_GlyphNames('dataset/000001.woff'))
    # 根据Index进行排序的顺序
    print('GlyphID:', m.get_labels_by_glyphID('dataset/000001.woff', 603))
    ```

-  将拿到的Unicode集合与对应字体文件上实际上显示的字符进行对应，并写入items里，**必须得按照名称由小到大的排序顺序进行存放**。

    格式例如000001.woff文件经过index方法查看，拿到的编码值是font_index的顺序显示，且文件里面有603个字符。则
    ```python
    font_index = '1234567890店...........跟块调糕'
    items = [
        # 字体文件排序方法， 文件路径， 文件内字符数，  映射的字符
        # index/names   dataset/...   int       string
        ['index', 'dataset/000001.woff', 603, font_index],
        ['index', 'dataset/000002.woff', 603, font_index],
        ['index', 'dataset/000003.woff', 603, font_index],
        ['index', 'dataset/000004.woff', 603, font_index]
    ]
    ```

    如果000008.woff文件经过names方法查看，拿到的编码值是font_name(一个新的字符串)，且文件里面只有40个字符。则

    ```python
    font_name = '1234阿斯顿撒.........块调糕'
    items = [
        # 字体文件排序方法， 文件路径， 文件内字符数，  映射的字符
        # index/names   dataset/...   int       string
        ['index', 'dataset/000001.woff', 603, font_index],
        ['index', 'dataset/000002.woff', 603, font_index],
        ['index', 'dataset/000003.woff', 603, font_index],
        ['index', 'dataset/000004.woff', 603, font_index],
        ...
        ['names', 'dataset/000008.woff', 40, font_name]
    ]
    ```

- 训练前，只要把之前的items将train_y进行映射，则可以进行训练。训练后会保存一个模型文件npz，以后则根据模型进行导入，dataset里面的文件也可根据
需要进行删除.
    ```python
    m.unicode2chr(unicode=train_y, items=items)
    # 训练并保存模型, 并写上文件名
    m.fit(train_x, train_y, filename='DaZhongDianPing')
    ```
- 训练全流程
    ```python
  from utils import model
  
  
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
        ['index', 'dataset/000004.woff', 603, font_index]
    ]
    m.unicode2chr(unicode=train_y, items=items)
    # 训练并保存模型
    m.fit(train_x, train_y, filename='DaZhongDianPing')
    ```

### 预测的代码示例
- 导入训练模型
    ```python
    # 初始化模型
    model = KnnFont()
    # 导入预训练数据集 默认DataSet.npz
    train_x, train_y = model.load('DaZhongDianPing')
    ```
- 导入待预测模型
    ```python
    # 加载待预测字体文件坐标向量
    # mode: 1训练模式， 0预测模式
    test_x, test_y = model.load_offset('test1.woff', mode=0)
    ```
- 拿到结果
    ```python
    # 获取 Unicode 与 字符的映射
    result = model.predict(train_x, train_y, test_x, test_y)
    print(result)
    ```
- 全流程
    ```python
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
    ```
    ```
    >> load DataSet from DaZhongDianPing.npz
    >> converted 0 test font file.
    >> {'glyph00000': ' ', 'unie011': '三', 'unie014': '林', 'unie01e': '果', 'unie022': '香', 'unie025': '四', 'unie038': '样', 'unie054': '学', 'unie064': '窗', 'unie067': '知', 'unie06e': '外', 'unie07a': '用', 'unie086': '吧', 'unie088': '钢', 'unie09a': '肉', 'unie09f': '还', 'unie0a0': '世', 'unie0a3': '设', 'unie0ac': '然', 'unie0af': '內', 'unie0b0': '他', 'unie0b5': '古', 'unie0c6': '就', 'unie0cc': '2', 'unie0d0': '武', 'unie0d9': '般', 'unie0df': '米', 'unie0e5': '瑞', 'unie0e7': '道', 'unie0e9': '秀', 'unie0ea': '气', 'unie0f1': '县', 'unie106': '中', 'unie10d': '快', 'unie114': '境', 'unie134': '生', 'unie167': '再', 'unie169': '集', 'unie171': '产', 'unie17b': '子', 'unie1b0': '轩', 'unie1cc': '广', 'unie1d2': '精', 'unie1d5': '回', 'unie1df': '较', 'unie1f5': '务', 'unie1fa': '份', 'unie201': '体', 'unie212': '后', 'unie215': '作', 'unie21c': '火', 'unie221': '祥', 'unie224': '了', 'unie226': '丽', 'unie232': '吃', 'unie233': '段', 'unie240': '4', 'unie246': '便', 'unie248': '虾', 'unie24a': '湖', 'unie251': '热', 'unie263': '汉', 'unie268': '师', 'unie274': '这', 'unie282': '斯', 'unie290': '部', 'unie293': '副', 'unie2ac': '源', 'unie2b2': '又', 'unie2b6': '饭', 'unie2de': '棒', 'unie2eb': '事', 'unie2f6': '溪', 'unie303': '关', 'unie319': '鸭', 'unie32a': '好', 'unie32f': '字', 'unie344': '时', 'unie348': '菜', 'unie351': '器', 'unie353': '贸', 'unie354': '常', 'unie359': '名', 'unie362': '烫', 'unie36c': '联', 'unie380': '些', 'unie382': '人', 'unie391': '建', 'unie3ad': '贝', 'unie3af': '童', 'unie3c9': '最', 'unie3cd': '兴', 'unie3d1': '网', 'unie3d5': '牛', 'unie3db': '跟', 'unie3dd': '春', 'unie3f9': '全', 'unie406': '杂', 'unie408': '同', 'unie410': '种', 'unie415': '万', 'unie41a': '都', 'unie41f': '楼', 'unie424': '无', 'unie437': '江', 'unie438': '酒', 'unie43c': '宾', 'unie43e': '态', 'unie44d': '纪', 'unie461': '讯', 'unie47e': '情', 'unie48c': '业', 'unie497': '饼', 'unie49a': '位', 'unie49f': '但', 'unie4a3': '可', 'unie4b2': '城', 'unie4ca': '尚', 'unie4d7': '桂', 'unie4de': '市', 'unie4e4': '里', 'unie4f8': '司', 'unie4ff': '凤', 'unie50c': '机', 'unie50e': '所', 'unie518': '特', 'unie526': '进', 'unie530': '板', 'unie53c': '线', 'unie557': '重', 'unie564': '文', 'unie565': '店', 'unie56a': '政', 'unie57f': '适', 'unie581': '强', 'unie5a0': '每', 'unie5a6': '足', 'unie5ab': '合', 'unie5ce': '没', 'unie5e1': '教', 'unie5f1': '整', 'unie5f2': '弄', 'unie5f5': '小', 'unie5f9': '直', 'unie600': '桥', 'unie613': '我', 'unie621': '什', 'unie626': '赞', 'unie634': '杨', 'unie637': '品', 'unie638': '周', 'unie639': '南', 'unie646': '酸', 'unie64e': '儿', 'unie66f': '惠', 'unie672': '尝', 'unie67b': '金', 'unie67d': '0', 'unie681': '张', 'unie68d': '井', 'unie6bd': '处', 'unie6bf': '号', 'unie6cd': '分', 'unie6d1': '角', 'unie6f0': '苑', 'unie6fb': '百', 'unie713': '二', 'unie71c': '油', 'unie726': '厦', 'unie738': '觉', 'unie73c': '玉', 'unie73e': '村', 'unie74a': '底', 'unie74b': '到', 'unie74d': '满', 'unie758': '口', 'unie774': '试', 'unie776': '选', 'unie785': '电', 'unie792': '堂', 'unie7ad': '鸿', 'unie7af': '天', 'unie7d0': '五', 'unie7d6': '明', 'unie7e4': '园', 'unie7e8': '售', 'unie7eb': '能', 'unie7f5': '红', 'unie7fd': '町', 'unie80b': '食', 'unie80f': '次', 'unie81f': '石', 'unie827': '有', 'unie839': '校', 'unie844': '川', 'unie848': '座', 'unie84d': '奶', 'unie85b': '旗', 'unie868': '原', 'unie87b': '衣', 'unie89c': '服', 'unie89f': '刚', 'unie8a1': '田', 'unie8bd': '幼', 'unie8c4': '3', 'unie8c8': '色', 'unie8ce': '理', 'unie8d0': '莲', 'unie8d3': '河', 'unie8de': '高', 'unie8fa': '推', 'unie900': '室', 'unie901': '微', 'unie915': '斜', 'unie916': '马', 'unie922': '兰', 'unie951': '错', 'unie95f': '达', 'unie963': '而', 'unie966': '心', 'unie967': '造', 'unie96a': '民', 'unie971': '东', 'unie975': '清', 'unie995': '带', 'unie9be': '宏', 'unie9c4': '噥', 'unie9cd': '屋', 'unie9db': '手', 'unie9df': '那', 'unie9e1': '珠', 'unie9ec': '寓', 'uniea02': '性', 'uniea05': '欢', 'uniea17': '培', 'uniea55': '过', 'uniea5b': '平', 'uniea66': '糕', 'uniea75': '局', 'uniea77': '打', 'uniea80': '干', 'uniea88': '华', 'uniea8b': '放', 'uniea8d': '黄', 'uniea91': '巷', 'uniea95': '汤', 'uniea97': '嘉', 'unieaa5': '厂', 'unieaa7': '现', 'unieaad': '块', 'unieab4': '为', 'unieab7': '的', 'unieab8': '农', 'unieac6': '饰', 'unieb0a': '头', 'unieb10': '加', 'unieb12': '让', 'unieb27': '爱', 'unieb35': '蛋', 'unieb48': '开', 'unieb4d': '湾', 'unieb4e': '王', 'unieb55': '十', 'unieb65': '意', 'unieb79': '央', 'unieb9a': '附', 'unieb9c': '利', 'uniebaf': '6', 'uniebbd': '笑', 'uniebc0': '动', 'uniebce': '长', 'uniebd9': '布', 'uniebe1': '昌', 'uniebf7': '塔', 'uniebfb': '阳', 'uniebfd': '日', 'uniebff': '代', 'uniec04': '元', 'uniec0b': '美', 'uniec10': '际', 'uniec26': '安', 'uniec33': '厨', 'uniec35': '几', 'uniec43': '姐', 'uniec49': '友', 'uniec59': '挺', 'uniec64': '货', 'uniec68': '话', 'uniec75': '得', 'uniec76': '影', 'uniec7c': '置', 'uniec7e': '真', 'uniec94': '步', 'uniec9d': '排', 'uniecbf': '北', 'uniecd1': '要', 'uniecde': '健', 'unieceb': '交', 'uniecf4': '材', 'uniecfa': '洲', 'uniecff': '面', 'unied07': '水', 'unied0a': '镇', 'unied0f': '富', 'unied11': '白', 'unied2f': '运', 'unied4b': '医', 'unied4c': '七', 'unied58': '台', 'unied6f': '办', 'unied73': '连', 'unied82': '铁', 'unied86': '购', 'unied95': '虹', 'unied9c': '制', 'uniedb2': '坊', 'uniedc2': '栋', 'uniedca': '保', 'uniedd1': '沿', 'uniedd4': '妆', 'uniede2': '烧', 'uniedf0': '向', 'uniedf4': '近', 'uniee07': '雅', 'uniee0c': '卫', 'uniee15': '工', 'uniee16': '度', 'uniee1b': '也', 'uniee24': '宁', 'uniee35': '公', 'uniee3d': '鱼', 'uniee3f': '容', 'uniee46': '车', 'uniee47': '路', 'uniee49': '风', 'uniee4b': '去', 'uniee59': '以', 'uniee78': '汇', 'uniee89': '汽', 'unieeba': '停', 'unieec0': '门', 'unieec1': '区', 'unieece': '家', 'unieed4': '买', 'unieee2': '着', 'unieee8': '凯', 'unieef2': '管', 'unief02': '第', 'unief04': '紫', 'unief07': '因', 'unief08': '下', 'unief36': '两', 'unief4d': '药', 'unief57': '福', 'unief58': '别', 'unief6c': '8', 'unief72': '来', 'uniefb0': '们', 'uniefc7': '烟', 'uniefcf': '价', 'uniefd0': '接', 'uniefda': '岭', 'uniefe3': '馆', 'uniefea': '景', 'unieff3': '术', 'unieffe': '顺', 'unif008': '自', 'unif00a': '串', 'unif00d': '梅', 'unif013': '皮', 'unif01b': '铺', 'unif02a': '缘', 'unif037': '对', 'unif040': '旁', 'unif045': '州', 'unif04b': '走', 'unif04c': '洗', 'unif055': '喝', 'unif059': '泰', 'unif062': '定', 'unif07a': '沙', 'unif07f': '成', 'unif087': '桌', 'unif091': '永', 'unif094': '算', 'unif0ac': '振', 'unif0af': '柳', 'unif0b0': '锅', 'unif0b5': '云', 'unif0d3': '卖', 'unif0d4': '装', 'unif0dc': '才', 'unif0e3': '候', 'unif0e5': '丁', 'unif0f2': '间', 'unif0fe': '方', 'unif102': '通', 'unif11a': '层', 'unif125': '隆', 'unif12d': '龙', 'unif139': '泉', 'unif144': '会', 'unif149': '个', 'unif14f': '山', 'unif15d': '乐', 'unif169': '本', 'unif198': '岗', 'unif19b': '甲', 'unif1b7': '八', 'unif1ca': '胜', 'unif1d2': '与', 'unif1d6': '实', 'unif1da': '叉', 'unif1e3': '正', 'unif1e5': '超', 'unif212': '佳', 'unif221': '岛', 'unif223': '庆', 'unif238': '式', 'unif23f': '评', 'unif24b': '哈', 'unif24d': '少', 'unif254': '片', 'unif256': '彩', 'unif257': '荣', 'unif25d': '诚', 'unif265': '盛', 'unif26c': '站', 'unif270': '且', 'unif277': '新', 'unif278': '羊', 'unif279': '等', 'unif27c': '销', 'unif286': '太', 'unif288': '宝', 'unif2a2': '拍', 'unif2a4': '银', 'unif2a7': '单', 'unif2ae': '更', 'unif2ba': '港', 'unif2c3': '很', 'unif2cb': '值', 'unif2e2': '于', 'unif2f6': '博', 'unif301': '5', 'unif30d': '期', 'unif30e': '7', 'unif31d': '经', 'unif31f': '鸡', 'unif32a': '发', 'unif32b': '料', 'unif333': '地', 'unif335': '阿', 'unif33e': '么', 'unif34e': '鲜', 'unif355': '科', 'unif366': '团', 'unif369': '荐', 'unif371': '酱', 'unif379': '双', 'unif394': '商', 'unif3a8': '差', 'unif3cc': '西', 'unif3da': '迎', 'unif3de': '国', 'unif3e8': '九', 'unif3e9': '客', 'unif40a': '看', 'unif411': '滨', 'unif439': '啦', 'unif440': '力', 'unif454': '旅', 'unif457': '济', 'unif458': '豆', 'unif45f': '助', 'unif46d': '想', 'unif473': '记', 'unif475': '量', 'unif47a': '9', 'unif48f': '主', 'unif491': '花', 'unif495': '津', 'unif49e': '找', 'unif4a9': '专', 'unif4b1': '乡', 'unif4b3': '1', 'unif4b6': '鞋', 'unif4d7': '感', 'unif4f2': '计', 'unif4f3': '味', 'unif4f9': '喜', 'unif51e': '之', 'unif521': '牌', 'unif534': '庄', 'unif539': '康', 'unif53e': '拉', 'unif557': '临', 'unif559': '育', 'unif55c': '餐', 'unif561': '是', 'unif56d': '恒', 'unif573': '在', 'unif57b': '限', 'unif57f': '茶', 'unif58d': '格', 'unif595': '大', 'unif59b': '松', 'unif5a2': '技', 'unif5a4': '多', 'unif5a6': '员', 'unif5b6': '塘', 'unif5bd': '化', 'unif5d0': '总', 'unif5d2': '训', 'unif5d4': '级', 'unif5d7': '艺', 'unif5df': '谷', 'unif5e2': '京', 'unif5e3': '丰', 'unif5ea': '星', 'unif5ef': '嫩', 'unif5f3': '做', 'unif5f5': '社', 'unif5f8': '六', 'unif5f9': '物', 'unif5fd': '你', 'unif607': '女', 'unif610': '批', 'unif611': '朝', 'unif613': '边', 'unif619': '厅', 'unif629': '氏', 'unif641': '入', 'unif64e': '说', 'unif659': '调', 'unif672': '己', 'unif67a': '出', 'unif67e': '费', 'unif681': '甜', 'unif695': '如', 'unif69e': '型', 'unif6a2': '前', 'unif6a4': '峰', 'unif6a6': '包', 'unif6cb': '居', 'unif6e1': '维', 'unif6e7': '养', 'unif6ea': '吉', 'unif706': '海', 'unif70f': '陵', 'unif718': '修', 'unif71a': '像', 'unif730': '午', 'unif747': '营', 'unif75c': '光', 'unif762': '信', 'unif76c': '鑫', 'unif76e': '队', 'unif76f': '朋', 'unif776': '幢', 'unif778': '年', 'unif781': '浦', 'unif784': '行', 'unif78d': '烤', 'unif796': '比', 'unif7a1': '侧', 'unif7a8': '场', 'unif7ab': '上', 'unif7ac': '其', 'unif7bb': '院', 'unif7c0': '配', 'unif7c4': '省', 'unif7c8': '点', 'unif7cc': '粉', 'unif7d3': '完', 'unif7ee': '起', 'unif7ff': '只', 'unif803': '当', 'unif804': '非', 'unif807': '啊', 'unif824': '辣', 'unif826': '提', 'unif827': '木', 'unif836': '街', 'unif83b': '环', 'unif856': '和', 'unif859': '横', 'unif886': '给', 'unif88b': '青', 'unif896': '活', 'unif8a0': '具', 'unif8a7': '解', 'unif8a9': '德', 'unif8aa': '晚', 'unif8b0': '不', 'unif8bb': '尔', 'unif8be': '麻', 'unif8c1': '老', 'unif8d2': '三', 'unif8ec': '房', 'unif8f7': '锦', 'unif8fd': '府', 'x': '.'}
    ```

### 使用案例
训练时候产生的模型DaZhongDianPing是从大众点评返回的woff文件进行的，经过测试准确率达到100%。可以直接load使用。

### 依赖库
```
pip install fontTools xml numpy sklearn 
```

