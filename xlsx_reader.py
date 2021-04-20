import pandas,json

df=pandas.read_excel('./test.xlsx')
out=pandas.DataFrame(df,columns={'filename','artist','title','artist id'}).to_dict('records')
with open('spotipy-res.json','w') as s:
    s.write(json.dumps(out,indent=3))
# print(df)
# print(pandas.DataFrame(df,columns=['filename','artist','title']))
# artist=list(df['artist'])
# title=list(df['title'])
# art_id=list(df['artist id'])
# x=59
# print(artist[x])
# print(art_id[x])
# print(title[x])