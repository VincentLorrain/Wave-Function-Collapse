
from PIL import Image
import numpy as np

class Tiles:
    def __init__(self) -> None:
        self.idx = 0
        self.tiles = {}


    def add_tile(self,tile):
        if tile not in self:
            self.tiles[self.idx] = tile
            self.idx += 1

    def get_tile_idx(self,tile):
        for idx,val in self.tiles.items():
            if (tile==val).all:
                return idx
        return None

    def __repr__(self) -> str:
        return self.tiles.__repr__()
    
    def __len__(self):
        return len(self.tiles)

    def keys(self):
        return self.tiles.keys()

    def values(self):
        return self.tiles.values()

    def items(self):
        return self.tiles.items()

    def pop(self, *args):
        return self.tiles.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.tiles, dict_)

    def __contains__(self, item):

        for value in self.tiles.values():
            if (value == item).all():
                return True
        return False

    def __iter__(self):
        return iter(self.tiles)


class TilesRuleMaker:

    def __init__(self,path_img,tile_size = (3,3)) -> None:
            img = Image.open( path_img )
            img.load()
            img=img.convert(mode='RGB')
            img.show()

            #self.img = np.asarray( img, dtype='int8' )
            self.img = np.array( img)

            self.tile_size = tile_size
            print(self.img.shape)

            # img = Image.fromarray( self.img )
            # img.show()

    def run(self):
        
        tile_pos = []

        (ix,iy,ch) = self.img.shape
        out_x = ix//self.tile_size[0]
        out_y = iy//self.tile_size[1]

        deltas_pos = [(0,-1),(1,0) ,(0,1),(-1,0)]
        tiles = Tiles()
     

        #get all the tiles
        for ox in range(out_x):
            start_x = ox*self.tile_size[0]
            stop_x = start_x+self.tile_size[0]
            for oy in range(out_y):
                start_y = oy*self.tile_size[1]
                stop_y = start_y+self.tile_size[1]
                ref = self.img[start_x:stop_x,start_y:stop_y,:]
            
                tiles.add_tile(ref)
                 

        #get relation pos
        for ox in range(out_x):
            start_x = ox*self.tile_size[0]
            stop_x = start_x+self.tile_size[0]
            for oy in range(out_y):
                start_y = oy*self.tile_size[1]
                stop_y = start_y+self.tile_size[1]
                ref = self.img[start_x:stop_x,start_y:stop_y,:]

                print(ref)
                print(tiles.get_tile_idx(ref), end=' ')

                for delta_pos in deltas_pos:
                    new_ox = ox + delta_pos[0]
                    new_oy = oy + delta_pos[1]

                    if new_ox < 0 or new_ox >= out_x \
                    or new_oy < 0 or new_oy >= out_y:
                        continue
                    c_start_x = new_ox*self.tile_size[0]
                    c_stop_x = start_x+self.tile_size[0]
                    c_start_y = new_oy*self.tile_size[1]
                    c_stop_y = start_y+self.tile_size[1]
                    cmpr = self.img[c_start_x:c_stop_x,c_start_y:c_stop_y,:]

        print(tiles)
   

                


        

if __name__ == "__main__":
    tile = TilesRuleMaker('asset/corgi.png')
    tile.run()