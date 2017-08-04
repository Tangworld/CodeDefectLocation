import pickle
import types
import string
import MySQLdb
'''
file_txt = open('aspectjfullfilter.txt', 'rb')
file_pkl = file('aspectj.pkl', 'wb')

pre_data = file_txt.readlines()
#data = eval(pre_data)
print type(pre_data)
D = {}

for data in pre_data:
    dic = eval(data)
    key = dic['id']
    del dic['id']
    D[key] = dic

print D['166514']
print D['329111']
pickle.dump(D, file_pkl, True)
'''
'''
file_pkl = file('aspectj.pkl', 'rb')
file_csv = open('aspectj.csv', 'rb')
file_maps = file('maps.pkl', 'wb')
datas = pickle.load(file_pkl)
file_csv.readline()
lines = file_csv.readlines()

paths =[]
for line in lines:
    tmp = line.strip().split(',')[-1]
    print tmp
    #print tmp
    paths.append(tmp)
paths = list(set(paths))
del paths[0]
print len(paths)
#print paths

maps = {}
index = 0
pathsVS = []
for data in datas.keys():
    ps = datas[data]['ts']#.replace('.', '/')
    for p in ps:
        index += 1
        p = p.strip().replace('.', '/')
        pathsVS.append(p)
pathsVS = list(set(pathsVS))
print len(pathsVS)

for p in pathsVS:
    for path in paths:
        if p in string.lower(path):
            maps[p.replace('/','.')] = path
            break
        #print p
        #print maps[p], index
print 'weaver.patterns.perthisortargetpointcutvisitor' in maps.keys()
print len(maps.keys())

pickle.dump(maps, file_maps, True)
print "Done"
'''

def f2winsert():
    db = MySQLdb.connect("localhost", "root", "root", "locator")
    cursor = db.cursor()
    file_maps = file('maps.pkl', 'r')

    maps = pickle.load(file_maps)
    #print type(maps)

    print maps.items()
    for key in maps.keys():
        fullpath = maps[key]
        fullpath = fullpath.replace(' ', '')
        #print key
        # cursor.execute("select * from locator_bugidmap")
        #cursor.execute("select filepath from locator_filemap")
        #filepaths = cursor.fetchall()
        #for f in filepaths:
            # print type(f)
        #    if f[0] in maps.items():
        #        print type(f[0])
        cursor.execute("update locator_filemap set path_l2ss = '"+key+"' where filepath = '"+fullpath+"'")
        # cnt += 1

    db.commit()  # Commit the transaction
    cursor.close()
    db.close()

f2winsert()
