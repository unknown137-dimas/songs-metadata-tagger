from pymongo import MongoClient
import json,pandas,re


conn=MongoClient(host='127.0.0.1', port=27000)
db=conn.main
coll=db.rawSpotifyDB
old_coll=db.raw

def matchFile():
    # df=pandas.read_excel('test.xlsx')
    # art_id=list(df['artist id'])
    # titles=list(df['title'])
    input=('3g34PW5oNmDBxMVUTzx2XK','now, we')
    res=list(coll.aggregate([
            {'$unwind':'$artists'},
            {'$unwind':'$tracks'},
            {'$unwind':'$tracks.items'},
            {'$unwind':'$images'},
            {'$match':{'images.height':640}},
            {'$match':{'artists.id':input[0]}},
            {'$project':{
                '_id':0,
                'id':1,
                'name':1,
                'release_date':1,
                'artist_id':'$artists.id',
                'artist':'$artists.name',
                'title':'$tracks.items.name',
                'track_number':'$tracks.items.track_number',
                'total_tracks':1,
                'disc_number':'$tracks.items.disc_number',
                'images':'$images.url'}}
            ]))
    with open('output.json','w') as o:
    # tmp=[]
    # with open('log.txt','w') as l:
    #     for i in range(len(art_id)):
    #         # input=(art_id[i],titles[i])
    #         s='FAILED'
        for r in res:
            if re.search(str(input[1]).lower(),str(r['title']).lower()):
                o.write(json.dumps(r,indent=3))
    #                 tmp.append(r)
    #                 s='PASS'
    #         l.write(str(titles[i])+' -> '+s+'\n')
    # out=pandas.DataFrame(tmp)
    # out.to_excel(this_dir+'/output.xlsx')

def mongo_demo():
    res=coll.find_one({},{'_id':0})
    with open('mong.json','w') as m:
        # for r in list(res):
        m.write(json.dumps(res,indent=3))

def db_dup_remover():
    res=list(old_coll.find({},{'_id':0}))
    seen=set()
    tmp=[]
    for r in res:
        if r['album_id'] not in seen:
            seen.add(r['album_id'])
            tmp.append(r)
    for t in tmp:
        coll.insert_one(t)

matchFile()