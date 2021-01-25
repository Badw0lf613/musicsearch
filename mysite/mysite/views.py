from django.shortcuts import render
import re
import py2neo
import json
# from mysite import match
from . import match

# Create your views here.


def template(category, string):
    ans = dict()
    if category == 'singer':
        matchObj = re.match(r'和(.*)合作过的歌手',string, re.M|re.I)
        print(matchObj)
        if matchObj:
            ans['singer'] = matchObj.group(1)
            ans['type'] = '000'
            ans['relation'] = '合作'
        else:
            matchObj = re.match(r'(.*)主创是谁', string, re.M | re.I)
            ans['album'] = matchObj.group(1)
            ans['type'] = '001'
            ans['relation'] = '主创是'

    elif category == 'song':
        matchObj = re.match(r'(.*)唱过什么歌', string, re.M | re.I)
        if matchObj:
            ans['singer'] = matchObj.group(1)
            ans['type'] = '010'
            ans['relation'] = '演唱'
        else:
            matchObj = re.match(r'我想看(.*)的歌词', string, re.M | re.I)
            ans['song'] = matchObj.group(1)
            ans['type'] = '011'
            ans['relation'] = 'lyric'

    elif category == 'album':
        matchObj = re.match(r'(.*)收录于哪个专辑', string, re.M | re.I)
        if matchObj:
            ans['song'] = matchObj.group(1)
            ans['type'] = '100'
            ans['relation'] = '收录于'
        else:
            matchObj = re.match(r'(.*)的相似专辑', string, re.M | re.I)
            ans['album'] = matchObj.group(1)
            ans['type'] = '101'
            ans['relation'] = '相似'

    elif category == 'list':
        matchObj = re.match(r'(.*)在哪个歌单里有', string, re.M | re.I)
        if matchObj:
            ans['song'] = matchObj.group(1)
            ans['type'] = '110'
            ans['relation'] = '属于'

        else:
            matchObj = re.match(r'(.*)风格的歌单有哪些', string, re.M | re.I)
            ans['label'] = matchObj.group(1)
            ans['type'] = '111'
            ans['relation'] = ''
    return ans


def test(request):
    if request.method == "GET":
        return render(request, "test.html")
    else:
        shuru = request.POST.get("shuru")
        category = request.POST.get("select")
        print(category)
        # --------------------匹配模式----------------------------
        # 歌手： 000.和xxx合作过的歌手  001. xxx主创是谁
        # 歌曲： 010.xxx唱过什么歌  011.我想看xxx的歌词
        # 专辑： 100.xxx收录于哪个专辑 101.xxx的相似专辑
        # 歌单: 110.xxx在哪个歌单里有  111. xx风格的歌单有哪些

        keys = template(category, shuru)

        root, answer = match.require(keys['type'], list(keys.values())[0])
        print(answer)
        #搜索
        length = len(answer)
        print('!!!', length)
        transit = []
        for id, item in enumerate(answer):
            transit.append(item)
        print(transit)

        #搜索结果
        # answer = 'test answer'
        # return render(request, "index.html")
        return render(request, "test.html", {"nodes": json.dumps(transit, ensure_ascii=False),
                                             "length": json.dumps(length), "root": json.dumps(root),
                                             "relation": json.dumps(keys['relation'])})