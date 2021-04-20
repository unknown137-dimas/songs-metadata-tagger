import os,re,music_tag,pandas,json
from pymongo import MongoClient


conn=MongoClient('mongodb://127.0.0.1:27000')
db=conn.main
coll=db.rawSpotifyDB

## add filter block to select audio file w/ empty metadata only
## add here

def filename():
    this_dir=os.getcwd()
    os.chdir('/users/unknown-x/music')
    fn=[x for x in os.listdir() if re.search('.m4a',x)]
    art=[str(music_tag.load_file(a)['artist']) for a in fn]

    df=pandas.DataFrame({'filename':fn,'artist':art})
    df.to_excel(this_dir+'/test.xlsx')

def DBExtract():
    res=list(coll.aggregate([
            {'$unwind':'$artists'},
            {'$unwind':'$tracks'},
            {'$unwind':'$tracks.items'},
            {'$project':{
                '_id':0,
                'id':1,
                'name':1,
                'release_date':1,
                'artist':'$artists.name',
                'title':'$tracks.items.name',
                'track_number':'$tracks.items.track_number',
                'total_tracks':1,
                'disc_number':'$tracks.items.disc_number'}}
            ]))
    
    df=pandas.DataFrame(res)
    df.to_excel('db.xlsx')
    
    # with open('output.json','w') as o:
    #     for r in res:
    #         if input[0].lower()==str(r['title']).lower():
    #             o.write(json.dumps(r,indent=3))

input=('you never know','41MozSoPIsD1dJM0CLPjZF')
DBExtract()
