import pandas as pd

f = open('dataset/amazon/books/asin_id_map.txt')
asin_map = {}

for l in f:
    ls = l[:-1].split('\t')
    asin_map[ls[0]] = int(ls[1])

for fi, fo in [['local_train_splitByUser', 'train'], ['local_test_splitByUser', 'valid']]:
    f = open('dataset/amazon/books/'+fi)

    bp = []
    hist = []
    hist_type=[]
    impressions=[]
    user_id=[]
    l = 'start'
    c = 1
    while True:
        l = f.readline()
        if not l: break
        ls1 = l.split('\t')
        l = f.readline()
        ls2 = l.split('\t')
        if ls1[1] != ls2[1]:
            #print(ls1, ls2)
            break

        hist.append([asin_map[h] for h in ls1[4].split('')])
        impressions.append([(asin_map[ls1[2]], int(ls1[0])),(asin_map[ls2[2]], int(ls2[0]))])
        #user_id.append(ls1[1])
        user_id.append(c)
        c+=1
        bp.append('2021-01-01')
        hist_type.append('view')

    #print(len(bp))
    data = {'base_period': bp, 'history': hist, 'history_types': hist_type, 'impressions': impressions, 'user_id':user_id}
    df = pd.DataFrame(data)
    df.to_pickle('dataset/amazon/books/processed/'+fo+'/behaviors.pkl')
