# coding:utf-8
# from py2neo import Graph, Node, Relationship
from py2neo import *

# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://localhost:7474', username='neo4j', password='Aptx4869')
matcher = NodeMatcher(graph)
# 建立节点

def require(num,input):
    print(num, input)
    # if num == '000':
    #     artistname=input
    #     matchstr='match (x:artist{name:\''+artistname+'\'})-[r:`合作`]-(y:artist) return y'
    #     p = graph.run(matchstr).data()
    #     listout = []
    #     for p1 in p:
    #         #print(p1['y']['introduction'])
    #         dictout=dict(name=p1['y']['name'], introduction=p1['y']['introduction'])
    #         if dictout not in listout:
    #             listout.append(dictout)
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
        root = dictout
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
        matchstr = 'match (p:album)-[:`属于专辑`]-(z:music)-[:`相似`]-(x:music)-[a:`属于专辑`]-(y:album{name:\''+albumname+'\'}) return p'
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
        root = dict()
        print(listout)

    return root,listout

