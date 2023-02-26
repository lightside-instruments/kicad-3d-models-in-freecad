import FreeCAD
import FreeCADGui


App = FreeCAD # shortcut
Gui = FreeCADGui # shortcut

# FreeCAD.newDocument("shape")
FreeCAD.setActiveDocument("shape")

Gui.insert(u"112-024-113R001.wrl","shape")

