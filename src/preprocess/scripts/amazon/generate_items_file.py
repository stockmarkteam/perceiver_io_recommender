import pandas as pd
f = open("dataset/amazon/books/meta_Books.json")

ids=[]
title=[]
body=[]
cats=[]
cats_dict = {}
asin_map = {}
asin_id = 0
fc = open('dataset/amazon/books/processed/categories.txt','w')
for i, l in enumerate(f):
    a=eval(l)

    if a['asin'] not in asin_map:
        asin_id+=1
        asin_map[a['asin']]=asin_id

    ids.append(asin_map[a['asin']])

    if 'title' in a:
        title.append(a['title'])
    else: title.append('')
    cats.append(a['categories'][0][-1])
    if 'description' in a:
        body.append(a['description'])
    else: body.append('')
    if a['categories'][0][-1] not in cats_dict:
        cats_dict[a['categories'][0][-1]] = 1
        fc.write(a['categories'][0][-1]+'\n')
fc.close()

f = open('dataset/amazon/books/asin_id_map.txt','w')
for asin in asin_map:
    f.write(asin + '\t' + str(asin_map[asin]) + '\n')
f.close()
data = {'id': ids, 'title': title, 'body': body, 'category': cats}
df = pd.DataFrame(data).set_index('id')
#named 'articles' in order to conform with mind dataset
df.to_pickle('dataset/amazon/books/processed/train/articles.pkl')
