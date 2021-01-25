from py2neo import Graph, Node, Relationship, NodeMatcher, Subgraph
import json
import pandas
graph = Graph('http://localhost:7474', username='neo4j', password='cyh991227')
matcher = NodeMatcher(graph)

#匹配
def require(num,input):
    if num == '000':
        artistname=input
        matchstr='match (x:artist{name:\''+artistname+'\'})-[r:`合作`]-(y:artist) return y'
        p = graph.run(matchstr).data()
        listout = []
        for p1 in p:
            dictout=dict(name=p1['y']['name'], introduction=p1['y']['introduction'])
            if dictout not in listout:
                listout.append(dictout)
        node = matcher.match('artist', name = artistname).first()
        root = dict(name = node['name'], introduction = node['introduction'])
        print(root)
        print(listout)

    if num == '001':
        albumname=input
        matchstr='match (x:artist)-[a:`演唱`]-(y:music)-[b:`属于专辑`]-(z:album{name:\''+albumname+'\'}) return x'
        p = graph.run(matchstr).data()
        listout = []
        for p1 in p:
            # print(p1['y']['introduction'])
            dictout = dict(name=p1['x']['name'], introduction=p1['x']['introduction'])
            listout.append(dictout)
            break
        node = matcher.match('album', name=albumname).first()
        root = dict(name=node['name'])
        print(root)
        print(listout)

    if num == '010':
        artistname=input
        matchstr='match (x:artist{name:\''+artistname+'\'})-[a:`演唱`]-(y:music) return y'
        p = graph.run(matchstr).data()
        listout = []
        for p1 in p:
            dictout = dict(name=p1['y']['name'], lyric=p1['y']['lyric'])
            listout.append(dictout)
        node = matcher.match('artist', name=artistname).first()
        root = dict(name=node['name'], introduction=node['introduction'])
        print(root)
        print(listout)

    if num == '011':
        musicname = input
        matchstr = 'match (x:music{name:\'' + musicname + '\'}) return x'
        p = graph.run(matchstr).data()
        listout = []
        for p1 in p:
            dictout = dict(name=p1['x']['name'], lyric=p1['x']['lyric'])
            listout.append(dictout)
        print(listout)

    if num == '100':
        musicname=input
        matchstr='match (x:music{name:\''+musicname+'\'})-[a:`属于专辑`]-(y:album) return y'
        p = graph.run(matchstr).data()
        listout = []
        for p1 in p:
            dictout = dict(name=p1['y']['name'])
            listout.append(dictout)
        node = matcher.match('music', name=musicname).first()
        root = dict(name=node['name'], lyric=node['lyric'])
        print(root)
        print(listout)

    if num == '101':
        albumname = input
        #返回目标专辑
        matchstr = 'match (p:album)-[:`属于专辑`]-(z:music)-[:`相似`]-(x:music)-[a:`属于专辑`]-(y:album{name:\''+albumname+'\'}) return p'
        p = graph.run(matchstr).data()
        listout = []
        for p1 in p:
            dictout = dict(name=p1['p']['name'])
            if dictout in listout:
                continue
            listout.append(dictout)
        #返回原专辑中的音乐
        matchstr = 'match (p:album)-[:`属于专辑`]-(z:music)-[:`相似`]-(x:music)-[a:`属于专辑`]-(y:album{name:\'' + albumname + '\'}) return z'
        p = graph.run(matchstr).data()
        listout = []
        for p1 in p:
            dictout = dict(name=p1['z']['name'])
            if dictout in listout:
                continue
            listout.append(dictout)
        # 返回目标专辑中的音乐
        matchstr = 'match (p:album)-[:`属于专辑`]-(z:music)-[:`相似`]-(x:music)-[a:`属于专辑`]-(y:album{name:\'' + albumname + '\'}) return x'
        p = graph.run(matchstr).data()
        listout = []
        for p1 in p:
            dictout = dict(name=p1['p']['name'])
            if dictout in listout:
                continue
            listout.append(dictout)
        node = matcher.match('album', name=albumname).first()
        root = dict(name=node['name'])
        print(root)
        print(listout)

    if num == '110':
        musicname = input
        matchstr = 'match (x:music{name:\''+musicname+'\'})-[:`属于歌单`]-(y:playlist) return y'
        p = graph.run(matchstr).data()
        listout = []
        for p1 in p:
            dictout = dict(name=p1['y']['name'])
            if dictout in listout:
                continue
            listout.append(dictout)
        node = matcher.match('music', name=musicname).first()
        root = dict(name=node['name'], lyric=node['lyric'])
        print(root)
        print(listout)

    if num == '111':
        labelname = input
        matchstr = 'match (x:playlist{`' +labelname+ '`:\'1\'}) return x'
        p = graph.run(matchstr).data()
        listout = []
        for p1 in p:
            dictout = dict(name=p1['x']['name'])
            if dictout in listout:
                continue
            listout.append(dictout)
        node = matcher.match('artist', name=artistname).first()
        print(listout)
        
