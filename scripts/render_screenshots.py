import FreeCAD, FreeCADGui
import os, glob

FreeCADGui.setupWithoutGUI()
os.makedirs("gallery/img", exist_ok=True)

for fcstd in glob.glob("**/*.FCStd", recursive=True):
    doc = FreeCAD.openDocument(fcstd)
    FreeCADGui.showMainWindow()
    gdoc = FreeCADGui.getDocument(doc.Name)
    
    name = os.path.splitext(os.path.basename(fcstd))[0]
    view = gdoc.ActiveView
    view.fitAll()
    
    # 3 Perspektiven
    view.viewFront()
    view.fitAll()
    view.saveImage(f"gallery/img/{name}_front.png", 800, 600, "White")
    
    view.viewRight()
    view.fitAll()
    view.saveImage(f"gallery/img/{name}_right.png", 800, 600, "White")
    
    view.viewTop()
    view.fitAll()
    view.saveImage(f"gallery/img/{name}_top.png", 800, 600, "White")
    
    FreeCAD.closeDocument(doc.Name)
