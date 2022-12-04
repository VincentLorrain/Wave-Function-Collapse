
from PIL import Image
import numpy as np

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

        #get all the tiles
        for ox in range(out_x):
            start_x = ox*self.tile_size[0]
            stop_x = start_x+self.tile_size[0]
            for oy in range(out_y):
                start_y = oy*self.tile_size[1]
                stop_y = start_y+self.tile_size[1]

                tmp = self.img[start_x:stop_x,start_y:stop_y,:]
                tile_pos.append((tmp,(ox,oy)))
                print(ox,oy)
        #
        


tile = TilesRuleMaker('corgi.png')

tile.run()