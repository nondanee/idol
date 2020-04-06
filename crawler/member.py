# -*- coding: utf-8 -*-

import re

members = {
    '運営スタッフ': ['0000', 'unei-sutaffu'],
    '秋元真夏': ['0101', 'akimoto-manatsu'],
    '生田絵梨花': ['0102', 'ikuta-erika'],
    '生駒里奈': ['0103', 'ikoma-rina'],


    '伊藤万理華': ['0106', 'itou-marika'],
    '井上小百合': ['0107', 'inoue-sayuri'],
    '衛藤美彩': ['0108', 'etou-misa'],
    '川後陽菜': ['0109', 'kawago-hina'],
    '川村真洋': ['0110', 'kawamura-mahiro'],
    '齋藤飛鳥': ['0111', 'saitou-asuka'],
    '斎藤ちはる': ['0112', 'saitou-chiharu'],
    '斉藤優里': ['0113', 'saitou-yuuri'],
    '桜井玲香': ['0114', 'sakurai-reika'],
    '白石麻衣': ['0115', 'shiraishi-mai'],
    '高山一実': ['0116', 'takayama-kazumi'],
    '中田花奈': ['0117', 'nakada-kana'],
    '中元日芽香': ['0118', 'nakamoto-himeka'],

    '西野七瀬': ['0120', 'nishino-nanase'],
    '能條愛未': ['0121', 'noujou-ami'],


    '樋口日奈': ['0124', 'higuchi-hina'],

    '星野みなみ': ['0126', 'hoshino-minami'],
    '松村沙友理': ['0127', 'matsumura-sayuri'],

    '若月佑美': ['0129', 'wakatsuki-yumi'],
    '和田まあや': ['0130', 'wada-maaya'],
    '渡辺みり愛': ['0201', 'watanabe-miria'],
    '新内眞衣': ['0202', 'shinuchi-mai'],
    '北野日奈子': ['0203', 'kitano-hinako'],
    '堀未央奈': ['0204', 'hori-miona'],
    '伊藤かりん': ['0205', 'itou-karin'],
    '寺田蘭世': ['0206', 'terada-ranze'],

    '佐々木琴子': ['0208', 'sasaki-kotoko'],

    '山崎怜奈': ['0210', 'yamazaki-rena'],
    '伊藤純奈': ['0211', 'itou-junna'],
    '鈴木絢音': ['0212', 'suzuki-ayane'],

    '相楽伊織': ['0214', 'sagara-iori'],
    '伊藤理々杏': ['0301', 'itou-riria'],
    '岩本蓮加': ['0302', 'iwamoto-renka'],
    '梅澤美波': ['0303', 'umezawa-minami'],
    '大園桃子': ['0304', 'oozono-momoko'],
    '久保史緒里': ['0305', 'kubo-shiori'],
    '阪口珠美': ['0306', 'sakaguchi-tamami'],
    '佐藤楓': ['0307', 'satou-kaede'],
    '中村麗乃': ['0308', 'nakamura-reno'],
    '向井葉月': ['0309', 'mukai-hazuki'],
    '山下美月': ['0310', 'yamashita-mizuki'],
    '吉田綾乃クリスティー': ['0311', 'yoshida-ayano-christie'],
    '与田祐希': ['0312', 'yoda-yuuki'],
    '遠藤さくら': ['0401', 'endou-sakura'],
    '賀喜遥香': ['0402', 'kaki-haruka'],
    '掛橋沙耶香': ['0403', 'kakehashi-sayaka'],
    '金川紗耶': ['0404', 'kanagawa-saya'],
    '北川悠理': ['0405', 'kitagawa-yuri'],
    '柴田柚菜': ['0406', 'shibata-yuna'],
    '清宮レイ': ['0407', 'seimi-yarei'],
    '田村真佑': ['0408', 'tamura-mayu'],
    '筒井あやめ': ['0409', 'tsutsui-ayame'],
    '早川聖来': ['0410', 'hayakawa-seira'],
    '矢久保美緒': ['0411', 'yakubo-mio'],



    '石森虹花': ['1101', 'ishimori-nijika'],
    '今泉佑唯': ['1102', 'imaizumi-yui'],
    '上村莉菜': ['1103', 'uemura-rina'],
    '尾関梨香': ['1104', 'ozeki-rika'],
    '織田奈那': ['1105', 'oda-nana'],
    '小池美波': ['1106', 'koike-minami'],
    '小林由依': ['1107', 'kobayashi-yui'],
    '齋藤冬優花': ['1108', 'saitou-fuyuka'],
    '佐藤詩織': ['1109', 'satou-shiori'],
    '志田愛佳': ['1110', 'shida-manaka'],
    '菅井友香': ['1111', 'sugai-yuuka'],
    '鈴本美愉': ['1112', 'suzumoto-miyu'],
    '長沢菜々香': ['1113', 'nagasawa-nanako'],
    '土生瑞穂': ['1114', 'habu-mizuho'],
    '原田葵': ['1115', 'harada-aoi'],

    '平手友梨奈': ['1117', 'hirate-yurina'],
    '守屋茜': ['1118', 'moriya-akane'],
    '米谷奈々未': ['1119', 'yonetani-nanami'],
    '渡辺梨加': ['1120', 'watanabe-rika'],
    '渡邉理佐': ['1121', 'watanabe-risa'],
    '長濱ねる': ['1122', 'nagahama-neru'],
    '井上梨名': ['1201', 'inoue-rina'],
    '関有美子': ['1202', 'seki-yumiko'],
    '武元唯衣': ['1203', 'takemoto-yui'],
    '田村保乃': ['1204', 'tamura-hono'],
    '藤吉夏鈴': ['1205', 'fujiyoshi-karin'],
    '松田里奈': ['1206', 'matsuda-rina'],
    '松平璃子': ['1207', 'matsudaira-riko'],
    '森田ひかる': ['1208', 'morita-hikaru'],
    '山﨑天': ['1209', 'yamasaki-ten'],
    '遠藤光莉': ['1210', 'endo-hikari'],
    '大園玲': ['1211', 'ozono-rei'],
    '大沼晶保': ['1212', 'onuma-akiho'],
    '幸阪茉里乃': ['1213', 'kousaka-marino'],
    '増本綺良': ['1214', 'masumoto-kira'],
    '守屋麗奈': ['1215', 'moriya-rena'],



    '井口眞緒': ['2101', 'iguchi-mao'],
    '潮紗理菜': ['2102', 'ushio-sarina'],
    '柿崎芽実': ['2103', 'kakizaki-memi'],
    '影山優佳': ['2104', 'kageyama-yuuka'],
    '加藤史帆': ['2105', 'katou-shiho'],
    '齊藤京子': ['2106', 'saitou-kyouko'],
    '佐々木久美': ['2107', 'sasaki-kumi'],
    '佐々木美玲': ['2108', 'sasaki-mirei'],
    '高瀬愛奈': ['2109', 'takase-mana'],
    '高本彩花': ['2110', 'takamoto-ayaka'],
    '東村芽依': ['2111', 'higashimura-mei'],
    '金村美玖': ['2201', 'kanemura-miku'],
    '河田陽菜': ['2202', 'kawata-hina'],
    '小坂菜緒': ['2203', 'kosaka-nao'],
    '富田鈴花': ['2204', 'tomita-suzuka'],
    '丹生明里': ['2205', 'nibu-akari'],
    '濱岸ひより': ['2206', 'hamagisi-hiyori'],
    '松田好花': ['2207', 'matsuda-konoka'],
    '宮田愛萌': ['2208', 'miyata-manamo'],
    '渡邉美穂': ['2209', 'watanabe-miho'],
    '上村ひなの': ['2301', 'kamimura-hinano'],
    '髙橋未来虹': ['2302', 'takahashi-mikuni'],
    '森本茉莉': ['2303', 'morimoto-marii'],
    '山口陽世': ['2304', 'yamaguchi-haruyo'],
}

