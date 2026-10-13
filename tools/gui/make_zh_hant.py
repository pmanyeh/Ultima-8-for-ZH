"""Fill scummvm-src/po/zh_Hant.po from zh_Hans.po (OpenCC s2twp, Taiwan
phrasing) plus fixes, and append the strings of the Ultima VIII options.

Start from the empty upstream zh_Hant.po (the script fills msgstr from
zh_Hans.po every time, so running it again on its own output also works):

    pip install opencc-python-reimplemented
    python tools/gui/make_zh_hant.py

Then rebuild gui/themes/translations.dat from all the po files (WSL):

    g++ -O2 -o create_translations devtools/create_translations/*.cpp
    ./create_translations translations.dat po/*.po && mv translations.dat gui/themes/

New strings of the Ultima VIII options: add them to ULTIMA below.
"""
import re, sys
from opencc import OpenCC
sys.stdout.reconfigure(encoding='utf-8')

PO = r'D:\git\Ultima 8 for ZH\scummvm-src\po'
cc = OpenCC('s2twp')

# after OpenCC: wording used in Taiwan / in this project
FIXES = [
    ('全屏', '全螢幕'), ('影片模式', '顯示模式'), ('寬屏', '寬螢幕'),
    ('存檔遊戲', '存檔'), ('遊戲存檔', '存檔'),
    ('鍵位', '按鍵'), ('質量', '品質'), ('信號', '訊號'),
    ('默認', '預設'), ('缺省', '預設'), ('屏幕', '螢幕'),
    ('激活', '啟用'), ('文本', '文字'), ('運行', '執行'), ('調色板', '調色盤'),
    ('項目', '專案'),
    ('全域性', '全域'), ('覆蓋全域', '覆寫全域'), ('退出', '離開'), ('矯正', '校正'),
    ('縱橫比', '長寬比'), ('寬高比', '長寬比'), ('首選', '偏好'), ('地址', '位址'),
    ('遮蔽全部', '全部靜音'), ('聲音字型', 'SoundFont'), ('音色庫', 'SoundFont'),
]

# whole translations, by msgid
EXACT = {
    '~O~K': '確定 (~O~)',
    'OK': '確定',
    'Okay': '確定',
    'Keymaps': '按鍵對應',
    '~R~emove Game': '移除遊戲 (~R~)',
}


def parse(path):
    """[(header_lines, {'msgctxt':..,'msgid':..,'msgid_plural':..,'msgstr':..|{n:..}}, raw_block)]"""
    text = open(path, encoding='utf-8').read()
    out = []
    for block in text.split('\n\n'):
        entry = {}
        cur = None
        for line in block.split('\n'):
            m = re.match(r'^(msgctxt|msgid_plural|msgid|msgstr(?:\[\d+\])?) "(.*)"$', line)
            if m:
                cur = m.group(1)
                entry[cur] = m.group(2)
            elif cur and line.startswith('"') and line.endswith('"'):
                entry[cur] += line[1:-1]
            elif line.startswith('#~'):
                entry['obsolete'] = True
        out.append((block, entry))
    return out


def key(e):
    return (e.get('msgctxt'), e.get('msgid'), e.get('msgid_plural'))


def conv(s):
    s = cc.convert(s)
    for a, b in FIXES:
        s = s.replace(a, b)
    return s


def esc_wrap(field, value):
    return f'{field} "{value}"'


hans = {key(e): e for _, e in parse(PO + r'\zh_Hans.po') if 'msgid' in e and not e.get('obsolete')}
blocks = parse(PO + r'\zh_Hant.po')
filled = 0
out_blocks = []
for block, e in blocks:
    if 'msgid' not in e or e.get('obsolete'):
        out_blocks.append(block)
        continue
    if e['msgid'] == '' and 'msgctxt' not in e:
        # header
        b = re.sub(r'"Language-Team: .*?\\n"', r'"Language-Team: Traditional Chinese (Taiwan)\\n"', block)
        out_blocks.append(b)
        continue
    h = hans.get(key(e))
    comments = [l for l in block.split('\n') if l.startswith('#')]
    lines = list(comments)
    if 'msgctxt' in e:
        lines.append(esc_wrap('msgctxt', e['msgctxt']))
    lines.append(esc_wrap('msgid', e['msgid']))
    if 'msgid_plural' in e:
        lines.append(esc_wrap('msgid_plural', e['msgid_plural']))
        for n in range(2):
            v = conv(h.get(f'msgstr[{n}]', '')) if h else ''
            lines.append(esc_wrap(f'msgstr[{n}]', v))
        if h and h.get('msgstr[0]'):
            filled += 1
    else:
        v = conv(h['msgstr']) if h and h.get('msgstr') else ''
        if e['msgid'] in EXACT:
            v = EXACT[e['msgid']]
        if v:
            filled += 1
            lines = [l for l in lines if l != '#, fuzzy']
        lines.append(esc_wrap('msgstr', v))
    out_blocks.append('\n'.join(lines))

