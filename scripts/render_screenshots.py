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
    for angle, suffix in [("front", "front"), ("right", "right"), ("top", "top")]:
        view.viewIsometric()
        view.saveImage(f"gallery/img/{name}_{suffix}.png", 800, 600, "White")
    
    FreeCAD.closeDocument(doc.Name)
