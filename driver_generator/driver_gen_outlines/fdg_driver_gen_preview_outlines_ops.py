from enum import Enum
import os
import bpy
from bpy.types import Operator

class FDG_OT_GeneratePreviewOutlines_Op(Operator):
    bl_idname = "fdg.gen_preview_outlines"
    bl_label = "Generate Preview Outlines"
    bl_description = "Generates the preview Outlines for the selected Characters"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        if not (wm.output_path or wm.file_name):
            return False
        if len(context.scene.collection_list) == 0:
            return False

        return True

    def execute(self, context):
        wm = context.window_manager
        scene = context.scene
    	
        for item in scene.collection_list:
            collection = item.character_collection
            print(collection)
            print(item)
            self.prepare_collection_for_render(collection, item)
        bpy.ops.fdg.conform_visibilities()
        self.prepare_scene_for_render(context)
        filepath = bpy.data.filepath
        if "_line.blend" in filepath:
            bpy.ops.wm.save_mainfile(filepath=filepath)
        else:
            filepath = filepath[:-6] + "_line" + filepath[-6:]
            bpy.ops.wm.save_as_mainfile(filepath=filepath)
        

        return {'FINISHED'}

    def create_preview_line(self, collection, transmission: bool, item=None):
        context = bpy.context
        outline_collection = bpy.data.collections.get("Outlines")
        if not outline_collection:
            outline_collection = bpy.data.collections.new("Outlines")
            context.scene.collection.children.link(outline_collection)
        
        gp_data = bpy.data.grease_pencils.new(collection.name + "_lines")
        gp_ob = bpy.data.objects.new(collection.name + "_lines", gp_data)
        outline_collection.objects.link(gp_ob)
        if item:
            item.outline_object = gp_ob

        gp_ob.show_in_front = True

        gp_layer = gp_data.layers.new(name="gp_layer", set_active = True)
        gp_layer.frames.new(0)
        gp_layer.use_lights = False

        if "gp_mat" in bpy.data.materials.keys():
            gp_mat = bpy.data.materials["gp_mat"]
        else:
            gp_mat = bpy.data.materials.new("gp_mat")

        if not gp_mat.is_grease_pencil:
            bpy.data.materials.create_gpencil_data(gp_mat)

        gp_mat.grease_pencil.color = (0.058, 0.018, 0.025, 1.0)

        gp_data.materials.append(gp_mat)

        lineart = gp_ob.grease_pencil_modifiers.new("Line Art", 'GP_LINEART')
        lineart.source_collection = collection
        lineart.target_layer = gp_layer.info
        lineart.target_material = gp_mat
        lineart.smooth_tolerance = 0.0
        lineart.use_intersection = False

        

        

        """ if transmission:
            transmission_lineart = gp_ob.grease_pencil_modifiers.new("Transmission Line Art", 'GP_LINEART')
            transmission_lineart.source_collection = collection
            transmission_lineart.target_layer = gp_layer.info
            transmission_lineart.target_material = gp_mat
            transmission_lineart.use_cache = True
            transmission_lineart.level_start = 1
            transmission_lineart.use_material_mask = True
            transmission_lineart.use_material_mask_bits[0] = True
            transmission_lineart.smooth_tolerance = 0.0
            transmission_lineart.use_intersection = False """

        thickness = gp_ob.grease_pencil_modifiers.new("Thickness", 'GP_THICK')
        thickness.use_normalized_thickness = True
        thickness.thickness = 3
        thickness.use_custom_curve = True

        thickness.curve.curves[0].points[0].location = (0.0, 0.625)
        thickness.curve.curves[0].points[1].location = (1.0, 0.625)
        thickness.curve.curves[0].points.new(0.5, 1.0)

        for point in thickness.curve.curves[0].points:
            point.handle_type = 'AUTO'
        thickness.curve.update()

    def check_for_glasses(self, collection):
        """ for obj in collection.all_objects:
            for mat_slot in obj.material_slots:
                mat_line_art = mat_slot.material.lineart
                if mat_line_art.use_material_mask:
                    return True """

        return False

    def setup_booleans_in_collection(self, collection):
        for obj in collection.all_objects:
            for mod in obj.modifiers:
                if mod.type == 'BOOLEAN':
                    mod.solver = 'EXACT'
                    mod.use_self = True

    def prepare_collection_for_render(self, collection, item):
        print(not item)
        if not item.outline_object:
            
            self.create_preview_line(collection, self.check_for_glasses(collection), item)
                
        self.setup_booleans_in_collection(collection)

    def prepare_scene_for_render(self, context):
        wm = context.window_manager
        context.space_data.overlay.show_overlays = False
        context.space_data.show_gizmo = False
        context.scene.render.resolution_x = 1920
        context.scene.render.resolution_y = 1080
        context.scene.render.resolution_percentage = 100
        context.scene.render.image_settings.file_format = 'JPEG'
        context.scene.render.image_settings.color_mode = 'RGB'
        context.scene.render.image_settings.compression = 90
        context.scene.render.simplify_subdivision = 1
        context.space_data.shading.type = 'MATERIAL'
        context.space_data.region_3d.view_perspective = 'CAMERA'
        path = os.path.join(wm.output_path, wm.file_name + ".####.jpg")
        context.scene.render.filepath = path

