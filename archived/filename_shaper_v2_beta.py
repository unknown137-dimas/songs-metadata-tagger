import spotipy,os,re,json,music_tag
from spotipy.oauth2 import SpotifyClientCredentials

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
    res=sp.search(q=a,type='artist',limit=20)
    for artist in res['artists']['items']:
        if 'k-pop' in artist['genres'] and re.match('^'+a+'$',artist['name'].lower()):
            tmp.append(artist['id'])
    return tmp

def matching_name(ar,tr):
    dir=os.getcwd()
    # c=0
    q='MV'
    os.chdir('/users/unknown-x/music')
    with open(dir+'/with-'+q+'.txt','w') as n:
        # os.chdir('/Users/unknown-x/Music')
        for f in os.listdir():
            if not re.match("Music",f) and not re.match(".DS_Store",f):
                # m=music_tag.load_file(f)
                if re.search(ar.lower(),f.lower()) and not re.search('mashup',f.lower()):
                    if re.search(q,f) and f!=None:
                        # if f!=None:
                        f_tmp=f.replace('_',' ')
                        if re.findall(tr['name'].lower(),f_tmp.lower()) and int(tr['track_number'])==1:
                            res=[f_tmp,tr['name'],tr['track_number'],tr['id']]
                            print(res)
                            
                    
                    # a.save()
# artists_list=gen_artist_list()
# data=[get_artist_id(a) for a in artists_list]
data=get_artist_id('twice')
# if __name__ ==" __main__":

with open('out-v2.txt','w') as o:
    for d in data:
    # def info_parser(d):
    #     out=[]
        for ar_al in sp.artist_albums(d,country='ID')['items']:
            al_id=ar_al['id']
            al_rel=ar_al['release_date'].split('-')[0]
            al_name=ar_al['name']
            al_ty=ar_al['type']
            ar_name=ar_al['artists'][0]['name']
            if int(ar_al['total_tracks'])>1:
                for al_tr in sp.album_tracks(al_id,limit=15)['items']:
                    # o.write(str(matching_name(al_tr['name']))+'\n')
                    # o.write(str(matching_name(q=ar_name,t=al_tr['name'])))
                    matching_name(ar=ar_name,tr=al_tr)
                    # o.write(str([al_id,al_name,al_tr['id'],al_tr['track_number'],al_tr['name']])+'\n')
                        # o.write(str([ar_name,al_name,al_rel,t['track_number'],t['name']])+'\n')
    # return out
# for d in data:
#     for i in info_parser(d):
#         print(i)
        # print(x)
        # x=str({'artist':sp.artist(d)['name'],'albums':al})
        # o.write(json.dumps(x,indent=3))

    # print(d)
