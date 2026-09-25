FREE=0
OBSTACLE=1
class OccupancyGrid:
    def __init__(self,w=25,h=20):
        self.width,self.height=w,h
        self.grid=[[FREE]*w for _ in range(h)]
        for x in range(w): self.grid[0][x]=self.grid[h-1][x]=OBSTACLE
        for y in range(h): self.grid[y][0]=self.grid[y][w-1]=OBSTACLE
        for x in range(4,11): self.grid[5][x]=OBSTACLE
        for x in range(14,22): self.grid[5][x]=OBSTACLE
        for y in range(7,16): self.grid[y][7]=OBSTACLE
        for y in range(4,13): self.grid[y][17]=OBSTACLE
        for x in range(10,17): self.grid[14][x]=OBSTACLE
        for x in range(19,23): self.grid[11][x]=OBSTACLE
        for c in [(7,5),(12,5),(17,8),(7,12),(13,14),(19,11)]: self.set_free(c)
    def valid(self,c): return 0<=c[0]<self.width and 0<=c[1]<self.height
    def is_obstacle(self,c): return not self.valid(c) or self.grid[c[1]][c[0]]==OBSTACLE
    def set_obstacle(self,c): self.grid[c[1]][c[0]]=OBSTACLE
    def set_free(self,c): self.grid[c[1]][c[0]]=FREE
    def neighbors(self,c):
        x,y=c
        for d in ((1,0),(-1,0),(0,1),(0,-1)):
            n=(x+d[0],y+d[1])
            if self.valid(n): yield n
    def count(self): return sum(r.count(OBSTACLE) for r in self.grid)
