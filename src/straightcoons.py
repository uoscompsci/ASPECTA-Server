import math
from bezier import *
from scipy.weave import inline

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
        self.Q0control.append(self.getMidPoints(self.Q0pts[len(self.Q0pts)-1-0],self.Q0pts[len(self.Q0pts)-1-1]))
        for z in range(1,len(self.Q0pts)):
            self.Q0control.append(self.oppControl(self.Q0pts[len(self.Q0pts)-1-z],self.Q0control[z-1]))
        for z in range(0,len(self.Q0control)):
            self.Q0control[z] = self.findThird(self.Q0pts[len(self.Q0pts)-1-z],self.Q0control[z])
        self.Q0pts = list(reversed(self.Q0pts))

        self.Q1control=[]
        self.Q1control.append(self.getMidPoints(self.Q1pts[len(self.Q1pts)-1-0],self.Q1pts[len(self.Q1pts)-1-1]))
        for z in range(1,len(self.Q1pts)):
            self.Q1control.append(self.oppControl(self.Q1pts[len(self.Q1pts)-1-z],self.Q1control[z-1]))
        for z in range(0,len(self.Q1control)):
            self.Q1control[z] = self.findThird(self.Q1pts[len(self.Q1pts)-1-z],self.Q1control[z])
        self.Q1pts = list(reversed(self.Q1pts))
            
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
        point10, point11, point20, point21 = point1[0], point1[1], point2[0], point2[1]
        code = """
            #include <math.h>
            float xdiff = point20 - point10;
            float ydiff = point21 - point11;
            float csq = pow(xdiff,2) + pow(ydiff,2);
            float c = sqrt(csq);
            xdiff = xdiff/c;
            ydiff = ydiff/c;
            xdiff = xdiff * (c/3*2);
            ydiff = ydiff * (c/3*2);
            py::list ret;
            ret.append(point10+xdiff);
            ret.append(point11+ydiff);
            return_val = ret;
        """
        ret = inline(code, ['point10', 'point11', 'point20', 'point21'])
        return ret
        
    def getMidPoints(self, point1, point2):
        return ((float(point1[0])+float(point2[0]))/float(2), (float(point1[1])+float(point2[1]))/float(2))

    def oppControl(self, point, control):
        return (float(point[0])+(float(point[0])-float(control[0])),float(point[1])+(float(point[1])-float(control[1])))
        
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
        Q00, Q01, Q10, Q11, P00, P01, P10, P11 = Q0[0], Q0[1], Q1[0], Q1[1], P0[0], P0[1], P1[0], P1[1]
        tl0, tl1, tr0, tr1, bl0, bl1, br0, br1 = self.tl[0], self.tl[1], self.tr[0], self.tr[1], self.bl[0], self.bl[1], self.br[0], self.br[1]
        code = """
            float x = (1-u)*Q00 + u*Q10 + (1-v)*P00 + v*P10 - ((1-u)*(1-v)*tl0 + u*(1-v)*tr0 + (1-u)*v*bl0 + u*v*br0);
            float y = (1-u)*Q01 + u*Q11 + (1-v)*P01 + v*P11 - ((1-u)*(1-v)*tl1 + u*(1-v)*tr1 + (1-u)*v*bl1 + u*v*br1);
            py::list ret;
            ret.append(x);
            ret.append(y);
            return_val = ret;
        """
        ret = inline(code, ['u', 'v', 'Q00', 'Q10', 'P00', 'P10', 'tl0', 'tr0', 'bl0', 'br0', 'Q01', 'Q11', 'P01', 'P11', 'tl1', 'tr1', 'bl1', 'br1'])
        return ret
