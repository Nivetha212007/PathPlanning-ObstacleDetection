from heapq import heappush,heappop
from time import perf_counter
def astar(grid,start,goal):
    t=perf_counter()
    if grid.is_obstacle(start) or grid.is_obstacle(goal): return False,[],0,0,(perf_counter()-t)*1000
    h=lambda a:abs(a[0]-goal[0])+abs(a[1]-goal[1])
    q=[]; seq=0; g={start:0}; came={}; closed=set(); heappush(q,(h(start),0,seq,start))
    while q:
        _,cg,_,cur=heappop(q)
        if cur in closed: continue
        closed.add(cur)
        if cur==goal:
            p=[cur]
            while cur in came: cur=came[cur]; p.append(cur)
            p.reverse(); return True,p,len(p)-1,len(closed),(perf_counter()-t)*1000
        for n in grid.neighbors(cur):
            if n in closed or grid.is_obstacle(n): continue
            ng=cg+1
            if ng<g.get(n,10**9):
                g[n]=ng; came[n]=cur; seq+=1; heappush(q,(ng+h(n),ng,seq,n))
    return False,[],0,len(closed),(perf_counter()-t)*1000
