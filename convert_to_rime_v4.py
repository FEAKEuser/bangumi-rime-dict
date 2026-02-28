import json
import re
import os
from pypinyin import lazy_pinyin, Style

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

def is_valid_chinese_word(word):
    if not word or len(word.strip()) == 0:
        return False
    
    if len(word) > 8:
        return False
    
    if len(word) < 2:
        return False
    
    for char in word:
        if not ('\u4e00' <= char <= '\u9fff'):
            return False
    
    return True

def get_english_weight(word, base_weight):
    short_abbr = re.compile(r'^(TV|OVA|PC|PS[2345]?|RPG|AVG|ACT|GAL|OST|ED|OP|WEB|JRPG|ARPG|OAD|NDS|PSP|STEAM|JUMP|R18|3D|FPS|RTS|STG|SRPG|AIR|ELF|ARC|ADV|SLG|MOBILE|EVA|JOJO|KEY|BGM|CD|DVD|BL|GL|UC|IX|IQ|NET|AMV|MAD)$', re.IGNORECASE)
    if short_abbr.match(word):
        return base_weight // 10
    
    if re.match(r'^[A-Z]{1,4}$', word):
        return base_weight // 10
    
    if re.match(r'^\d+[A-Za-z]*$', word) or re.match(r'^[A-Za-z]+\d+$', word):
        return base_weight // 2
    
    return base_weight

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
            
            aliases = extract_aliases(infobox)
            for alias in aliases:
                if alias and is_valid_chinese_word(alias):
                    words[alias] = words.get(alias, 0) + collects // 2 + 1
            
            nicknames = extract_nickname(infobox)
            for nick in nicknames:
                if nick and is_valid_chinese_word(nick):
                    words[nick] = words.get(nick, 0) + collects // 2 + 1
    
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
            
            aliases = extract_aliases(infobox)
            for alias in aliases:
                if alias and is_valid_chinese_word(alias):
                    words[alias] = words.get(alias, 0) + collects // 2 + 1
            
            nicknames = extract_nickname(infobox)
            for nick in nicknames:
                if nick and is_valid_chinese_word(nick):
                    words[nick] = words.get(nick, 0) + collects // 2 + 1
    
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
            
            infobox = data.get('infobox', '')
            
            chinese_name = extract_chinese_name(infobox)
            if chinese_name and is_valid_chinese_word(chinese_name):
                chinese_words[chinese_name] = chinese_words.get(chinese_name, 0) + weight
            
            aliases = extract_aliases(infobox)
            for alias in aliases:
                if alias and is_valid_chinese_word(alias):
                    chinese_words[alias] = chinese_words.get(alias, 0) + weight // 2
            
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
    
    print(f"\nGenerating pinyin and writing output...")
    
    output_path = os.path.join(base_dir, 'bangumi.dict.yaml')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Rime dictionary - Bangumi\n")
        f.write("# encoding: utf-8\n\n")
        f.write("---\n")
        f.write("name: bangumi\n")
        f.write("version: \"2026-02-28\"\n")
        f.write("sort: by_weight\n")
        f.write("...\n\n")
        
        all_words_list = []
        
        for word, weight in all_chinese_words.items():
            if word and len(word) > 0:
                pinyin = get_pinyin(word)
                all_words_list.append((word, pinyin, weight))
        
        for word, weight in all_english_words.items():
            if word and len(word) > 0:
                all_words_list.append((word, word.lower().replace(' ', ''), weight))
        
        all_words_list.sort(key=lambda x: -x[2])
        
        for word, pinyin, weight in all_words_list:
            f.write(f"{word}\t{pinyin}\t{weight}\n")
    
    print(f"\nTotal Chinese words: {len(all_chinese_words)}")
    print(f"Total English words: {len(all_english_words)}")
    print(f"Total unique words: {len(all_words_list)}")
    print(f"Output saved to: {output_path}")

if __name__ == '__main__':
    main()
