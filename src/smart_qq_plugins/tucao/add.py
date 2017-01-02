from six.moves import cPickle
new = {
        '反馈': ['请私聊给小鸭子，343183163'], 
        'galgame': ['galgame打多了会变成死宅的，死宅很恶心的。'], 
        'bug': ['请反馈给小鸭子'], 
        '小白': ['其实一般自称小白的都是大触哟 ╮(╯▽╰)╭'], 
        '[Dd][Ii][Ss][Mm].*论坛': ['Elisa的温馨提示：dism++论坛正在备案中，暂时无法链接哟～'], 
        '[Dd][Ii][Ss][Mm].*官网': ['Elisa的温馨提示：DISM++官网正在备案中，请耐心等待~'], 
        'IrisWind': ['今生今世 飘尘只爱她一人 今生今世 只娶她一人 若不能达 则入地狱 永不超生\n这样就好'], 
        '操你': ['你要操我吗，但是我可是会操雪乃的Robot QwwwwQ'], 
        'Rambin三大格言': ['睡眠=午睡\n休眠=晚上睡觉\n重启=人生重来枪'], 
        '天津风': ['岛津风最棒了～Prpr'],  
        }

with open("./200783396.tucao", "wb+") as tucao_file:
    cPickle.dump(new, tucao_file)