# Ultima VIII (engines/ultima): the game options and the Chinese settings
ULTIMA = [
    ('Traditional Chinese translation (繁體中文)', '繁體中文翻譯'),
    ('Shows the game text in Traditional Chinese (English version of the game only).', '以繁體中文顯示遊戲文字（只適用英文版遊戲）。'),
    ('Show the English after names (名稱加註英文)', '名稱加註英文'),
    ('With the Chinese translation, names are followed by their English the first time they are shown.', '人名、地名等專有名詞第一次出現時附上英文。'),
    ('High-resolution Chinese text (高解析中文字)', '高解析中文字'),
    ("Draws the Chinese text at the resolution of the window instead of the game's 320x200. Takes effect when the game is started.",
     '以視窗解析度繪製中文字，而不是遊戲的 320×200。重新啟動遊戲後生效。'),
    ('Quick action icons (快捷圖示列)', '快捷圖示列'),
    ('Icons for the backpack, keyring, saving and other actions in the bottom right corner, shown when the mouse is there.',
     '畫面右下角的背包、鑰匙圈、存檔等快捷圖示，滑鼠移過去時出現。'),
    ('Walk to use (自動走近使用)', '自動走近使用'),
    ('Double-clicking an item out of reach makes the Avatar walk to it and use it.', '雙擊太遠的物品時，聖者會自動走過去再使用。'),
    ('Chinese engravings (墓碑牌區全中文)', '墓碑牌匾全中文'),
    ('Gravestones and plaques show the translation in place of the English engraving, instead of a subtitle below it.',
     '墓碑與牌匾直接刻上中文；關閉時為英文雕刻加中文字幕。'),
    ('Use original save/load screens', '使用原版的存讀檔畫面'),
    ('Use the original save/load screens instead of the ScummVM ones', '使用遊戲原本的日記本存讀檔，而不是 ScummVM 的畫面'),
    ('Enable frame skipping', '允許略過畫格'),
    ('Allow the game to skip animation frames when running too slow.', '遊戲執行太慢時，允許略過動畫畫格。'),
    ('Enable frame limiting', '限制畫格速率'),
    ('Limits the speed of the game to prevent running too fast.', '限制遊戲速度，避免執行太快。'),
    ('Enable cheats', '開啟作弊'),
    ('Allow cheats by commands and a menu when player is clicked.', '允許使用作弊指令與作弊圖示。'),
    ('Enable high resolution', '高解析度'),
    ('Enable a higher resolution for the game', '以較高的解析度執行遊戲'),
    ('Play foot step sounds', '播放腳步聲'),
    ('Plays sound when the player moves.', '聖者移動時播放腳步聲。'),
    ('Enable jump to mouse position', '跳向滑鼠位置'),
    ('Jumping while not moving targets the mouse cursor rather than direction only.', '原地跳躍時跳向滑鼠游標的位置，而不只是方向。'),
    ('Enable font replacement', '替換遊戲字型'),
    ('Replaces game fonts with rendered fonts', '以向量字型取代遊戲的點陣字型'),
    ('Enable font anti-aliasing', '字型反鋸齒'),
    ('When font anti-aliasing is enabled, the text is smoother.', '開啟反鋸齒時，文字較平滑。'),
    # the settings page (ultima8/misc/options_widget.cpp)
    ('Dialogue text (high-resolution)', '【對話文字（高解析）】'),
    ('Font:', '字型：'),
    ('Size:', '字級：'),
    ('Letter spacing:', '字距：'),
    ('Chinese-Latin spacing:', '中英間距：'),
    ('Line spacing:', '行距：'),
    ('Outline:', '黑框：'),
    ('The font of conversations, barks and answers with the high-resolution Chinese text.', '開啟高解析中文字時，對話、台詞與選項使用的字型。'),
    ('Font size, in game pixels (the screen is 320 wide).', '字級，單位是遊戲像素（畫面寬 320）。'),
    ('Extra space between characters, in game pixels.', '字與字之間多加的間距，單位是遊戲像素。'),
    ('Extra space where Chinese characters meet Latin letters or digits, in game pixels.', '中文與英文字母、數字相接處再多加的間距，單位是遊戲像素。'),
    ('Extra space between lines, in game pixels.', '行與行之間多加的間距，單位是遊戲像素。'),
    ('Thickness of the dark outline of the text, in game pixels. 0: none.', '文字黑框的粗細，單位是遊戲像素；0 為無黑框。'),
    ('Dialogue text (pixel font)', '【對話文字（點陣，未開高解析時）】'),
    ('The font used when the high-resolution Chinese text is off.', '關閉高解析中文字時使用的字型。'),
    ('Font size, in game pixels.', '字級，單位是遊戲像素。'),
    ('Speech bubbles', '【台詞框】'),
    ('Lines per page:', '每頁行數：'),
    ('Width:', '寬度：'),
    ('Lines of Chinese text in a speech bubble before the next page.', '台詞框每頁顯示的中文行數。'),
    ('Width of a speech bubble with Chinese text, in game pixels.', '中文台詞框的寬度，單位是遊戲像素（最大 300）。'),
    ('Books and scrolls', '【書本與捲軸】'),
    ('The font of books and scrolls.', '書本與捲軸使用的字型。'),
    ('Same as the dialogue', '與對話相同'),
    ('Font size of books and scrolls, in game pixels.', '書本與捲軸的字級，單位是遊戲像素。'),
    ('Gravestones and plaques', '【墓碑與牌匾】'),
    ('The font of the Chinese engravings.', '墓碑與牌匾中文雕刻使用的字型。'),
    ('Font size of the engravings, in game pixels.', '雕刻文字的字級，單位是遊戲像素。'),
    ('Controls', '【操作】'),
    ('Click anywhere for the next page of speech', '對話時點畫面任何地方都會翻頁'),
    ('In a conversation, a click anywhere goes to the next page, as in Ultima VII. Off: click the text.',
     '對話時點畫面任何地方都會翻到下一頁，和 Ultima VII 相同。關閉：要點在文字上（原版）。'),
    ('Escape closes the frontmost window first', 'Esc 先關閉最上層的視窗'),
    ('Escape closes the frontmost container or inventory before it opens the menu.',
     'Esc 先關閉最上層的箱子、背包或屬性頁，全部關完才打開選單。'),
    ('Show the quick action icons only under the mouse', '快捷圖示列只在滑鼠移過去時出現'),
    ('Off: the quick action icons are always shown.', '關閉：快捷圖示列一直顯示。'),
    ('Land targeted jumps on the middle of the target', '跳向滑鼠位置時，落在目標中央'),
    ('With jump to mouse position, the Avatar lands with his whole footing on the stone or platform under the mouse, and shakes his head if there is no room. Off: the original landing.',
     '開啟「跳向滑鼠位置」時，聖者會整個人落在滑鼠所指的石頭或平台上；放不下就搖頭。關閉：原版的落點。'),
    ("Show the damage of the Avatar's blows", '顯示聖者攻擊的傷害數字'),
    ('The damage the Avatar does floats up from the one he hit, or Blocked when the armour took it all.',
     '聖者打中敵人時，敵人頭上會浮出傷害數字；被盔甲完全擋下時顯示「格擋」。'),
    ('Defaults', '恢復預設'),
    ('Set the settings above (not the checkboxes) back to their defaults.', '把上面的字型與數值設定恢復成預設值（不含最上方的勾選框）。'),
    ('Default (%S)', '預設（%S）'),
]


def po_escape(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


have = {key(e)[1]: i for i, (_, e) in enumerate(blocks) if 'msgid' in e}
extra = []
for en, zh in ULTIMA:
    msgid = po_escape(en)
    done = False
    for i, b in enumerate(out_blocks):
        if re.search(r'^msgid "' + re.escape(msgid) + r'"$', b, re.M) and 'msgctxt' not in b:
            out_blocks[i] = re.sub(r'^msgstr ".*"$', lambda m: 'msgstr "' + po_escape(zh) + '"', b, flags=re.M)
            done = True
    if not done:
        extra.append('#: engines/ultima\nmsgid "%s"\nmsgstr "%s"' % (msgid, po_escape(zh)))
out_blocks += extra
print('ultima strings', len(ULTIMA), 'appended', len(extra))

open(PO + r'\zh_Hant.po', 'w', encoding='utf-8', newline='\n').write('\n\n'.join(out_blocks) + '\n')
print('filled', filled, 'of', sum(1 for _, e in blocks if 'msgid' in e and not e.get('obsolete')))