class FDG_OT_ActivateBooleans_OP(Operator):
    bl_idname = "fdg.activate_booleans"
    bl_label = "Exact Booleans"
    bl_description = "Sets all Booleans in the given collections to to Exact with self intersection"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if len(context.scene.collection_list) == 0:
            return False

        return True

    def execute(self, context):
        scene = context.scene
    	
        for item in scene.collection_list:
            collection = item.character_collection
            self.setup_booleans_in_collection(collection)

        return {'FINISHED'}

    def setup_booleans_in_collection(self, collection):
        for obj in collection.all_objects:
            for mod in obj.modifiers:
                if mod.type == 'BOOLEAN':
                    mod.solver = 'EXACT'
                    mod.use_self = True

class FDG_OT_DeactivateBooleans_OP(Operator):
    bl_idname = "fdg.deactivate_booleans"
    bl_label = "Fast Booleans"
    bl_description = "Sets all Booleans in the given collections to Fast"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if len(context.scene.collection_list) == 0:
            return False

        return True

    def execute(self, context):
        scene = context.scene
    	
        for item in scene.collection_list:
            collection = item.character_collection
            self.setup_booleans_in_collection(collection)

        return {'FINISHED'}

    def setup_booleans_in_collection(self, collection):
        for obj in collection.all_objects:
            for mod in obj.modifiers:
                if mod.type == 'BOOLEAN':
                    mod.solver = 'FAST'

class FDG_OT_PrepareScene_OP(Operator):
    bl_idname = "fdg.prepare_scene"
    bl_label = "Prepare Scene"
    bl_description = "Sets Resolution, Output Path, File Format. Sets Simplify to 1, turns off Overlays and Gizmos and sets sahding type to Material. Sets View to Camera View."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        context.space_data.overlay.show_overlays = False
        context.space_data.show_gizmo = False
        context.scene.render.resolution_x = 1920
        context.scene.render.resolution_y = 1080
        context.scene.render.resolution_percentage = 100
        context.scene.render.image_settings.file_format = 'JPEG'
        context.scene.render.image_settings.color_mode = 'RGB'
        context.scene.render.image_settings.compression = 90
        context.scene.render.simplify_subdivision = 1
        context.space_data.shading.type = 'MATERIAL'
        context.space_data.region_3d.view_perspective = 'CAMERA'
        path = os.path.join(wm.output_path, wm.file_name + ".####.jpg")
        context.scene.render.filepath = path

        return {'FINISHED'}

