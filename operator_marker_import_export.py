from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from bpy_extras.io_utils import ImportHelper
import bpy

class ExportTimelineMarkers(Operator, ExportHelper):
    """Export timeline markers to a CSV file"""
    bl_idname = "export.timeline_markers"
    bl_label = "Export timeline markers to a CSV file"
    filename_ext = ".csv"
    filter_glob = StringProperty(default="*.csv", options={'HIDDEN'}, maxlen=255)

    def execute(self, context):
        with open(filepath, 'w', encoding='utf-8') as f:
            for marker in context.scene.timeline_markers:
                f.write('{},{}\n'.format(marker.frame, marker.name))

        return {'FINISHED'}

class ImportTimelineMarkers(Operator, ImportHelper):
    bl_idname = "import.timeline_markers"
    bl_label = "Import timeline markers from a CSV file"
    filename_ext = '.csv'
    filter_glob = StringProperty(default='*.csv', options={'HIDDEN'})

    def execute(self, context):
        scene = context.scene
        self.properties.filepath
        with open(self.properties.filepath, 'r') as f:
            for line in f:
                frame, name = line.split(',')
                context.scene.timeline_markers.new(name.strip(), frame=int(frame))

        return {'FINISHED'}

def menu_func_export(self, context):
    self.layout.operator(ExportTimelineMarkers.bl_idname, text="Export timeline markers as CSV")

def menu_func_import(self, context):
    self.layout.operator(ImportTimelineMarkers.bl_idname, text="Import timeline markers as CSV")

def register():
    bpy.utils.register_class(ExportTimelineMarkers)
    bpy.utils.register_class(ImportTimelineMarkers)
    bpy.types.INFO_MT_file_export.append(menu_func_export)
    bpy.types.INFO_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ExportTimelineMarkers)
    bpy.utils.unregister_class(ImportTimelineMarkers)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()
