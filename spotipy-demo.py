import spotipy,re,json,pandas,os,music_tag
from spotipy.oauth2 import SpotifyClientCredentials

id='2f44d222e8bf4795a8d3a7d394449760'
secret='0d2048a09a67474e85646a729508c787'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=id, client_secret=secret))

input=('iz*one','pretty')

art=['Rocket Punch', 'LOONA', 'Red Velvet', 'Oh My Girl', 'IZ*ONE', 'Weki Meki', 'Lovelyz', 
'TWICE', 'IU', 'Everglow', 'CLC', 'DreamCatcher', 'Cignature', 'EXID', 
'GFRIEND', 'Fromis_9', 'WJSN', "Girls' Generation", 'BlackPink', 'Secret', 'DreamNote', 
'NATURE', 'APRIL', 'Apink', 'K/DA', 'ITZY', 'Cherry Bullet', 'TRI.BE', 
'AleXa', 'AESPA', 'AOA', 'Momoland', 'Weeekly', '(G)I-DLE', 'Yukika']

def get_artist_name():
    os.chdir('/Users/unknown-x/music')
    file=[f for f in os.listdir() if re.search('.m4a',f)]
    for a in file:
        x=str(music_tag.load_file(a)['artist'])
        if x not in art:
            art.append(x)
    print(art)

def get_artist_id():
    with open('log.txt','w') as l:
        tmp=[]
        for x in art:
            s='FAILED'
            res=sp.search(q=x,type='artist',limit=50)
            r=res['artists']['items'][0]
            tmp.append({'id':r['id'],'artist':r['name']})
            s='PASS'
            l.write(x+' -> '+s+'\n')

    df=pandas.DataFrame(tmp)
    print(df)
    # df.to_excel('spotipy-res.xlsx')

def query(n,i):
    # res=sp.search('TRI.BE',type='artist',limit=50)
    o=0
    res=[]
    while True:
        tmp=sp.artist_albums(i,limit=50,offset=o)
        for r in tmp['items']:
            res.append({'id':r['id'],'name':r['name']})
        # res.append(tmp)
        if len(tmp['items'])==50:
            o+=50
        else:
            break
    
    # res=sp.album(n)
    # sp.album_tracks
    # res=sp.album(n)
    # res=sp.album_tracks(n)
    with open('spotipy-res.json','w') as sr:
        out=[]
        #     tmp={'name':r['name'],'id':r['id'],'genres':r['genres']}
            # for a in r['artists']:
            #     if a['id']==i:
        sr.write(json.dumps(res,indent=3))
        sr.write(str(len(res)))

al_id='5M9KMJ64uiEh8LjnnXdKjG'
twice='7n2Ycct7Beij7Dj7meI4X0'
tribe='6BgYuNomEs12UIrnxhWE9a'
query(n=al_id,i=twice)
# get_artist_id()
