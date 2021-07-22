bl_info = {
  "name": "Origami FOLD",
  "author": "Shankar Sivarajan",
  "blender": (2,93,0),
  "version": (0, 0, 2),
  "location": "File > Import-Export",
  "description": "Import origami .fold files",
  "category": "Import-Export",
}

import bpy

import json

import numpy as np

import os

from bpy_extras.io_utils import ImportHelper

class ImportOrigami(bpy.types.Operator, ImportHelper):
    bl_idname = "import_origami.fold"
    bl_label = "Import Origami"
    
    bl_description = "Import origami"
    # bl_options = {'UNDO'}
  
    filename_ext = ".fold";
  
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
  
    filter_glob: bpy.props.StringProperty(
        default="*.fold",
        options={"HIDDEN"},
    )
  
    @classmethod
    def poll(cls, context):
      return True
  
    def execute(self, context):
        
        filename = self.filepath
        
        with open(filename) as json_file:
            origami_dict = json.load(json_file)
    
        verts_list = origami_dict['vertices_coords']
        edges_list = origami_dict['edges_vertices']
        faces_list = origami_dict['faces_vertices']
      
        verts = []
        edges = []
        faces = []

        for vert in verts_list:
            verts.append(vert)      
         
        for edge in edges_list:
            edges.append(edge) 

        for face in faces_list:
            faces.append(face) 

          
        name = origami_dict["frame_title"].split(" ")[0]
        me = bpy.data.meshes.new(name)
          
        me.from_pydata(verts, edges, faces)
          
        ob = bpy.data.objects.new(name, me)
          
        col = bpy.context.collection
        col.objects.link(ob)
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
          
        return {'FINISHED'}
  
    def draw(self, context):
        pass


def menu_import(self, context):
    self.layout.operator(ImportOrigami.bl_idname, text="Origami (.fold)")
    
def register():
    bpy.utils.register_class(ImportOrigami)
    
    bpy.types.TOPBAR_MT_file_import.append(menu_import)

def unregister():
    
    bpy.utils.unregister_class(ImportOrigami)
    
    bpy.types.TOPBAR_MT_file_import.remove(menu_import)
  
if __name__ == "__main__":
  register()
