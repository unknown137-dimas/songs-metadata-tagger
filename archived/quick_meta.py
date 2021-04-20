import music_tag,os,re

os.chdir('/Users/unknown-x/Music')
q='IZ-ONE'
t='like'
for f in os.listdir():
    if re.search('.m4a',f):
        a=music_tag.load_file(f)
            # f_tmp=f.replace('_',' ')
        if re.match(q,str(a['artist'])):
            # if re.search(t.lower(),f.lower()):
                # print(f)
            a['artist']='IZ*ONE'
            a.save()
# aud=f['artist']
# f['artist']='IZ-ONE'
# f.remove_tag('artist')
# print(sample, f['artist'])