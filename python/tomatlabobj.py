class OBJ:
    def __init__(self, filename, swapyz=False):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.eye = []
        self.f = open('result.obj', 'w')

        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'e':
                v = [int(x) for x in values[1:4]]
                self.f.write("e ")
                for i in v:
                    self.f.write(str(i))
                    self.f.write(" ")
                self.f.write("\n")
            if values[0] == 'v':
                v = [float(x) for x in values[1:4]]
                if swapyz:
                    v = v[2], v[0], v[1]
                self.vertices.append(v)
                self.f.write("v ")
                for i in v:
                    self.f.write(str(i))
                    self.f.write(" ")
                self.f.write("\n")
            elif values[0] == 'f':
                face = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                self.faces.append(face)
                self.f.write("f ")
                for i in face:
                    self.f.write(str(i))
                    self.f.write(" ")
                self.f.write("\n")

obj = OBJ("./TEA2.obj", swapyz=False)
