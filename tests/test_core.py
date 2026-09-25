from navigation.navigation_manager import Navigation
def test_path():
 n=Navigation(); assert n.plan(); assert all(not n.grid.is_obstacle(c) for c in n.path)
def test_invalid():
 n=Navigation(); n.add(n.start); assert not n.grid.is_obstacle(n.start)
def test_replan_from_current():
 n=Navigation(); assert n.plan(); n.ugv.move(n.path[3]); old=n.ugv.cell; c=n.path[4]; n.add(c); assert n.path and n.path[0]==old and c not in n.path
