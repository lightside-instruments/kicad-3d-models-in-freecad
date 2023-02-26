import FreeCAD
import FreeCADGui


App = FreeCAD # shortcut
Gui = FreeCADGui # shortcut

# FreeCAD.newDocument("shape")
FreeCAD.setActiveDocument("shape")

name="PLASTIC-BLUE-01",
ambientIntensity= 0.565,
diffuseColor= (0.137, 0.402, 0.727),
specularColor= (0.359, 0.379, 0.270),
shininess=0.25

doc = App.ActiveDocument
for obj in doc.Objects:
	print(obj)
	print(obj.Name)
	if(obj.Name.startswith('Shape0')):
		print(Gui.ActiveDocument.getObject(obj.Name).ShapeColor)
#	Gui.ActiveDocument.getObject(obj.Name).ShapeColor = 
#	Gui.ActiveDocument.getObject(obj.Name).LineColor = 
#	Gui.ActiveDocument.getObject(obj.Name).PointColor = 
		Gui.ActiveDocument.getObject(obj.Name).DiffuseColor = diffuseColor

#expVRML.say(material_substitutions)
