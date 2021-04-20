import os,re,music_tag,pandas,spotipy,json,ast
from requests.api import get
from pymongo import MongoClient
from spotipy.oauth2 import SpotifyClientCredentials

this_dir=os.getcwd()

conn=MongoClient('mongodb://127.0.0.1:27000')
db=conn.main
coll=db.rawSpotifyDB

id='2f44d222e8bf4795a8d3a7d394449760'
secret='0d2048a09a67474e85646a729508c787'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=id, client_secret=secret))

# dir=os.getcwd()
art=['Rocket Punch', 'LOONA', 'Red Velvet', 'Oh My Girl', 'IZ*ONE', 'Weki Meki', 'Lovelyz', 
'TWICE', 'IU', 'Everglow', 'CLC', 'DreamCatcher', 'Cignature', 'EXID', 
'GFRIEND', 'Fromis_9', 'WJSN', "Girls' Generation", 'BlackPink', 'Secret', 'DreamNote', 
'NATURE', 'APRIL', 'Apink', 'K/DA', 'ITZY', 'Cherry Bullet', 'TRI.BE', 
'AleXa', 'AESPA', 'AOA', 'Momoland', 'Weeekly', '(G)I-DLE', 'Yukika','Eunha']


def get_artist_name():
    os.chdir('/Users/unknown-x/music')
    file=[f for f in os.listdir() if re.search('.m4a',f)]
    for a in file:
        x=str(music_tag.load_file(a)['artist'])
        if x not in art:
            art.append(x)
    print(art)

def get_artist_name_v2():
    os.chdir('/Users/unknown-x/music')
    file=[f for f in os.listdir() if re.search('.m4a',f)]
    tmp=[]
    for f in file:
        s=music_tag.load_file(f)
        if str(s['album'])=='' and str(s['artist'])=='':
            tmp.append(f)
    df=pandas.DataFrame({'filename':tmp,'artist':'','title':'','artist_id':''})
    df.to_excel(this_dir+'/filename.xlsx')

def get_artist_id():
    tmp=[]
    for x in art:
        res=sp.search(q=x,type='artist',limit=10)
        for r in res['artists']['items']:
            tmp.append({'id':r['id'],'artist':r['name']})
    df=pandas.DataFrame(tmp)
    df.to_excel(this_dir+'/spotipy-res.xlsx')

def get_artist_id_v2():
    df=pandas.read_excel(this_dir+'/filename.xlsx')
    artist=df['artist']
    tmp=[]
    for x in artist:
        res=sp.search(q=x,type='artist',limit=10)
        for r in res['artists']['items']:
            tmp.append({'id':r['id'],'artist':r['name']})
    df=pandas.DataFrame(tmp)
    df.to_excel(this_dir+'/spotipy-res.xlsx')

def insertToDB():
    df=pandas.read_excel(this_dir+'/spotipy-res.xlsx')
    id=list(df['id'])
    for i in id:
        o=0
        x=[]
        while True:
            tmp=sp.artist_albums(i,limit=50,offset=o)
            for t in tmp['items']:
                x.append({'id':t['id']})
            if len(tmp['items'])==50:
                o+=50
            else:
                break
        for r in x:
            res=sp.album(r['id'])
            for a in res['artists']:
                if a['id']==i:
                    coll.insert_one(res)

def matchFile():
    df=pandas.read_excel(this_dir+'/filename.xlsx')
    file=pandas.DataFrame(df,columns={'filename','artist','title','artist_id'}).to_dict('records')
    out=[]
    for f in file:
        res=list(coll.aggregate([
                {'$unwind':'$artists'},
                {'$unwind':'$tracks'},
                {'$unwind':'$tracks.items'},
                {'$match':{'artists.id':f['artist_id']}},
                {'$project':{
                    '_id':0,
                    'album id':'$album_id',
                    'album name':'$name',
                    'release date':'$release_date',
                    'artist id':'$artists.id',
                    'artist':'$artists.name',
                    'title':'$tracks.items.name',
                    'track number':'$tracks.items.track_number',
                    'total tracks':'$total_tracks',
                    'disc number':'$tracks.items.disc_number',
                    'images':1}}
                ]))
        tmp=[]
        for r in res:
            if re.search(str(f['title']).lower(),str(r['title']).lower()):
                tmp.append(r)
        seen=set()
        new_tmp=[]
        for d in tmp:
            dx={'album name':d['album name'],'title':d['title'],'track number':d['track number']}
            t=tuple(dx.items())
            if t not in seen:
                seen.add(t)
                new_tmp.append(d)
        if len(new_tmp)!=0:
            for t in new_tmp:
                s={'filename':f['filename']}
                s.update(t)
                out.append(s)
        else:
            out.append({'filename':f['filename']})
    pandas.DataFrame(out).to_excel(this_dir+'/output.xlsx')
    # with open('output.json','w') as oj:
    #         oj.write(json.dumps(out,indent=3))

def meta():
    df=pandas.read_excel(this_dir+'/output.xlsx')
    images=df['images']
    files=pandas.DataFrame(df,columns={'filename','images','album name',
    'release date','artist','title','track number','total tracks','disc number'}).to_dict('records')
    url=set()
    print('Downloading Album Artworks...')
    for image in images:
        for i in ast.literal_eval(image):
            if i['height']==640:
                url.add(str(i['url']))
    for u in url:
        name=u.split('/')[-1]+'.jpeg'
        if name not in os.listdir(this_dir+'/images_tmp'):
            r = get(u, allow_redirects=True)
            open(this_dir+'/images_tmp/'+name, 'wb').write(r.content)

    print('Adding Metadata to the File...')
    os.chdir('/Users/unknown-x/music')
    for f in files:
        for i in ast.literal_eval(f['images']):
            if i['height']==640:
                name=this_dir+'/images_tmp/'+str(i['url']).split('/')[-1]+'.jpeg'
        print(f['filename'])
        a=music_tag.load_file(f['filename'])
        a['artist']=f['artist']
        a['album']=f['album name']
        a['year']=str(f['release date']).split('-')[0]
        a['tracktitle']=f['title']
        a['totaltracks']=f['total tracks']
        a['tracknumber']=f['track number']
        a['discnumber']=f['disc number']
        with open(name,'rb') as artwork:
            a['artwork']=artwork.read()
        a['artwork'].first.thumbnail([64, 64])
        a.save()

get_artist_name_v2()