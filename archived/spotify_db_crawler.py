from pymongo import MongoClient
import spotipy,re,os,json
from spotipy.oauth2 import SpotifyClientCredentials


conn=MongoClient(host='127.0.0.1', port=27000)
db=conn.main
coll=db.testv2

id='2f44d222e8bf4795a8d3a7d394449760'
secret='0d2048a09a67474e85646a729508c787'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=id, client_secret=secret))

def gen_artist_list():
    tmp=[]
    for f in os.listdir("/Users/unknown-x/Movies/KPOP"):
            if not re.search('\.',f) and not re.search('Mashup',f) and not re.search('Raon Lee',f) and not re.search('YuA Violin',f):
            # if not re.search('\.',f):
                tmp.append(f.lower())

    return tmp

def get_artist_id(a):
    tmp=[]
    res=sp.search(q=a,type='artist',limit=50)
    for artist in res['artists']['items']:
        if re.search('k-pop',str(artist['genres'])) and re.match('^'+a+'$',artist['name'].lower()):
            tmp.append(artist['id'])     
    return tmp

data=[''.join(get_artist_id(x)) for x in gen_artist_list()]
print(data)

# for d in data:
#     if len(d)>0:
#         al_tmp=[]
#         art=[]
#         for ar_al in sp.artist_albums(d)['items']:
#             art.append(ar_al['artists'][0]['name'])
#             tr_tmp=[]
#             for al_tr in sp.album_tracks(ar_al['id'],limit=50)['items']:
#                 tr_tmp.append({'tr_id':al_tr['id'],
#                                 'tr_name':al_tr['name'],
#                                 'tr_num':al_tr['track_number'],
#                                 'disc_num':al_tr['disc_number']})
                
#             al_tmp.append({'al_id':ar_al['id'],
#                             'al_name':ar_al['name'],
#                             'release_date':ar_al['release_date'].split('-')[0],
#                             'total_tracks':ar_al['total_tracks'],
#                             'tracks':tr_tmp})
        
#         posts={'artist':art[0],'albums':al_tmp}
#         coll.insert_one(posts)
