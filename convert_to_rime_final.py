import json
import re
import os
from pypinyin import lazy_pinyin, Style

# 日语假名单字
KANA_ENTRIES = [
    ('あ', 'a', 1000), ('い', 'i', 1000), ('う', 'u', 1000), ('え', 'e', 1000), ('お', 'o', 1000),
    ('か', 'ka', 1000), ('き', 'ki', 1000), ('く', 'ku', 1000), ('け', 'ke', 1000), ('こ', 'ko', 1000),
    ('さ', 'sa', 1000), ('し', 'shi', 1000), ('す', 'su', 1000), ('せ', 'se', 1000), ('そ', 'so', 1000),
    ('た', 'ta', 1000), ('ち', 'chi', 1000), ('つ', 'tsu', 1000), ('て', 'te', 1000), ('と', 'to', 1000),
    ('な', 'na', 1000), ('に', 'ni', 1000), ('ぬ', 'nu', 1000), ('ね', 'ne', 1000), ('の', 'no', 1000),
    ('は', 'ha', 1000), ('ひ', 'hi', 1000), ('ふ', 'fu', 1000), ('へ', 'he', 1000), ('ほ', 'ho', 1000),
    ('ま', 'ma', 1000), ('み', 'mi', 1000), ('む', 'mu', 1000), ('め', 'me', 1000), ('も', 'mo', 1000),
    ('や', 'ya', 1000), ('ゆ', 'yu', 1000), ('よ', 'yo', 1000),
    ('ら', 'ra', 1000), ('り', 'ri', 1000), ('る', 'ru', 1000), ('れ', 're', 1000), ('ろ', 'ro', 1000),
    ('わ', 'wa', 1000), ('を', 'wo', 1000), ('ん', 'n', 1000),
    # 浊音
    ('が', 'ga', 900), ('ぎ', 'gi', 900), ('ぐ', 'gu', 900), ('げ', 'ge', 900), ('ご', 'go', 900),
    ('ざ', 'za', 900), ('じ', 'ji', 900), ('ず', 'zu', 900), ('ぜ', 'ze', 900), ('ぞ', 'zo', 900),
    ('だ', 'da', 900), ('ぢ', 'di', 900), ('づ', 'du', 900), ('で', 'de', 900), ('ど', 'do', 900),
    ('ば', 'ba', 900), ('び', 'bi', 900), ('ぶ', 'bu', 900), ('べ', 'be', 900), ('ぼ', 'bo', 900),
    ('ぱ', 'pa', 900), ('ぴ', 'pi', 900), ('ぷ', 'pu', 900), ('ぺ', 'pe', 900), ('ぽ', 'po', 900),
    # 拗音
    ('きゃ', 'kya', 800), ('きゅ', 'kyu', 800), ('きょ', 'kyo', 800),
    ('しゃ', 'sha', 800), ('しゅ', 'shu', 800), ('しょ', 'sho', 800),
    ('ちゃ', 'cha', 800), ('ちゅ', 'chu', 800), ('ちょ', 'cho', 800),
    ('にゃ', 'nya', 800), ('にゅ', 'nyu', 800), ('にょ', 'nyo', 800),
    ('ひゃ', 'hya', 800), ('ひゅ', 'hyu', 800), ('ひょ', 'hyo', 800),
    ('みゃ', 'mya', 800), ('みゅ', 'myu', 800), ('みょ', 'myo', 800),
    ('りゃ', 'rya', 800), ('りゅ', 'ryu', 800), ('りょ', 'ryo', 800),
    ('ぎゃ', 'gya', 800), ('ぎゅ', 'gyu', 800), ('ぎょ', 'gyo', 800),
    ('じゃ', 'ja', 800), ('じゅ', 'ju', 800), ('じょ', 'jo', 800),
    ('びゃ', 'bya', 800), ('びゅ', 'byu', 800), ('びょ', 'byo', 800),
    ('ぴゃ', 'pya', 800), ('ぴゅ', 'pyu', 800), ('ぴょ', 'pyo', 800),
    # 片假名
    ('ア', 'a', 900), ('イ', 'i', 900), ('ウ', 'u', 900), ('エ', 'e', 900), ('オ', 'o', 900),
    ('カ', 'ka', 900), ('キ', 'ki', 900), ('ク', 'ku', 900), ('ケ', 'ke', 900), ('コ', 'ko', 900),
    ('サ', 'sa', 900), ('シ', 'shi', 900), ('ス', 'su', 900), ('セ', 'se', 900), ('ソ', 'so', 900),
    ('タ', 'ta', 900), ('チ', 'chi', 900), ('ツ', 'tsu', 900), ('テ', 'te', 900), ('ト', 'to', 900),
    ('ナ', 'na', 900), ('ニ', 'ni', 900), ('ヌ', 'nu', 900), ('ネ', 'ne', 900), ('ノ', 'no', 900),
    ('ハ', 'ha', 900), ('ヒ', 'hi', 900), ('フ', 'fu', 900), ('ヘ', 'he', 900), ('ホ', 'ho', 900),
    ('マ', 'ma', 900), ('ミ', 'mi', 900), ('ム', 'mu', 900), ('メ', 'me', 900), ('モ', 'mo', 900),
    ('ヤ', 'ya', 900), ('ユ', 'yu', 900), ('ヨ', 'yo', 900),
    ('ラ', 'ra', 900), ('リ', 'ri', 900), ('ル', 'ru', 900), ('レ', 're', 900), ('ロ', 'ro', 900),
    ('ワ', 'wa', 900), ('ヲ', 'wo', 900), ('ン', 'n', 900),
]

