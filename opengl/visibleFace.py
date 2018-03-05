import numpy as np


def visible(obj):
    m = 0
    vpnormal = np.array([0, 0, obj.bbox_center[2]+3])
    face = []
    for row in obj.faces:
        face.append(row[0])
    visVertices = obj.vertices[:]
    for i in range(len(face)):
        v1index = face[m][0] - 1
        v2index = face[m][1] - 1
        v3index = face[m][2] - 1
        vx1 = visVertices[v1index][0]
        vy1 = visVertices[v1index][1]
        vz1 = visVertices[v1index][2]
        vx2 = visVertices[v2index][0]
        vy2 = visVertices[v2index][1]
        vz2 = visVertices[v2index][2]
        vx3 = visVertices[v3index][0]
        vy3 = visVertices[v3index][1]
        vz3 = visVertices[v3index][2]
        a = (vy1 - vy2) * (vz1 - vz3) - (vy1 - vy3) * (vz1 - vz2)
        b = (vz1 - vz2) * (vx1 - vx3) - (vx1 - vx2) * (vz1 - vz3)
        c = (vx1 - vx2) * (vy1 - vy3) - (vx1 - vx3) * (vy1 - vy2)
        curnormal = np.array([a, b, c])

        if np.dot(vpnormal, curnormal) <= 0:
            del face[m]
            m = m - 1
        m = m + 1
    print(len(face))