def get_id(name):
    return members[name][0]

def get_romaji(name):
    return members[name][1]

def identify(author, title):

    if author == '３期生':

        rules = [
            ['伊藤々杏', '伊藤理々杏'],
            ['伊藤理々杏', '伊藤理々杏'],
            ['伊藤 理々杏', '伊藤理々杏'],
            ['岩本蓮加', '岩本蓮加'],
            ['岩本 蓮加', '岩本蓮加'],
            [' 本蓮加', '岩本蓮加'],
            ['梅澤美波', '梅澤美波'],
            ['梅澤 美波', '梅澤美波'],
            ['大園桃子', '大園桃子'],
            ['大園 桃子', '大園桃子'],
            ['久保史緖里', '久保史緒里'],
            ['久保史緒里', '久保史緒里'],
            ['久保 史緒里', '久保史緒里'],
            ['史緒里', '久保史緒里'],
            ['阪口珠美', '阪口珠美'],
            ['阪口 珠美', '阪口珠美'],
            ['阪口美', '阪口珠美'],
            ['佐藤楓', '佐藤楓'],
            ['佐藤 楓', '佐藤楓'],
            ['中麗乃', '中村麗乃'],
            ['中村麗乃', '中村麗乃'],
            ['中村 麗乃', '中村麗乃'],
            ['向井葉月', '向井葉月'],
            ['向井 葉月', '向井葉月'],
            ['向葉月。', '向井葉月'],
            ['向井葉', '向井葉月'],
            ['山美月', '山下美月'],
            ['山下美月', '山下美月'],
            ['山下 美月', '山下美月'],
            ['吉田綾乃クリスティー', '吉田綾乃クリスティー'],
            ['吉田綾乃 クリスティー', '吉田綾乃クリスティー'],
            ['吉田 綾乃 クリスティー', '吉田綾乃クリスティー'],
            ['与田祐希', '与田祐希'],
            ['与田 祐希', '与田祐希'],
        ]

    elif author == 'けやき坂462期生':

        rules = [
            ['金村美玖', '金村美玖'],
            ['河田陽菜', '河田陽菜'],
            ['小坂菜緒', '小坂菜緒'],
            ['富田鈴花', '富田鈴花'],
            ['丹生明里', '丹生明里'],
            ['濱岸ひより', '濱岸ひより'],
            ['松田好花', '松田好花'],
            ['宮田愛萌', '宮田愛萌'],
            ['渡邉美穂', '渡邉美穂'],
        ]

    elif author == '欅坂46二期生':

        rules = [
            ['井上梨名', '井上梨名'],
            ['関有美子', '関有美子'],
            ['武元唯衣', '武元唯衣'],
            ['田村保乃', '田村保乃'],
            ['藤吉夏鈴', '藤吉夏鈴'],
            ['松田里奈', '松田里奈'],
            ['松平璃子', '松平璃子'],
            ['森田ひかる', '森田ひかる'],
            ['山﨑天', '山﨑天'],
            ['山﨑 天', '山﨑天'],
        ]

    elif author == '４期生':

        rules = [
            ['遠藤さくら', '遠藤さくら'],
            ['賀喜遥香', '賀喜遥香'],
            ['賀喜 遥香', '賀喜遥香'],
            ['掛橋沙耶香', '掛橋沙耶香'],
            ['金川紗耶', '金川紗耶'],
            ['北川悠理', '北川悠理'],
            ['柴田柚菜', '柴田柚菜'],
            ['清宮レイ', '清宮レイ'],
            ['田村真佑', '田村真佑'],
            ['筒井あやめ', '筒井あやめ'],
            ['早川聖来', '早川聖来'],
            ['矢久保美緒', '矢久保美緒'],
        ]

    elif author == '欅坂46新二期生':

        rules = [
            ['遠藤光莉', '遠藤光莉'],
            ['大園玲', '大園玲'],
            ['大沼晶保', '大沼晶保'],
            ['幸阪茉里乃', '幸阪茉里乃'],
            ['増本綺良', '増本綺良'],
            ['守屋麗奈', '守屋麗奈'],
        ]

    elif author == '日向坂46新三期生':

        rules = [
            ['髙橋 未来虹', '髙橋未来虹'],
            ['森本 茉莉', '森本茉莉'],
            ['山口 陽世', '山口陽世'],
        ]

    else:

        rules = []

    for rule in rules:
        if title.find(rule[0]) != -1:
            author = rule[1]
            title = re.sub(rule[0], '', title)
            title = re.sub(r'[\xa0|\s]*$', '', title)
            break

    return (author, title)

def bind(author, feed_id):

    correct = {
        '1019921': '山﨑天',
        '1028268': '山﨑天',
        '0054642': '北川悠理',
        '1033182': '髙橋未来虹'
    }

    if feed_id in correct:
        return correct[feed_id]
    else:
        return author