# 日本汉字多音字
JP_KANJI_POLYPHONIC = [
    ('雫', 'na', 5000),
    ('辻', 'shi', 3000),
    ('峠', 'ka', 3000),
    ('凪', 'zhi', 3000),
    ('喰', 'can', 3000),
    ('喰', 'sun', 2000),
]

# 假名转罗马音对照表
KANA_TO_ROMA = {
    # 平假名
    'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
    'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
    'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
    'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
    'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
    'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
    'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
    'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
    'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
    'わ': 'wa', 'を': 'wo', 'ん': 'n',
    'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
    'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
    'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
    'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
    'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
    'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
    'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
    'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
    'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
    'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
    'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
    'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',
    'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
    'じゃ': 'ja', 'じゅ': 'ju', 'じょ': 'jo',
    'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
    'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo',
    'っ': '',
    # 片假名
    'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
    'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
    'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
    'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
    'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
    'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ': 'ho',
    'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
    'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
    'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
    'ワ': 'wa', 'ヲ': 'wo', 'ン': 'n',
    'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
    'ザ': 'za', 'ジ': 'ji', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
    'ダ': 'da', 'ヂ': 'ji', 'ヅ': 'zu', 'デ': 'de', 'ド': 'do',
    'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
    'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',
    'キャ': 'kya', 'キュ': 'kyu', 'キョ': 'kyo',
    'シャ': 'sha', 'シュ': 'shu', 'ショ': 'sho',
    'チャ': 'cha', 'チュ': 'chu', 'チョ': 'cho',
    'ニャ': 'nya', 'ニュ': 'nyu', 'ニョ': 'nyo',
    'ヒャ': 'hya', 'ヒュ': 'hyu', 'ヒョ': 'hyo',
    'ミャ': 'mya', 'ミュ': 'myu', 'ミョ': 'myo',
    'リャ': 'rya', 'リュ': 'ryu', 'リョ': 'ryo',
    'ギャ': 'gya', 'ギュ': 'gyu', 'ギョ': 'gyo',
    'ジャ': 'ja', 'ジュ': 'ju', 'ジョ': 'jo',
    'ビャ': 'bya', 'ビュ': 'byu', 'ビョ': 'byo',
    'ピャ': 'pya', 'ピュ': 'pyu', 'ピョ': 'pyo',
    'ッ': '', 'ー': '-',
}

def kana_to_romaji(text):
    result = ''
    i = 0
    while i < len(text):
        if i + 1 < len(text):
            two_char = text[i:i+2]
            if two_char in KANA_TO_ROMA:
                result += KANA_TO_ROMA[two_char]
                i += 2
                continue
        one_char = text[i]
        if one_char in KANA_TO_ROMA:
            result += KANA_TO_ROMA[one_char]
        else:
            result += one_char
        i += 1
    return result

