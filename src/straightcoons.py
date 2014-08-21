import math
from bezier import *

class coonsCalc:
    tl = None
    tr = None
    br = None
    bl = None
    P0pts = []
    P1pts = []
    Q0pts = []
    Q1pts = []
    
    def __init__(self,top_left,top_right,bottom_right,bottom_left,top_points,bottom_points,left_points,right_points):
        self.tl = top_left
        self.tr = top_right
        self.br = bottom_right
        self.bl = bottom_left
        self.P0pts = top_points
        self.P1pts = bottom_points
        self.Q0pts = left_points
        self.Q1pts = right_points
        self.Q0control=[]
        self.Q0control.append(self.getMidPoints(self.Q0pts[0],self.Q0pts[1]))
        for z in range(1,len(self.Q0pts)):
            self.Q0control.append(self.oppControl(self.Q0pts[z],self.Q0control[z-1]))
        for z in range(0,len(self.Q0control)):
            self.Q0control[z] = self.findThird(self.Q0pts[z],self.Q0control[z])
            
        self.Q1control=[]
        self.Q1control.append(self.getMidPoints(self.Q1pts[0],self.Q1pts[1]))
        for z in range(1,len(self.Q1pts)):
            self.Q1control.append(self.oppControl(self.Q1pts[z],self.Q1control[z-1]))
        for z in range(0,len(self.Q1control)):
            self.Q1control[z] = self.findThird(self.Q1pts[z],self.Q1control[z])
            
        self.P0control=[]
        self.P0control.append(self.getMidPoints(self.P0pts[0],self.P0pts[1]))
        for z in range(1,len(self.P0pts)):
            self.P0control.append(self.oppControl(self.P0pts[z],self.P0control[z-1]))
        for z in range(0,len(self.P0control)):
            self.P0control[z] = self.findThird(self.P0pts[z],self.P0control[z])
            
        self.P1control=[]
        self.P1control.append(self.getMidPoints(self.P1pts[0],self.P1pts[1]))
        for z in range(1,len(self.P1pts)):
            self.P1control.append(self.oppControl(self.P1pts[z],self.P1control[z-1]))
        for z in range(0,len(self.P1control)):
            self.P1control[z] = self.findThird(self.P1pts[z],self.P1control[z])
            
        self.calc = bezierCalc()
        
    def findThird(self, point1, point2):
        xdiff = float(point2[0] - point1[0])
        ydiff = float(point2[1] - point1[1])
        csq = pow(xdiff,2) + pow(ydiff,2)
        c = math.sqrt(csq)
        xdiff = xdiff/c
        ydiff = ydiff/c
        xdiff = xdiff * (c/3*2)
        ydiff = ydiff * (c/3*2)
        return(point1[0]+xdiff,point1[1]+ydiff)
        
    def getMidPoints(self, point1, point2):
        return ((point1[0]+point2[0])/float(2), (point1[1]+point2[1])/float(2))
    
    def oppControl(self, point, control):
        return (point[0]+(point[0]-control[0]),point[1]+(point[1]-control[1]))
        
    def getQCurve0Pt(self,v):
        return self.calc.calculateBezierPoint(self.Q0pts, self.Q0control, v)
        
    def getQCurve1Pt(self,v):
        return self.calc.calculateBezierPoint(self.Q1pts, self.Q1control, v)
        
    def getPCurve0Pt(self,u):
        return self.calc.calculateBezierPoint(self.P0pts, self.P0control, u)
        
    def getPCurve1Pt(self,u):
        return self.calc.calculateBezierPoint(self.P1pts, self.P1control, u)
    
    def getCoonsPoints(self,width,height):
        surface = {}
        for i in range(0,width):
            for j in range(0,height):
                u = float(float(i)/(float(width)-1))
                v = float(float(j)/(float(height)-1))
                surface[str(i) + "," + str(j)] = self.getCoonsPoint(u,v)
        return surface
    
    def getCoonsPoint(self,u,v):
        Q0 = self.getQCurve0Pt(v*(len(self.Q0pts)-1))
        Q1 = self.getQCurve1Pt(v*(len(self.Q1pts)-1))
        P0 = self.getPCurve0Pt(u*(len(self.P0pts)-1))
        P1 = self.getPCurve1Pt(u*(len(self.P1pts)-1))
        x = (1-u)*Q0[0] + u*Q1[0] + (1-v)*P0[0] + v*P1[0] - ((1-u)*(1-v)*self.tl[0] + u*(1-v)*self.tr[0] + (1-u)*v*self.bl[0] + u*v*self.br[0])
        y = (1-u)*Q0[1] + u*Q1[1] + (1-v)*P0[1] + v*P1[1] - ((1-u)*(1-v)*self.tl[1] + u*(1-v)*self.tr[1] + (1-u)*v*self.bl[1] + u*v*self.br[1])
        return(x,y)