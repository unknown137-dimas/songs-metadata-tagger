import os,re

dir=os.getcwd()
os.chdir('/users/unknown-x/movies/kpop')
lst=os.listdir("/Users/unknown-x/movies/kpop/")
lst.sort()
q=['mv','music video']
with open(dir+'/mv_counter.txt','w') as mc:
    for f in lst:
        count=0
        if not re.search('\.',f):
            for i in os.listdir(f):
                i_tmp=i.replace('_',' ')
                for a in q:
                    if re.search('\.',i) and re.search(a,i_tmp.lower()):
                        count+=1
            mc.write(str(f+' '+str(count))+'\n')
