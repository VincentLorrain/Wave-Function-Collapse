import numpy as np
import sys

print(sys.getrecursionlimit())


tiles = {
    -1:'o',
    0 : ' ',
    1 : '╔',
    2 : '╗',
    3 : '═',
    4 : '║',
    5 : '╚',
    6 : '╝',
}

"""
the rule is define depending of a grid deltas (x,y)
      (0,1)
        |  
(-1,0)--O--(1,0)
        |
     (0-,1)

then for each type of tiles in the center we define the tiles that can be set to the delta 
"""
tiles_rule = {
    (0,-1):{-1:{0,1,2,3,4,5,6}, 0:{0,3,5,6},    1:{0,3,5,6},    2:{0,3,5,6},    3:{0,3},        4:{1,2,4},      5:{4,1,2},      6:{4,1,2}},   #u
    (1,0) :{-1:{0,1,2,3,4,5,6}, 0:{0,1,4,5},    1:{2,3,6},      2:{0,4,5},      3:{2,3,6},      4:{0,4,1,5},    5:{3,6},        6:{0,4,1}},   #r
    (0,1) :{-1:{0,1,2,3,4,5,6}, 0:{0,1,2,3},    1:{4,5,6},      2:{4,5,6},      3:{0,1,2,3},    4:{5,6,4},      5:{0,1,2,3},    6:{0,1,2,3}}, #d
    (-1,0):{-1:{0,1,2,3,4,5,6}, 0:{0,2,4,6},    1:{0,4,6},      2:{1,3},        3:{5,1,3},      4:{0,2,6,4},    5:{4,6,0,2},    6:{1,3,5}}, #l
}

class WaveFunctionCollapse:

    def __init__(self,tiles,tiles_rule,map_size = (10,10)) -> None:
        self.tiles      =tiles
        self.nb_tile    =len(tiles.keys())
        self.tiles_rule =tiles_rule
        #make the map
        self.limit_map  =map_size
        self.map_v=np.empty(map_size,dtype=object)
        for x in range(self.limit_map[0]):
            for y in range(self.limit_map[1]):
                self.map_v[x,y] = set(tiles.keys())

    def get_rules_form_centrals(self,centrals:set()):
        local_rule = {}
        for delta_pos,possibility in self.tiles_rule.items():
            local_rule[delta_pos] = set()
            i_centrals = set(possibility.keys()).intersection(centrals)
            for i in i_centrals:
                local_rule[delta_pos]=local_rule[delta_pos].union(possibility[i])
        return local_rule

    def collapse(self,position:tuple):

        local_rule = self.get_rules_form_centrals(self.map_v[position])
        for delta_pos,rule in local_rule.items():
            new_pos = (position[0]+delta_pos[0],position[1]+delta_pos[1])
            #is in the map 
            if new_pos[0] < 0 or new_pos[1] < 0 \
            or new_pos[0] >= self.limit_map[0] or new_pos[1] >= self.limit_map[1]:
                continue

            
            new_possibility = self.map_v[new_pos].intersection(rule)

            if new_possibility == set():
               
                self.map_v[new_pos] = {-1}
                print('Untrue',position,new_pos)
                
                #raise()
                continue

            if new_possibility != self.map_v[new_pos]:
                #self.plot()
                self.map_v[new_pos] = new_possibility
                self.collapse(new_pos)

    def run(self):
        #get next
        #print('init')
        min_possibility = self.nb_tile
        next_pos = []
        #print('go')
        for y in range(self.limit_map[1]):
            for x in range(self.limit_map[0]):
                #print(min_possibility)
                if len(self.map_v[x,y]) > 1 :
                    if len(self.map_v[x,y]) < min_possibility:
                        min_possibility = len(self.map_v[x,y])
                        next_pos = [(x,y)]
                    elif len(self.map_v[x,y]) == min_possibility:
                        next_pos.append((x,y))
        # self.plot()
        # print('next_pos',next_pos)

        if next_pos == []:
            return
        #set the new pos
        idx_pos = np.random.randint(len(next_pos)-1) if len(next_pos) >1 else 0
        next_pos = next_pos[idx_pos]
        print('next_pos',next_pos)
        #c
        
        #print(self.map_v[next_pos])
        choice = {list(self.map_v[next_pos])[ np.random.randint(len(self.map_v[next_pos])-1) ]}
        #print(choice)

        self.map_v[next_pos] = choice

        #self.plot()

        self.collapse(next_pos)
        self.run()

    def get_max_possibility(self):
        max_possibility = (-1,(-1,-1))
        for y in range(self.limit_map[1]):
            for x in range(self.limit_map[0]):
                if len(self.map_v[x,y]) > max_possibility[0]:
                    max_possibility = (len(self.map_v[x,y]),(x,y))
        return max_possibility

    def plot(self):
        (max_len, max_pos) = self.get_max_possibility()
        for y in range(self.limit_map[1]):
            for x in range(self.limit_map[0]):
                print(f'|',end='')
                for possibility in self.map_v[x,y]:
                    print(f'{possibility} ',end='')
                
                print('  '*(max_len-len(self.map_v[x,y])),end='')
            print()

    def plot_tile(self):
        (max_len, max_pos) = self.get_max_possibility()
        for y in range(self.limit_map[1]):
            for x in range(self.limit_map[0]):
                if len(self.map_v[x,y])!= 1:
                    print('x',end='')
                else:
                    print(self.tiles[list(self.map_v[x,y])[0]],end='')
                
            print()

    
if __name__ == "__main__":
    a = WaveFunctionCollapse(tiles,tiles_rule,(10,10))
    a.run()                 
    a.plot_tile()

