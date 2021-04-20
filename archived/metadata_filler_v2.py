from pymongo import MongoClient
import os,re,music_tag,csv

conn=MongoClient('mongodb://127.0.0.1:27000')
db=conn.main
coll=db.testv2
dir=os.getcwd()

def gen_artist_list():
    tmp=[]
    for f in os.listdir("/Users/unknown-x/Movies/KPOP"):
            if not re.search('\.',f) and not re.search('Mashup',f) and not re.search('Raon Lee',f) and not re.search('YuA Violin',f):
                tmp.append(f)
    return tmp

def stage_1():
    # find mv / music video in local folder
    ret=[]
    filter=['MV','Music Video']
    lst=gen_artist_list()
    os.chdir('/users/unknown-x/music')
    for l in lst:
        tmp=[]
        for f in os.listdir():
            if not re.match("Music",f) and not re.match(".DS_Store",f):
                f_tmp=f.replace('_',' ')
                for q in filter:
                    if re.search(q.lower(),f_tmp.lower()) and not re.search('mashup',f.lower()):
                        m=music_tag.load_file(f)
                        if re.match(l.lower(),str(m['artist']).lower()):
                            tmp.append(f)
        ret.append([l,tmp])
    return ret

def match_name_stage_1(l_tr,tr):
    # if re.search(a.lower(),l_tr.lower()):
    f_tmp=l_tr.replace('_',' ')
    if re.search(tr.lower(),f_tmp.lower()):
        return [l_tr,tr]
    # if re.findall(tr['tr_name'].lower(),f_tmp.lower()):
        # ret=[l_tr,al['al_name'],al['release_date'],tr['tr_name'],tr['tr_num'],al['total_tracks']]
        # return match_name_stage_2(al['al_id'])
            # if ret!=None:

def match_name_stage_2(id):
    res=coll.aggregate([
    {'$unwind':'$albums'},
    {'$unwind':'$albums.tracks'},
    {'$match':{'albums.al_id':id}},
    {'$project':{'_id':0,'albums.al_id':1,'albums.al_name':1,'albums.tracks.tr_name':1}}
    ])
    # for r in list(res):
    #     e=[r['albums']['al_name'],r['albums']['tracks']['tr_name']]
    return res


# name=gen_artist_list()
local=stage_1()


    # for n in name:
n='TWICE'
res=list(coll.aggregate([
    {'$unwind':'$albums'},
    {'$unwind':'$albums.tracks'},
    {'$match':{'artist':n}},
    {'$match':{'albums.tracks.tr_num':1}},
    {'$project':{'_id':0,'albums.al_id':1,'albums.tracks.tr_name':1}}
]))
with open(dir+'/'+n+'.txt','w',encoding='utf_8_sig') as m:
    for r in res:
        q=r['albums']['tracks']['tr_name']
        for lcl in local:
            if re.findall(lcl[0],n):
                for l in lcl[1]:
                    x=match_name_stage_1(l_tr=l,tr=q)
                    if x!=None:
                        m.write(str(x)+'\n')
                # m.write(l+'\n')
                
                    # if re.findall(q,l):
                        # m.write(str([q,l])+'\n')

#                 for i in l:
#                     x=match_name_stage_1(a=a,l_tr=i,tr=tr,al=al)
#                         for o in x:
#                             m.write(str(o)+'\n')
                        # m=music_tag.load_file(x[0])
                        # m['album']=x[1]
                        # m['year']=x[2]
                        # m['tracknumber']=x[4]
                        # m['totaltracks']=x[5]
                        # m.write(str(x)+'\n')
                        # write=csv.writer(m,dialect='excel',delimiter=';')
                        # write.writerow(str(x))
