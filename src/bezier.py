import math
from scipy.weave import inline

class bezierCalc:

    def getMidPoints(self, point1, point2):
        return ((float(point1[0])+float(point2[0]))/float(2), (float(point1[1])+float(point2[1]))/float(2))

    def oppControl(self, point, control):
        return (float(point[0])+(float(point[0])-float(control[0])),float(point[1])+(float(point[1])-float(control[1])))

    def getControlPoints(self, points):
        controlPoints = []
        controlPoints.append(self.getMidPoints((points[0][0],points[0][1]), (points[1][0],points[1][1])))
        for x in range(1,len(points)):
            controlPoints.append(self.oppControl((points[x][0],points[x][1]), controlPoints[x-1]))
        return controlPoints

    def calculateBezierPoint(self,points,controlPoints,t):
        t = round(t,2)
        point = self.weaveCalculateBezierSubPoint(t%1, points[int(math.floor(t))], controlPoints[int(math.floor(t))], self.oppControl(points[int(math.ceil(t))],controlPoints[int(math.ceil(t))]), points[int(math.ceil(t))])
        return point

    def weaveCalculateBezierSubPoint(self, t, p1, p1_direct, p2_direct, p2):
        code = """
        float u = 1-t;
        float tpow2 = t*t;
        float upow2 = u*u;
        float upow3 = upow2*u;
        float tpow3 = tpow2*t;

        float px = upow3 * p10;
        px = px + (3 * upow2 * t * p1direct0);
        px = px + (3 * u * tpow2 * p2direct0);
        px = px + (tpow3 * p20);

        float py = upow3 * p11;
        py = py + (3 * upow2 * t * p1direct1);
        py = py + (3 * u * tpow2 * p2direct1);
        py = py + (tpow3 * p21);

        py::list ret;
        ret.append(px);
        ret.append(py);
        return_val = ret;
        """
        p10, p11, p20, p21 = p1[0], p1[1], p2[0], p2[1]
        p1direct0, p1direct1, p2direct0, p2direct1 = p1_direct[0], p1_direct[1], p2_direct[0], p2_direct[1]
        ret = inline(code, ['t', 'p10', 'p11', 'p1direct0', 'p1direct1', 'p2direct0', 'p2direct1', 'p20', 'p21'])
        return ret

    def getSubCurvePoints(self,num_points, p1, p1_direct, p2_direct, p2):
        points = []
        for i in range(0,num_points+1):
            t = i / float(num_points)
            point = self.weaveCalculateBezierSubPoint(t, p1, p1_direct, p2_direct, p2)
            points.append(point)
        return points

    def getCurvePoints(self,points,num):
        controlPoints = self.getControlPoints(points)
        end = len(points)-1
        x = 0
        diff = float(end)/num
        finalPoints = []
        while(round(x,3)<=end):
            #print(x)
            finalPoints.append(self.calculateBezierPoint(points, controlPoints, x))
            x+=diff
        return finalPoints