# 加载日本姓氏
JP_SURNAMES = set()
surname_file = os.path.join(os.path.dirname(__file__), 'japanese_surnames.txt')
if os.path.exists(surname_file):
    with open(surname_file, 'r', encoding='utf-8') as f:
        for line in f:
            JP_SURNAMES.add(line.strip())
    print(f'Loaded {len(JP_SURNAMES)} Japanese surnames')

# 加载已分离的名字
SPLIT_NAMES = {}
split_file = os.path.join(os.path.dirname(__file__), 'names_splitted.txt')
if os.path.exists(split_file):
    with open(split_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3 and parts[1]:
                SPLIT_NAMES[parts[0]] = (parts[1], parts[2])
    print(f'Loaded {len(SPLIT_NAMES)} pre-split names')

# 加载日文到中文翻译
JP_CN_TRANSLATIONS = {}
trans_file = os.path.join(os.path.dirname(__file__), 'jp_cn_translations.txt')
if os.path.exists(trans_file):
    with open(trans_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                JP_CN_TRANSLATIONS[parts[0]] = parts[1]
    print(f'Loaded {len(JP_CN_TRANSLATIONS)} JP-CN translations')

def remove_tone(pinyin):
    tone_map = {
        'ā': 'a', 'á': 'a', 'ǎ': 'a', 'à': 'a',
        'ē': 'e', 'é': 'e', 'ě': 'e', 'è': 'e',
        'ī': 'i', 'í': 'i', 'ǐ': 'i', 'ì': 'i',
        'ō': 'o', 'ó': 'o', 'ǒ': 'o', 'ò': 'o',
        'ū': 'u', 'ú': 'u', 'ǔ': 'u', 'ù': 'u',
        'ǖ': 'v', 'ǘ': 'v', 'ǚ': 'v', 'ǜ': 'v',
        'ü': 'v'
    }
    result = ''
    for char in pinyin:
        result += tone_map.get(char, char)
    return result

def get_pinyin(word):
    pinyin_list = lazy_pinyin(word, style=Style.TONE)
    result = ''
    for p in pinyin_list:
        result += remove_tone(p)
    return result

def is_valid_chinese_word(word, allow_single=False):
    if not word or len(word.strip()) == 0:
        return False
    
    if len(word) > 8:
        return False
    
    if len(word) < 2:
        if allow_single and len(word) == 1 and is_surname(word):
            return True
        return False
    
    for char in word:
        if not ('\u4e00' <= char <= '\u9fff'):
            return False
    
    return True

def is_surname(word):
    return word in SINGLE_SURNAMES or word in DOUBLE_SURNAMES

SINGLE_SURNAMES = set('赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史')

DOUBLE_SURNAMES = set([
    '欧阳','司马','上官','诸葛','慕容','夏侯','皇甫','尉迟','公羊','澹台','公孙','轩辕','东方','赫连','呼延','宇文','太史','端木','司徒','司空','亓官','司寇','仉督','子车','颛孙','壤驷','公良','漆雕','乐正','夹谷','宰父','谷利','晋','楚','闫',
    '伊藤','丰田','松下','索尼','任天堂','大桥','山川','佐藤','铃木','高橋','山本','中村','小林','加藤','吉田','山田','佐々木','近藤','齐藤','藤堂','黑崎','久保','木之本','土屋','卡斯兰','德丽莎','符华'
])

def split_name(name):
    # 如果有预分离的结果，直接使用
    if name in SPLIT_NAMES:
        surname, given = SPLIT_NAMES[name]
        return [name, surname, given]
    
    parts = []
    name_len = len(name)
    
    if name_len == 2:
        parts.append(name)
    elif name_len >= 3:
        if name[:2] in DOUBLE_SURNAMES:
            parts.append(name)
            if name_len == 3:
                parts.append(name[:2])
                parts.append(name[2:])
            elif name_len == 4:
                parts.append(name[:2])
                parts.append(name[2:])
            else:
                parts.append(name[:2])
                parts.append(name[2:4])
                parts.append(name[2:])
        else:
            parts.append(name)
            if name_len == 3:
                parts.append(name[0])
                parts.append(name[1:])
            elif name_len == 4:
                parts.append(name[:2])
                parts.append(name[2:])
            else:
                parts.append(name[0])
                parts.append(name[:2])
                parts.append(name[2:4])
                parts.append(name[1:])
    
    return parts

def get_english_weight(word, base_weight):
    short_abbr = re.compile(r'^(TV|OVA|PC|PS[2345]?|RPG|AVG|ACT|GAL|OST|ED|OP|WEB|JRPG|ARPG|OAD|NDS|PSP|STEAM|JUMP|R18|3D|FPS|RTS|STG|SRPG|AIR|ELF|ARC|ADV|SLG|MOBILE|EVA|JOJO|KEY|BGM|CD|DVD|BL|GL|UC|IX|IQ|NET|AMV|MAD)$', re.IGNORECASE)
    if short_abbr.match(word):
        return base_weight // 10
    
    if re.match(r'^[A-Z]{1,4}$', word):
        return base_weight // 10
    
    if re.match(r'^\d+[A-Za-z]*$', word) or re.match(r'^[A-Za-z]+\d+$', word):
        return base_weight // 2
    
    return base_weight

def scale_weight(weight):
    if weight == 0:
        return 1
    
    if weight > 100000:
        return weight // 20
    elif weight > 50000:
        return weight // 15
    elif weight > 10000:
        return weight // 10
    elif weight > 5000:
        return weight // 5
    elif weight > 1000:
        return weight // 3
    elif weight > 100:
        return weight // 2
    else:
        return max(weight, 1)

def extract_chinese_name(infobox):
    if not infobox:
        return None
    
    match = re.search(r'简体中文名=\s*([^\r\n]+)', infobox)
    if match:
        return match.group(1).strip()
    return None

def extract_aliases(infobox):
    if not infobox:
        return []
    
    aliases = []
    
    alias_match = re.search(r'别名=\s*\{([^}]+)\}', infobox, re.DOTALL)
    if alias_match:
        alias_text = alias_match.group(1)
        alias_list = re.findall(r'\[([^\]]+)\]', alias_text)
        for alias in alias_list:
            alias = alias.strip()
            if alias and not alias.startswith('第二中文名') and not alias.startswith('英文名'):
                aliases.append(alias)
    
    return aliases

def extract_nickname(infobox):
    if not infobox:
        return []
    
    nicknames = []
    nick_match = re.search(r'昵称=\s*([^\r\n]+)', infobox)
    if nick_match:
        nick_text = nick_match.group(1).strip()
        if nick_text:
            nick_list = re.findall(r'\[([^\]]+)\]', nick_text)
            nicknames.extend([n.strip() for n in nick_list])
    
    return nicknames

def process_character_jsonlines(filepath):
    words = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                data = json.loads(line)
            except:
                continue
            
            collects = data.get('collects', 0)
            
            infobox = data.get('infobox', '')
            
            chinese_name = extract_chinese_name(infobox)
            if chinese_name and is_valid_chinese_word(chinese_name):
                words[chinese_name] = words.get(chinese_name, 0) + collects + 1
                
                for part in split_name(chinese_name):
                    if part and is_valid_chinese_word(part, allow_single=True):
                        words[part] = words.get(part, 0) + collects // 4 + 1
            
            aliases = extract_aliases(infobox)
            for alias in aliases:
                if alias and is_valid_chinese_word(alias):
                    words[alias] = words.get(alias, 0) + collects // 2 + 1
                    
                    for part in split_name(alias):
                        if part and is_valid_chinese_word(part, allow_single=True):
                            words[part] = words.get(part, 0) + collects // 8 + 1
            
            nicknames = extract_nickname(infobox)
            for nick in nicknames:
                if nick and is_valid_chinese_word(nick):
                    words[nick] = words.get(nick, 0) + collects // 2 + 1
                    
                    for part in split_name(nick):
                        if part and is_valid_chinese_word(part, allow_single=True):
                            words[part] = words.get(part, 0) + collects // 8 + 1
    
    return words

def process_person_jsonlines(filepath):
    words = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                data = json.loads(line)
            except:
                continue
            
            collects = data.get('collects', 0)
            
            infobox = data.get('infobox', '')
            
            chinese_name = extract_chinese_name(infobox)
            if chinese_name and is_valid_chinese_word(chinese_name):
                words[chinese_name] = words.get(chinese_name, 0) + collects + 1
                
                for part in split_name(chinese_name):
                    if part and is_valid_chinese_word(part, allow_single=True):
                        words[part] = words.get(part, 0) + collects // 4 + 1
            
            aliases = extract_aliases(infobox)
            for alias in aliases:
                if alias and is_valid_chinese_word(alias):
                    words[alias] = words.get(alias, 0) + collects // 2 + 1
                    
                    for part in split_name(alias):
                        if part and is_valid_chinese_word(part, allow_single=True):
                            words[part] = words.get(part, 0) + collects // 8 + 1
            
            nicknames = extract_nickname(infobox)
            for nick in nicknames:
                if nick and is_valid_chinese_word(nick):
                    words[nick] = words.get(nick, 0) + collects // 2 + 1
                    
                    for part in split_name(nick):
                        if part and is_valid_chinese_word(part, allow_single=True):
                            words[part] = words.get(part, 0) + collects // 8 + 1
    
    return words

def is_valid_english_word(word):
    if not word or len(word.strip()) == 0:
        return False
    
    if len(word) > 30:
        return False
    
    if len(word) < 2:
        return False
    
    if re.search(r'[\u4e00-\u9fff]', word):
        return False
    
    if re.match(r'^\d+$', word):
        return False
    
    if not re.match(r'^[a-zA-Z0-9\s\.\-\+]+$', word):
        return False
    
    return True

def process_subject_jsonlines(filepath):
    chinese_words = {}
    english_words = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                data = json.loads(line)
            except:
                continue
            
            score = data.get('score', 0)
            collect_count = data.get('favorite', {}).get('done', 0)
            weight = int(score * 10) + collect_count // 10
            
            if 'name_cn' in data:
                name_cn = data.get('name_cn', '')
                if name_cn and is_valid_chinese_word(name_cn):
                    chinese_words[name_cn] = chinese_words.get(name_cn, 0) + weight
                    for part in split_name(name_cn):
                        if is_valid_chinese_word(part):
                            chinese_words[part] = chinese_words.get(part, 0) + weight // 2
            
            infobox = data.get('infobox', '')
            
            chinese_name = extract_chinese_name(infobox)
            if chinese_name and is_valid_chinese_word(chinese_name):
                chinese_words[chinese_name] = chinese_words.get(chinese_name, 0) + weight
                for part in split_name(chinese_name):
                    if is_valid_chinese_word(part):
                        chinese_words[part] = chinese_words.get(part, 0) + weight // 2
            
            aliases = extract_aliases(infobox)
            for alias in aliases:
                if alias and is_valid_chinese_word(alias):
                    chinese_words[alias] = chinese_words.get(alias, 0) + weight // 2
                    for part in split_name(alias):
                        if is_valid_chinese_word(part):
                            chinese_words[part] = chinese_words.get(part, 0) + weight // 4
            
            tags = data.get('tags', [])
            for tag in tags:
                tag_name = tag.get('name', '')
                tag_count = tag.get('count', 0)
                
                if is_valid_english_word(tag_name) and tag_count >= 30 and score >= 6.5:
                    w = tag_count + weight
                    english_words[tag_name] = english_words.get(tag_name, 0) + w
            
            name = data.get('name', '')
            if is_valid_english_word(name) and score >= 7.0 and collect_count >= 30:
                english_words[name] = english_words.get(name, 0) + weight
    
    return chinese_words, english_words

def main():
    base_dir = r"C:\Users\feohz\Documents\bagumi_local"
    
    all_chinese_words = {}
    all_english_words = {}
    
    print("Processing character.jsonlines...")
    char_words = process_character_jsonlines(os.path.join(base_dir, 'character.jsonlines'))
    for word, weight in char_words.items():
        all_chinese_words[word] = all_chinese_words.get(word, 0) + weight
    print(f"  Found {len(char_words)} words")
    
    print("Processing person.jsonlines...")
    person_words = process_person_jsonlines(os.path.join(base_dir, 'person.jsonlines'))
    for word, weight in person_words.items():
        all_chinese_words[word] = all_chinese_words.get(word, 0) + weight
    print(f"  Found {len(person_words)} words")
    
    print("Processing subject.jsonlines...")
    subject_cn, subject_en = process_subject_jsonlines(os.path.join(base_dir, 'subject.jsonlines'))
    for word, weight in subject_cn.items():
        all_chinese_words[word] = all_chinese_words.get(word, 0) + weight
    for word, weight in subject_en.items():
        weight = get_english_weight(word, weight)
        all_english_words[word] = all_english_words.get(word, 0) + weight
    print(f"  Found {len(subject_cn)} Chinese words, {len(subject_en)} English words")
    
    # 添加日文翻译
    print(f"\nAdding {len(JP_CN_TRANSLATIONS)} JP-CN translations...")
    for jp_name, cn_name in JP_CN_TRANSLATIONS.items():
        if cn_name and is_valid_chinese_word(cn_name):
            # 中文翻译
            all_chinese_words[cn_name] = all_chinese_words.get(cn_name, 0) + 50
            # 分词
            for part in split_name(cn_name):
                if part and is_valid_chinese_word(part, allow_single=True):
                    all_chinese_words[part] = all_chinese_words.get(part, 0) + 20
    
    print(f"\nScaling weights and writing output...")
    
    output_path = os.path.join(base_dir, 'bangumi.dict.yaml')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Rime dictionary - Bangumi\n")
        f.write("# encoding: utf-8\n\n")
        f.write("---\n")
        f.write("name: bangumi\n")
        f.write("version: \"2026-03-01\"\n")
        f.write("sort: by_weight\n")
        f.write("...\n\n")
        
        all_words_list = []
        
        for word, weight in all_chinese_words.items():
            if word and len(word) > 0:
                scaled_weight = scale_weight(weight)
                pinyin = get_pinyin(word)
                all_words_list.append((word, pinyin, scaled_weight))
        
        for word, weight in all_english_words.items():
            if word and len(word) > 0:
                scaled_weight = scale_weight(weight)
                all_words_list.append((word, word.lower().replace(' ', ''), scaled_weight))
        
        # 过滤英文词条：保留权重 >= 89 的（删除约60%低权重英文）
        english_threshold = 89
        all_words_list = [(w, p, wt) for w, p, wt in all_words_list 
                          if not re.match(r'^[A-Za-z]', w) or wt >= english_threshold]
        
        # 为没有翻译的日文假名名字添加罗马音
        jp_kana_words = []
        for jp_name, cn_name in JP_CN_TRANSLATIONS.items():
            # 如果有中文翻译，跳过
            continue
        
        # 读取名字分离结果，为假名名字添加罗马音
        for line in open(os.path.join(base_dir, 'names_splitted.txt'), 'r', encoding='utf-8'):
            parts = line.strip().split('\t')
            if len(parts) >= 3 and parts[1]:
                name = parts[0]
                # 只处理包含假名的名字
                if re.search(r'[\u3040-\u309F\u30A0-\u30FF]', name):
                    # 如果没有中文翻译，用罗马音
                    if name not in JP_CN_TRANSLATIONS:
                        romaji = kana_to_romaji(name)
                        if romaji and romaji != name:
                            jp_kana_words.append((name, romaji, 30))
        
        print(f"Added {len(jp_kana_words)} JP kana names with romaji")
        all_words_list.extend(jp_kana_words)
        
        all_words_list.extend(KANA_ENTRIES)
        print(f"Added {len(KANA_ENTRIES)} kana entries")
        
        all_words_list.extend(JP_KANJI_POLYPHONIC)
        print(f"Added {len(JP_KANJI_POLYPHONIC)} Japanese kanji polyphonic entries")
        
        all_words_list.sort(key=lambda x: -x[2])
        
        for word, pinyin, weight in all_words_list:
            f.write(f"{word}\t{pinyin}\t{weight}\n")
    
    print(f"\nTotal Chinese words: {len(all_chinese_words)}")
    print(f"Total English words: {len(all_english_words)}")
    print(f"Total unique words: {len(all_words_list)}")
    print(f"Output saved to: {output_path}")

if __name__ == '__main__':
    main()
