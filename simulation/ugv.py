import math
class UGV:
    def __init__(self,start): self.start=start; self.reset()
    def reset(self): self.cell=self.start; self.heading=0; self.moving=False
    def move(self,c):
        dx,dy=c[0]-self.cell[0],c[1]-self.cell[1]
        if dx or dy: self.heading=math.degrees(math.atan2(-dy,dx))%360
        self.cell=c