class FDG_OT_CreatePreviewLines_OP(Operator):
    bl_idname = "fdg.create_preview_lines"
    bl_label = "Create Preview Outlines"
    bl_description = "Creates preview Outlines for all selected collections."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene

        for item in scene.collection_list:
            collection = item.character_collection
            if not item.outline_object:
                self.create_preview_line(collection,False, item)

        return {'FINISHED'}

    def create_preview_line(self, collection, transmission: bool, item=None):
        context = bpy.context
        outline_collection = bpy.data.collections.get("Outlines")
        if not outline_collection:
            outline_collection = bpy.data.collections.new("Outlines")
            context.scene.collection.children.link(outline_collection)
        
        gp_data = bpy.data.grease_pencils.new(collection.name + "_lines")
        gp_ob = bpy.data.objects.new(collection.name + "_lines", gp_data)
        outline_collection.objects.link(gp_ob)
        if item:
            item.outline_object = gp_ob

        gp_ob.show_in_front = True

        gp_layer = gp_data.layers.new(name="gp_layer", set_active = True)
        gp_layer.frames.new(0)
        gp_layer.use_lights = False

        if "gp_mat" in bpy.data.materials.keys():
            gp_mat = bpy.data.materials["gp_mat"]
        else:
            gp_mat = bpy.data.materials.new("gp_mat")

        if not gp_mat.is_grease_pencil:
            bpy.data.materials.create_gpencil_data(gp_mat)

        gp_mat.grease_pencil.color = (0.058, 0.018, 0.025, 1.0)

        gp_data.materials.append(gp_mat)

        lineart = gp_ob.grease_pencil_modifiers.new("Line Art", 'GP_LINEART')
        lineart.source_collection = collection
        lineart.target_layer = gp_layer.info
        lineart.target_material = gp_mat
        lineart.smooth_tolerance = 0.01
        lineart.use_intersection = False

        

        

        """ if transmission:
            transmission_lineart = gp_ob.grease_pencil_modifiers.new("Transmission Line Art", 'GP_LINEART')
            transmission_lineart.source_collection = collection
            transmission_lineart.target_layer = gp_layer.info
            transmission_lineart.target_material = gp_mat
            transmission_lineart.use_cache = True
            transmission_lineart.level_start = 1
            transmission_lineart.use_material_mask = True
            transmission_lineart.use_material_mask_bits[0] = True
            transmission_lineart.smooth_tolerance = 0.0
            transmission_lineart.use_intersection = False """

        thickness = gp_ob.grease_pencil_modifiers.new("Thickness", 'GP_THICK')
        thickness.use_normalized_thickness = True
        thickness.thickness = 3
        thickness.use_custom_curve = True

        thickness.curve.curves[0].points[0].location = (0.0, 0.625)
        thickness.curve.curves[0].points[1].location = (1.0, 0.625)
        thickness.curve.curves[0].points.new(0.5, 1.0)

        for point in thickness.curve.curves[0].points:
            point.handle_type = 'AUTO'
        thickness.curve.update()

class FDG_OT_SaveLineFile_OP(Operator):
    bl_idname = "fdg.save_line_file"
    bl_label = "Save as Line File"
    bl_description = "Saves this File as new File with the _line suffix"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        filepath = bpy.data.filepath
        if "_line.blend" in filepath:
            bpy.ops.wm.save_mainfile(filepath=filepath)
        else:
            filepath = filepath[:-6] + "_line" + filepath[-6:]
            bpy.ops.wm.save_as_mainfile(filepath=filepath)

        return {'FINISHED'}

class FDG_OT_RenderPreview_Op(Operator):
    bl_idname = "fdg.render_preview"
    bl_label = "Render Preview"
    bl_description = "Renders the Preview"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.render.opengl(animation=True)

        return {'FINISHED'}

class FDG_OT_AddCollection_Op(Operator):
    bl_idname = "fdg.add_collection"
    bl_label = "Add Collection"
    bl_description = "Adds Empty Collection Pointer to Selection List"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        
        scene = context.scene
        scene.collection_list.add()
        
        return {'FINISHED'}

    

