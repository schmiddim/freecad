import FreeCAD
import os, glob, sys

# Offscreen rendering mit FreeCAD
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import FreeCADGui
FreeCADGui.setupWithoutGUI()

os.makedirs("gallery/img", exist_ok=True)

fcstd_files = glob.glob("**/*.FCStd", recursive=True)
print(f"Found {len(fcstd_files)} FCStd files")

for fcstd in fcstd_files:
    try:
        print(f"Processing: {fcstd}")
        doc = FreeCAD.openDocument(fcstd)
        name = os.path.splitext(os.path.basename(fcstd))[0]
        
        # Finde sichtbare Objekte
        visible_objects = [obj for obj in doc.Objects 
                          if hasattr(obj, 'Shape') and not obj.Shape.isNull()]
        
        if not visible_objects:
            print(f"  Skipping {name}: no valid shapes")
            FreeCAD.closeDocument(doc.Name)
            continue
        
        # Nutze FreeCAD's Thumbnail/Offscreen Rendering
        import importlib
        if importlib.util.find_spec("pivy"):
            from pivy import coin
            from FreeCAD import Base
            
            # Offscreen render mit coin3d
            viewport = FreeCADGui.ActiveDocument.ActiveView if FreeCADGui.ActiveDocument else None
            if viewport:
                for view_name, view_func in [("front", "viewFront"), ("right", "viewRight"), ("top", "viewTop")]:
                    getattr(viewport, view_func)()
                    viewport.fitAll()
                    viewport.saveImage(f"gallery/img/{name}_{view_name}.png", 800, 600, "White")
                    print(f"  Saved {name}_{view_name}.png")
        else:
            # Fallback: Erstelle Placeholder-Bild
            print(f"  Warning: pivy not available, skipping render for {name}")
        
        FreeCAD.closeDocument(doc.Name)
        
    except Exception as e:
        print(f"  Error processing {fcstd}: {e}")
        continue

print("Screenshot rendering complete")
