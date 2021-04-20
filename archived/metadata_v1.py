import music_tag, os, re
def add_meta(file,art):
    f=music_tag.load_file(file)
    f['artist']=art
    f.save()

artists=[]
def get_artist_name():
    for f in os.listdir("/Users/unknown-x/Movies/KPOP"):
        if not re.search('\.',f) and not re.search('Mashup',f) and not re.search('Raon Lee',f)and not re.search('YuA Violin',f):
        # if not re.search('\.',f):
            artists.append(f)
    # sp=['Mashup','Raon Lee', 'YuA Violin']
    # for s in sp:
    #     s=str(s)
    #     ind=artists.index(s)
    #     artists.insert(sp.index(s),artists[ind])
    #     artists.pop(ind+1)
    # for a in artists:
    #     print(a.lower())

tmp=[]
def match_artist():
    # with open('test-v2.txt','w') as ts:
        for f in os.listdir('/Users/unknown-x/Music'):
            # fn=os.path.basename(f)
            if not re.match("Music",f) and not re.match(".DS_Store",f):
                # ts.writelines(str(fn)+'\n')
                fn_tmp=f.replace('_',' ')
                for a in artists:
                    a_tmp=a.replace('_',' ')
                    if re.search('mashup',fn_tmp.lower()):
                        tmp_art={'filename':f,'artist':'Mashup'}
                        add_meta(tmp_art.get('filename'),tmp_art.get('artist'))
                        # ts.writelines(str(tmp_art)+'\n')
                        break
                    elif re.search('raon lee',fn_tmp.lower()):
                        tmp_art={'filename':f,'artist':'Raon Lee'}
                        add_meta(tmp_art.get('filename'),tmp_art.get('artist'))
                        # ts.writelines(str(tmp_art)+'\n')
                        break
                    elif re.search('yua violin',fn_tmp.lower()):
                        tmp_art={'filename':f,'artist':'YuA Violin'}
                        add_meta(tmp_art.get('filename'),tmp_art.get('artist'))
                        # ts.writelines(str(tmp_art)+'\n')
                        break
                    elif re.search('k da',fn_tmp.lower()):
                        tmp_art={'filename':f,'artist':'K-DA'}
                        add_meta(tmp_art.get('filename'),tmp_art.get('artist'))
                        # ts.writelines(str(tmp_art)+'\n')
                        break
                    elif re.search(a_tmp.lower(),fn_tmp.lower()):
                        tmp_art={'filename':f,'artist':a}
                        add_meta(tmp_art.get('filename'),tmp_art.get('artist'))
                        # ts.writelines(str(tmp_art)+'\n')
                        break
                # else:
                #     tmp_art={'filename':f}
                #     ts.writelines(str(tmp_art)+'\n')
                #     break

os.chdir('/Users/unknown-x/Music')
get_artist_name()
match_artist()
