
import numpy as np
# ╗╝═╚╔
# ╔═╗║
# ╚═╝
#tile name and asset

tiles = {0 : ' ',
        1 : '╔',
        2 : '╗',
        3 : '═',
        4 : '║',
        5 : '╚',
        6 : '╝',

        }

#tile rule for central and delta pos
#central tile { tuple offset (x,y) [possibility]}
tiles_rule = {
    #   up                    r                       d                       l
    0:{(0,-1):{0,3,5,6},       (1,0):{0,1,4,5},      (0,1):{0,1,2,3},      (-1,0):{0,2,4,6}},
    1:{(0,-1):{0,3,5,6},       (1,0):{0,2,3},        (0,1):{4,5,6},        (-1,0):{0,4,6}},
    2:{(0,-1):{0,3,5,6},       (1,0):{0,4,5},        (0,1):{4,5,6},        (-1,0):{1,3}},
    3:{(0,-1):{0,3},           (1,0):{2,3,6},        (0,1):{0,1,2,3},      (-1,0):{5,1,3}},
    4:{(0,-1):{1,2,4},         (1,0):{0,4,1,5},      (0,1):{5,6,4},        (-1,0):{0,2,6,4}},
    5:{(0,-1):{4,1,2},         (1,0):{3,6},          (0,1):{0,1,2,3},      (-1,0):{4,6,0,2}},
    6:{(0,-1):{4,1,2},         (1,0):{0,4,1},        (0,1):{0,1,2,3},      (-1,0):{1,2,3,5}},
}

def get_entropy(map_v,nb_tile):
    entropy = 0.
    for y in range(map_v.shape[1]):
        for x in range(map_v.shape[0]):
            e_x = len(map_v[x,y])/nb_tile
            e_min = 1./nb_tile
            e_max = 1.
            case_entropy = (e_x - e_min) / (e_max-e_min)
            #print(case_entropy,end=' ')
            entropy += case_entropy
        #print()

    entropy = entropy/(map_v.shape[0]*map_v.shape[1])
    print(entropy)
    return entropy

def plot_map(map_v,nb_tile):
    (size_x,size_y) = map_v.shape
    for idx_y in range(size_y):
        for idx_x in range(size_x):
            print('|',end ='')
            for idx_p , i in enumerate(map_v[idx_x,idx_y]):
                print(i,',',end='')

            print('  '*(nb_tile-len(map_v[idx_x,idx_y])),end='')
        print()
    print()

def plot_tiles(map_v,tiles):
    (size_x,size_y) = map_v.shape
    for idx_y in range(size_y):
        for idx_x in range(size_x):
            if len(map_v[idx_x,idx_y]) >1:
                print('x',end ='')
            else:
                for i in map_v[idx_x,idx_y]:
                    print(tiles[i],end ='')
        print()
    print()

def run_rule_pos(map_v,x,y,tiles_rule):
    pos_tiles = map_v[x,y]
    to_applies = {}

    for central in pos_tiles:
        for delta_pos in tiles_rule[central].keys():

            #init the to_applies
            new_x = x + delta_pos[0]
            new_y = y + delta_pos[1]
            if not(new_x >= 0 and new_x < map_v.shape[0]\
            and new_y >= 0 and new_y < map_v.shape[1]):
                continue
            
            new_set = to_applies.get((new_x,new_y),set()).union(tiles_rule[central][delta_pos] )

            if new_set != set():
                to_applies[(new_x,new_y)] = new_set
        
    #print(to_applies)
    #applies to map
    for new_pos,possibility in to_applies.items():
        map_v[new_pos] =map_v[new_pos].intersection(possibility)


def set_next(map_v,nb_tile):
    min_e = nb_tile
    out = []
    for x in range(map_v.shape[0]):
        for y in range(map_v.shape[1]):
            e_tile =  len(map_v[x,y])
            if e_tile > 1 and e_tile <= min_e  :
                min_e = e_tile
                out.append((x,y))

    idx = np.random.randint(len(out)-1) if len(out) >1 else 0
    out = out[idx]

    if len(map_v[out]) == 1:
        return
    idx = np.random.randint(len(map_v[out])-1)
    map_v[out] = {list(map_v[out])[idx]}

# size x,y
map_size = (20,10)

#init map

map_v=np.empty(map_size,dtype=object)
for x in range(map_v.shape[0]):
    for y in range(map_v.shape[1]):
        map_v[x,y] = set(tiles.keys())

get_entropy(map_v,len(tiles.keys()))
#test




import time
plot_map(map_v,len(tiles.keys()))

while get_entropy(map_v,len(tiles.keys())) > 0.0001:
    #plot_tiles(map_v,tiles) 
    for x in range(map_v.shape[0]):
        for y in range(map_v.shape[1]):
            run_rule_pos(map_v,x,y,tiles_rule)
    # plot_tiles(map_v,tiles)
    # plot_map(map_v,len(tiles.keys()))
    

    set_next(map_v,len(tiles.keys()))

plot_map(map_v,len(tiles.keys()))
plot_tiles(map_v,tiles)