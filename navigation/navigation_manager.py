from planner.astar import astar
from simulation.ugv import UGV
from map.occupancy_grid import OccupancyGrid
class Navigation:
    def __init__(self):
        self.start=(2,2); self.goal=(22,17); self.grid=OccupancyGrid(); self.ugv=UGV(self.start)
        self.path=[]; self.result=(False,[],0,0,0); self.status="SYSTEM READY"; self.mode="ADD"; self.loglines=["SYSTEM READY"]
    def log(self,s): self.loglines.insert(0,s); self.loglines=self.loglines[:14]
    def plan(self,replan=False):
        self.status="REPLANNING" if replan else "PLANNING"; self.log(self.status)
        self.result=astar(self.grid,self.ugv.cell,self.goal)
        ok,self.path,cost,nodes,ms=self.result
        if ok: self.status="NEW PATH FOUND" if replan else "PATH FOUND"; self.log(self.status)
        else: self.path=[]; self.status="NO SAFE PATH AVAILABLE"; self.log(self.status)
        return ok
    def add(self,c):
        if c in (self.start,self.goal,self.ugv.cell): self.status="INVALID OBSTACLE POSITION"; self.log(self.status); return
        if self.grid.is_obstacle(c): return
        self.grid.set_obstacle(c); self.log(f"OBSTACLE ADDED: {c}")
        if c in self.path:
            self.status="PATH BLOCKED"; self.log("OBSTACLE DETECTED"); self.log("PATH BLOCKED"); self.plan(True)
    def remove(self,c):
        if self.grid.is_obstacle(c) and c not in (self.start,self.goal):
            self.grid.set_free(c); self.log(f"OBSTACLE REMOVED: {c}")
            if not self.path or self.status=="NO SAFE PATH AVAILABLE": self.plan(True)
    def tick(self):
        if not self.ugv.moving or not self.path:return
        if self.ugv.cell==self.goal:self.ugv.moving=False; self.status="GOAL REACHED"; self.log(self.status); return
        i=self.path.index(self.ugv.cell) if self.ugv.cell in self.path else -1
        if i<0 or i+1>=len(self.path): self.plan(True); return
        n=self.path[i+1]
        if self.grid.is_obstacle(n): self.ugv.moving=False; self.status="PATH BLOCKED"; self.plan(True); self.ugv.moving=bool(self.path); return
        self.ugv.move(n)
        if self.ugv.cell==self.goal:self.ugv.moving=False; self.status="GOAL REACHED"; self.log(self.status)
    def reset(self):
        self.grid=OccupancyGrid(); self.ugv=UGV(self.start); self.path=[]; self.result=(False,[],0,0,0); self.status="SYSTEM READY"; self.loglines=["SYSTEM READY"]
