import math

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
    
    def getCoonsPoints(self,width,height):
        surface = {}
        for i in range(0,width):
            for j in range(0,height):
                u = i/(width-1)
                v = i/(height-1)
                surface[str[i] + "," + str[j]] = getCoonsPoint(u,v)
        return surface
    
    def getCoonsPoint(self,u,v):
        Q0 = getQCurve0Pt(v)
        Q1 = getQCurve1Pt(v)
        P0 = getPCurve0Pt(u)
        P1 = getPCurve1Pt(u)
        x = (1-u)*Q0[0] + u*Q1[0] + (1-v)*P0[0] + v*P1[0] - ((1-u)*(1-v)*self.tl[0] + u*(1-v)*self.tr[0] + (1-u)*v*self.br[0] + u*v*self.bl[0])
        y = (1-u)*Q0[1] + u*Q1[1] + (1-v)*P0[1] + v*P1[1] - ((1-u)*(1-v)*self.tl[1] + u*(1-v)*self.tr[1] + (1-u)*v*self.br[1] + u*v*self.bl[1])
        return(x,y)
    
    def getQCurve0Pt(self,v):
        return (1-(v%1))*self.Q0pts[math.floor(v)]+(v%1)*self.Q0pts[math.ceil(v)]
        
    def getQCurve1Pt(self,v):
        return (1-(v%1))*self.Q1pts[math.floor(v)]+(v%1)*self.Q1pts[math.ceil(v)]
        
    def getPCurve0Pt(self,u):
        return (1-(u%1))*self.P0pts[math.floor(u)]+(u%1)*self.P0pts[math.ceil(u)]
        
    def getPCurve1Pt(self,u):
        return (1-(u%1))*self.P1pts[math.floor(u)]+(u%1)*self.P1pts[math.ceil(u)]