require('000', '林俊杰')

#建立节点
with open("163music_data_processed.json", "r", encoding="utf-16") as f:
    for data in f.readlines():
        dict = json.loads(data)
        if count%100 == 0:
            print(count)
        count = count+1

        node_music = Node('music',id = dict['_id'], name = dict['name'])
        graph.create(node_music)


        for artid, artname in zip(dict['artist_ids'],dict['artist_names']):
            if not(matcher.match('artist', id=artid).first()):
                node_artist = Node('artist', id = artid , name = artname)
                graph.create(node_artist)


        if not(matcher.match('album', id=dict['album_id']).first()):
            node_album = Node('album', id=dict['album_id'], name=dict['album_name'])
            graph.create(node_album)

        for playid, playname in zip(dict['playlist_ids'],dict['playlist_names']):
            if not(matcher.match('playlist', id=playid).first()):
                node_playlist = Node('playlist', id = playid , name = playname)
                graph.create(node_playlist)


#创建关系
with open("163music_data_processed.json", "r", encoding="utf-16") as f:
    for data in f.readlines():
        if count % 100 == 0:
            print(count)
        count = count + 1
        dict = json.loads(data)
        node_music = matcher.match('music', id=dict['_id']).first()
        node_artist_list=[]

        for artid, artname in zip(dict['artist_ids'],dict['artist_names']):
            node_artist = matcher.match('artist', id=artid).first()
            relationship_sing = Relationship(node_artist, '演唱', node_music)
            node_artist_list.append(node_artist)
            graph.create(relationship_sing)

        length=len(node_artist_list)
        for j in range(length):
            if j != 0:
                relationship_coo = Relationship(node_artist_list[0], '合作', node_artist_list[j])
                relationship_coo['歌曲'] = dict['_id']
                graph.create(relationship_coo)

        node_album = matcher.match('album', id=dict['album_id']).first()
        relationship_album = Relationship(node_music, '属于专辑', node_album)
        graph.create(relationship_album)

        for playid in dict['playlist_ids']:
            node_playlist = matcher.match('playlist', id=playid).first()
            relationship_playlist = Relationship(node_music, '属于歌单', node_playlist)
            graph.create(relationship_playlist)

        for smid in dict['similar_musics_ids']:
            node_smm = matcher.match('music', id=smid).first()
            if node_smm:
                relationship_smm = Relationship(node_music, '相似', node_smm)
            graph.create(relationship_smm)


#添加歌单属性
labellist=['华语', '流行', '民谣', '放松', '欧美', '翻唱', '孤独', '安静', '清晨', '午休', '夜晚', '治愈', '影视原声', '伤感', '榜单', '世界音乐', '怀旧', '校园', '学习', '旅行', '90后', '日语', '散步', '吉他', '粤语', '思念', '经典', '说唱', '清新', '运动', '浪漫', '地铁', '感动', '古风', '快乐', '网络歌曲', '电子', '游戏', '轻音乐', '00后', '兴奋', 'KTV', 'R&amp;B/Soul', '综艺', '工作', '下午茶', '另类/独立', '摇滚', '雷鬼', '钢琴', 'New Age', 'ACG', '民族', '小语种', '韩语', '器乐', '驾车', '酒吧', '70后', '乡村', '舞曲', '古典', '爵士', '80后', '性感', '后摇', '蓝调', '朋克', '金属', '儿童', '英伦', 'Bossa Nova']
import csv
with open('playlist_data.csv','r',encoding='gbk') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]
for row1 in rows:
    playlistid = row1[0]
    node = matcher.match('playlist', id = playlistid).first()
    if row1[1] == '':
        continue
    feature = row1[1].split(',')
    if node:
        for f in feature:
            #print(type(f))
            node[f] = '1'
            graph.push(node)
    print(count)
    count=count+1

#添加歌手简介
# import csv
# with open('artist_data.csv','r',encoding='gbk') as csvfile:
#     reader = csv.reader(csvfile)
#     rows = [row for row in reader]
# for row1 in rows:
#     artistid = row1[0]
#     node = matcher.match('artist', id=artistid).first()
#     if node:
#         node['introduction'] = row1[1]
#         graph.push(node)

# inputstr='华语'
# nodes = matcher.match('playlist',='1')
# #nodes = list(nodes)
# print(nodes)
# for node in nodes:
#     print(node)


# match_str = "MATCH (n:playlist{华语 : '1'}) RETURN n"
# p1 = graph.run(match_str).data()
# p1 = list(p1)
# for p in p1:
#     print(p['n']['name'])

#添加歌词
# import csv
# with open('play_data.csv','r',encoding='utf-8') as csvfile:
#     reader = csv.reader(csvfile)
#     rows = [row for row in reader]
# for row1 in rows:
#     musicid = row1[0]
#     node = matcher.match('music', id=musicid).first()
#     if node:
#         node['lyric'] = row1[1]
#         graph.push(node)