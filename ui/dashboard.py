from PySide6.QtCore import Qt,QTimer,Signal
from PySide6.QtGui import QPainter,QColor,QPen,QBrush
from PySide6.QtWidgets import *
from navigation.navigation_manager import Navigation

class Map(QWidget):
    clicked=Signal(object); hovered=Signal(object)
    def __init__(self,n): super().__init__(); self.n=n; self.setMinimumSize(760,600); self.setMouseTracking(True)
    def cell(self,p):
        s=min(self.width()/25,self.height()/20); ox=(self.width()-25*s)/2; oy=(self.height()-20*s)/2
        x=int((p.x()-ox)//s); y=int((p.y()-oy)//s); return (x,y) if 0<=x<25 and 0<=y<20 else None
    def mouseMoveEvent(self,e): self.hovered.emit(self.cell(e.position())); self.update()
    def mousePressEvent(self,e):
        if e.button()==Qt.LeftButton:
            c=self.cell(e.position())
            if c:self.clicked.emit(c)
    def paintEvent(self,e):
        p=QPainter(self); p.fillRect(self.rect(),QColor("#091018")); s=min(self.width()/25,self.height()/20); ox=(self.width()-25*s)/2; oy=(self.height()-20*s)/2
        path=set(self.n.path)
        for y in range(20):
            for x in range(25):
                c=(x,y); r=ox+x*s;t=oy+y*s
                p.fillRect(int(r),int(t),int(s),int(s),QColor("#d08a3e") if self.n.grid.is_obstacle(c) else QColor("#111c25"))
                if c in path:p.fillRect(int(r+s*.30),int(t+s*.30),int(s*.40),int(s*.40),QColor("#55b6ff"))
                p.setPen(QPen(QColor("#4b6172")));p.drawRect(int(r),int(t),int(s),int(s))
        def ctr(c):return ox+(c[0]+.5)*s,oy+(c[1]+.5)*s
        for c,col in ((self.n.start,"#25c997"),(self.n.goal,"#f2c94c")):
            x,y=ctr(c);p.setBrush(QBrush(QColor(col)));p.setPen(Qt.NoPen);p.drawEllipse(int(x-s*.22),int(y-s*.22),int(s*.44),int(s*.44))
        x,y=ctr(self.n.ugv.cell);p.setBrush(QBrush(QColor("#e9f0f6")));p.setPen(QPen(QColor("#4da3ff"),2));p.drawRoundedRect(int(x-s*.3),int(y-s*.2),int(s*.6),int(s*.4),5,5)
        p.setBrush(QBrush(QColor("#4da3ff")));p.setPen(Qt.NoPen);p.drawRect(int(x),int(y-s*.1),int(s*.2),int(s*.2))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__();self.n=Navigation();self.setWindowTitle("PathPlanning-ObstacleDetection — Autonomous UGV Path Planning System");self.resize(1400,880)
        self.setStyleSheet("QWidget{background:#081018;color:#dce6ef;font-family:Segoe UI} QPushButton{background:#142331;color:white;border:1px solid #2b4052;padding:9px;border-radius:5px} QFrame#p{background:#0d1720;border:1px solid #20303e;border-radius:8px} QListWidget{background:#09121a;border:1px solid #20303e}")
        c=QWidget();self.setCentralWidget(c);o=QVBoxLayout(c);h=QHBoxLayout();title=QLabel("PathPlanning-ObstacleDetection");title.setStyleSheet("font-size:25px;font-weight:700");h.addWidget(title);h.addWidget(QLabel("  AUTONOMOUS UGV PATH PLANNING SYSTEM"));h.addStretch();self.badge=QLabel();h.addWidget(self.badge);o.addLayout(h)
        b=QHBoxLayout();o.addLayout(b,1);lf=QFrame();lf.setObjectName("p");lv=QVBoxLayout(lf);lv.addWidget(QLabel("NAVIGATION MAP"));self.map=Map(self.n);self.map.clicked.connect(self.click);self.map.hovered.connect(lambda x:self.hover.setText("CELL —" if x is None else f"CELL X:{x[0]:02d} Y:{x[1]:02d}"));lv.addWidget(self.map);self.hover=QLabel("CELL —");lv.addWidget(self.hover);b.addWidget(lf,3)
        rf=QFrame();rf.setObjectName("p");r=QVBoxLayout(rf)
        self.info=QLabel();r.addWidget(QLabel("MISSION"));r.addWidget(self.info);self.metrics=QLabel();r.addWidget(QLabel("PATH PLANNING"));r.addWidget(self.metrics);self.env=QLabel();r.addWidget(QLabel("ENVIRONMENT"));r.addWidget(self.env)
        for text,fn in [("PLAN PATH",self.plan),("START NAVIGATION",self.start),("ADD OBSTACLE",lambda:self.mode("ADD")),("REMOVE OBSTACLE",lambda:self.mode("REMOVE")),("DEMO MODE",self.demo),("RESET",self.reset)]:
            q=QPushButton(text);q.clicked.connect(fn);r.addWidget(q)
        r.addWidget(QLabel("EVENT LOG"));self.events=QListWidget();r.addWidget(self.events,1);b.addWidget(rf,1)
        self.t=QTimer(self);self.t.timeout.connect(self.tick);self.t.start(500);self.refresh()
    def mode(self,m):self.n.mode=m;self.refresh()
    def click(self,c):
        self.n.add(c) if self.n.mode=="ADD" else self.n.remove(c);self.refresh()
    def plan(self):self.n.plan();self.refresh()
    def start(self):
        if not self.n.path:self.n.plan()
        self.n.ugv.moving=bool(self.n.path);self.n.status="NAVIGATING" if self.n.ugv.moving else self.n.status;self.n.log("NAVIGATION STARTED");self.refresh()
    def demo(self):self.reset();self.plan();self.start()
    def reset(self):self.n.reset();self.refresh()
    def tick(self):self.n.tick();self.refresh()
    def keyPressEvent(self,e):
        k=e.key()
        if k==Qt.Key_A:self.mode("ADD")
        elif k==Qt.Key_R:self.mode("REMOVE")
        elif k==Qt.Key_P:self.plan()
        elif k==Qt.Key_D:self.demo()
        elif k==Qt.Key_Space:self.start() if not self.n.ugv.moving else setattr(self.n.ugv,"moving",False)
        elif k==Qt.Key_Escape:self.reset()
    def refresh(self):
        ok,path,cost,nodes,ms=self.n.result;self.badge.setText(self.n.status)
        self.info.setText(f"START {self.n.start}\nDESTINATION {self.n.goal}\nUGV {self.n.ugv.cell}\nHEADING {self.n.ugv.heading:.0f}°")
        self.metrics.setText(f"ALGORITHM A*\nPATH STATUS {self.n.status}\nPATH LENGTH {len(path)} cells\nPATH COST {cost}\nNODES EXPLORED {nodes}\nPLANNING TIME {ms:.2f} ms")
        self.env.setText(f"OBSTACLES {self.n.grid.count()}\nGRID 25 × 20\nMODE {self.n.mode} OBSTACLE")
        self.events.clear();self.events.addItems(self.n.loglines);self.map.update()

if __name__=="__main__":
    app=QApplication([]);w=MainWindow();w.show();app.exec()
