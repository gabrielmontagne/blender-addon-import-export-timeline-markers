from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper, ImportHelper
import bpy

bl_info = {
    'name': 'Import / export markers to CSV',
    'author': 'gabriel montagné, gabriel@tibas.london',
    'version': (0, 0, 1),
    'blender': (2, 80, 0),
    'description': 'Replace makers in other scenes with the markers in this scene',
    'tracker_url': 'https://github.com/gabrielmontagne/blender-addon-project-markers/issues?status=new&status=open',
    'category': 'Object'
}

class MARKER_OT_export_csv(Operator, ExportHelper):
    """Export marker to CSV"""
    bl_idname = "marker.export_csv"
    bl_label = "Export markers to CSV"

    filename_ext = ".csv"
    filter_glob: StringProperty(default="*.csv", options={'HIDDEN'}, maxlen=255)

    def execute(self, context):
        scene = context.scene
        markers = scene.timeline_markers

        with open(self.properties.filepath, 'w', encoding='utf-8') as f:
            for marker in context.scene.timeline_markers:
                f.write('{}|{}\n'.format(marker.frame, marker.name))

        return {'FINISHED'}

class MARKER_OT_import_csv(Operator, ImportHelper):
    """Import marker from CSV"""
    bl_idname = "marker.import_csv"
    bl_label = "Import markers from CSV"

    filename_ext = ".csv"
    filter_glob: StringProperty(default="*.csv", options={'HIDDEN'}, maxlen=255)
    replace_current: BoolProperty(name='Replace current markers', default=True)

    def execute(self, context):
        scene = context.scene
        if self.replace_current:
            for xm in scene.timeline_markers:
                scene.timeline_markers.remove(xm)

        with open(self.properties.filepath, 'r') as f:
            for line in f:
                frame, name = line.split('|')
                scene.timeline_markers.new(name.strip(), frame=int(frame))

        return {'FINISHED'}

def register():
    bpy.utils.register_class(MARKER_OT_import_csv)
    bpy.utils.register_class(MARKER_OT_export_csv)

def unregister():
    bpy.utils.unregister_class(MARKER_OT_export_csv)
    bpy.utils.unregister_class(MARKER_OT_import_csv)

if __name__ == "__main__":
    register()
