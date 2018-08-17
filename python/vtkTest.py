import vtk

# def render():
#     # Create a rendering window and renderer
#     ren = vtk.vtkRenderer()
#     renWin = vtk.vtkRenderWindow()
#     renWin.AddRenderer(ren)
#     # Create a RenderWindowInteractor to permit manipulating the camera
#     iren = vtk.vtkRenderWindowInteractor()
#     iren.SetRenderWindow(renWin)
#     style = vtk.vtkInteractorStyleTrackballCamera()
#     iren.SetInteractorStyle(style)
#
#     filename = "tea100e.obj"
#     polydata = loadObj(filename)
#     ren.AddActor(polyDataToActor(polydata))
#     ren.SetBackground(0.1, 0.1, 0.1)
#
#     # enable user interface interactor
#     iren.Initialize()
#     renWin.Render()
#     iren.Start()
#
#
# def loadObj(fname):
#     """Load the given STL file, and return a vtkPolyData object for it."""
#     reader = vtk.vtkOBJReader()
#     reader.SetFileName(fname)
#     reader.Update()
#     polydata = reader.GetOutput()
#     return polydata
#
#
# def polyDataToActor(polydata):
#     """Wrap the provided vtkPolyData object in a mapper and an actor, returning
#     the actor."""
#     mapper = vtk.vtkPolyDataMapper()
#     mapper.SetInputConnection(polydata)
#     actor = vtk.vtkActor()
#     actor.SetMapper(mapper)
#     # actor.GetProperty().SetRepresentationToWireframe()
#     #actor.GetProperty().SetColor(0.5, 0.5, 1.0)
#     return actor
#
# render()

filename = "tea1000e.obj"
reader = vtk.vtkOBJReader()
reader.SetFileName(filename)
reader.Update()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.GetActiveCamera().SetPosition(-1064.1088490282684, 418.8666273583926, 1640.7995325161266)
renderer.GetActiveCamera().SetViewUp(0 , 1, 0)
renderer.SetBackground(0.1, 0.1, 0.1)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
renWin.Render()
iren.Start()