class FDG_OT_RemoveCollection_Op(Operator):
    bl_idname = "fdg.remove_collection"
    bl_label = "Remove Collection"
    bl_description = "Removes the selected Collection from Selection List"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        index = scene.collection_list_index
        scene.collection_list.remove(index)
        scene.collection_list_index = min(max(0, index - 1), len(scene.collection_list) - 1)
        
        return {'FINISHED'}

class FDG_OT_AddCollections_Op(Operator):
    bl_idname = "fdg.add_collections"
    bl_label = "Add Selected"
    bl_description = "Adds the selected Character Collections to the List."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        scene = context.scene
        selected_collections = [sel for sel in context.selected_ids if sel.rna_type.name == 'Collection']
        for thing in selected_collections:
            
            
            item = scene.collection_list.add()
            item.character_collection = thing
            for window in wm.windows:
                for area in window.screen.areas:
                    area.tag_redraw()
        return {'FINISHED'}

class FDG_OT_ConformViewportRenderVisibilities_OP(Operator):
    bl_idname = "fdg.conform_visibilities"
    bl_label = "Conform Visibilities"
    bl_description = "Objects that are Hidden or disabled in the Viewport will get disabled in the Render and Objects that are visible in the Viewport will be made visible in the Render"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        wm = context.window_manager
        scene = context.scene
        for obj in scene.objects:
            if obj.hide_viewport or obj.hide_get():
                obj.hide_render = True
            else:
                obj.hide_render = False

        for collection in scene.collection.children_recursive:
            layer_children_recursive = [col for col in self.traverse_tree(context.view_layer.layer_collection)]
            view_layer_collection = next((col for col in layer_children_recursive if col.name == collection.name), None)
            if collection.hide_viewport or view_layer_collection.hide_viewport:
                collection.hide_render = True
            else:
                collection.hide_render = False

        return {'FINISHED'}

    def traverse_tree(self, t):
        yield t
        for child in t.children:
            yield from self.traverse_tree(child)

def register():
    bpy.utils.register_class(FDG_OT_GeneratePreviewOutlines_Op)
    bpy.utils.register_class(FDG_OT_RenderPreview_Op)
    bpy.utils.register_class(FDG_OT_AddCollection_Op)
    bpy.utils.register_class(FDG_OT_RemoveCollection_Op)
    bpy.utils.register_class(FDG_OT_AddCollections_Op)
    bpy.utils.register_class(FDG_OT_ActivateBooleans_OP)
    bpy.utils.register_class(FDG_OT_CreatePreviewLines_OP)
    bpy.utils.register_class(FDG_OT_DeactivateBooleans_OP)
    bpy.utils.register_class(FDG_OT_PrepareScene_OP)
    bpy.utils.register_class(FDG_OT_SaveLineFile_OP)
    bpy.utils.register_class(FDG_OT_ConformViewportRenderVisibilities_OP)

def unregister():
    bpy.utils.unregister_class(FDG_OT_ConformViewportRenderVisibilities_OP)
    bpy.utils.unregister_class(FDG_OT_AddCollections_Op)
    bpy.utils.unregister_class(FDG_OT_RemoveCollection_Op)
    bpy.utils.unregister_class(FDG_OT_AddCollection_Op)
    bpy.utils.unregister_class(FDG_OT_RenderPreview_Op)
    bpy.utils.unregister_class(FDG_OT_GeneratePreviewOutlines_Op)
    bpy.utils.unregister_class(FDG_OT_SaveLineFile_OP)
    bpy.utils.unregister_class(FDG_OT_PrepareScene_OP)
    bpy.utils.unregister_class(FDG_OT_DeactivateBooleans_OP)
    bpy.utils.unregister_class(FDG_OT_CreatePreviewLines_OP)
    bpy.utils.unregister_class(FDG_OT_ActivateBooleans_OP)