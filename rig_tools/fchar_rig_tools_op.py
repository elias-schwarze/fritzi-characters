import bpy
from bpy.types import Operator

class FCHAR_OT_CreateSpineMaster_OP(Operator):
    bl_idname = "armature.create_spine_master"
    bl_label = "Create spine master"
    bl_description = "Creates a master bone to control the entire spine"
    bl_options = {"REGISTER", "UNDO"}

    # should only work in object mode
    @classmethod
    def poll(cls, context):

        if not bpy.context.object:
            return False

        obj = bpy.context.object
        if obj:
            if obj.mode == "OBJECT":
                return True

        return False

    def execute(self, context):
        
        # custom shape creation

        verts = [(1.1303999423980713, 0.1547279953956604, -0.13347600400447845), (1.1210072040557861, 0.15472817420959473, -0.2768296003341675), (1.0929802656173706, 0.15472817420959473, -0.41773033142089844), (1.0468016862869263, 0.15472817420959473, -0.5537672638893127), (0.9832625389099121, 0.15384173393249512, -0.6826573610305786), (0.9034484624862671, 0.12809038162231445, -0.8033981323242188), (0.8087260723114014, 0.07397103309631348, -0.914121150970459), (0.7007160782814026, 0.0012869834899902344, -1.0124871730804443), (0.5812661051750183, -0.08016180992126465, -1.0963842868804932), (0.45242050290107727, -0.16057252883911133, -1.1639546155929565), (0.31638363003730774, -0.23014426231384277, -1.2136205434799194), (0.17548291385173798, -0.27907490730285645, -1.2440999746322632), (0.03212952986359596, -0.2975635528564453, -1.2544227838516235), (-0.11122384667396545, -0.27907490730285645, -1.2440999746322632), (-0.252124547958374, -0.23014426231384277, -1.2136204242706299), (-0.38816142082214355, -0.16057252883911133, -1.163954496383667), (-0.5170074105262756, -0.08016180992126465, -1.096384048461914), (-0.636457085609436, 0.0012865066528320312, -1.0124871730804443), (-0.74446702003479, 0.07397103309631348, -0.9141212701797485), (-0.8391894698143005, 0.12809038162231445, -0.8033981323242188), (-0.9190031290054321, 0.15384173393249512, -0.6826575994491577), (-0.9825426936149597, 0.15472817420959473, -0.5537673830986023), (-1.0287212133407593, 0.15472817420959473, -0.4177304208278656), (-1.0567479133605957, 0.15472817420959473, -0.27682948112487793), (-1.0661439895629883, 0.15472817420959473, -0.133476123213768), (-1.0567481517791748, 0.15472817420959473, 0.00987716019153595), (-1.0287212133407593, 0.15472817420959473, 0.15077799558639526), (-0.9825425744056702, 0.15472817420959473, 0.28681468963623047), (-0.9190031290054321, 0.15384173393249512, 0.4156160056591034), (-0.8391894698143005, 0.12809038162231445, 0.5337749719619751), (-0.7444671392440796, 0.07397103309631348, 0.6390721797943115), (-0.6364571452140808, 0.0012869834899902344, 0.7301508188247681), (-0.5170069932937622, -0.08016180992126465, 0.8058822154998779), (-0.3881615400314331, -0.16057252883911133, 0.8653900623321533), (-0.252124547958374, -0.23014426231384277, 0.9080815315246582), (-0.11122409999370575, -0.27907490730285645, 0.9336552619934082), (0.03212953358888626, -0.2975633144378662, 0.9421242475509644), (0.17548315227031708, -0.27907490730285645, 0.9336552619934082), (0.31638363003730774, -0.23014426231384277, 0.9080815315246582), (0.4524206817150116, -0.16057205200195312, 0.8653900623321533), (0.5812661051750183, -0.08016180992126465, 0.8058822154998779), (0.7007163166999817, 0.0012869834899902344, 0.7301508188247681), (0.8087260723114014, 0.07397103309631348, 0.6390721797943115), (0.9034485816955566, 0.12809038162231445, 0.5337749719619751), (0.983262300491333, 0.15384173393249512, 0.41561636328697205), (1.0468019247055054, 0.15472817420959473, 0.28681468963623047), (1.0929802656173706, 0.15472817420959473, 0.1507776379585266), (1.121006965637207, 0.15472817420959473, 0.00987716019153595)]
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 24), (24, 25),
                (25, 26), (26, 27), (27, 28), (28, 29), (29, 30), (30, 31), (31, 32), (32, 33), (33, 34), (34, 35), (35, 36), (36, 37), (37, 38), (38, 39), (39, 40), (40, 41), (41, 42), (42, 43), (43, 44), (44, 45), (45, 46), (46, 47), (47, 0)]
        mesh = bpy.data.meshes.new(('cs_spine_master'))
        mesh.from_pydata(verts, edges, [])
        mesh.update()

        spine_ctrl = bpy.data.objects.new('cs_spine_master', mesh)
        bpy.context.collection.objects.link(spine_ctrl)

        arm_name = bpy.context.selected_objects[0].name
        arm = bpy.context.selected_objects[0]

        bpy.ops.object.editmode_toggle()

        ### create Spine Master Bone

        bpy.ops.armature.select_all(action='DESELECT')

        bone = bpy.data.objects[arm_name].data.edit_bones["c_spine_04.x"]
        bpy.data.objects[arm_name].data.edit_bones.active = bone
        arm.data.edit_bones.active.select_head = True
        arm.data.edit_bones.active.select_tail = True

        bpy.ops.armature.duplicate_move()
        bpy.data.objects[arm_name].data.edit_bones["c_spine_04.x.001"].name = "c_spine_fk_bend"

        ###create parent relations for c_spine_fk_bend

        bpy.data.objects[arm_name].data.edit_bones["c_spine_fk_bend"].parent = bpy.data.objects[arm_name].data.edit_bones["c_root_master.x"]


        ###change to pose mode
        bpy.ops.object.posemode_toggle()

        ##c_spine_04.x constraint

        def createTransformConst(bone):
            
            transformConstraint =bpy.data.objects[arm_name].pose.bones[bone].constraints.new('TRANSFORM')

            transformConstraint.target = arm
            transformConstraint.subtarget = "c_spine_fk_bend"

            transformConstraint.target_space = "LOCAL"
            transformConstraint.owner_space = "LOCAL"

            transformConstraint.influence = 0.4
            
            transformConstraint.map_from = "ROTATION"

            transformConstraint.from_min_x_rot = -180
            transformConstraint.from_max_x_rot = 180

            transformConstraint.from_min_y_rot = -180
            transformConstraint.from_max_y_rot = 180

            transformConstraint.from_min_z_rot = -180
            transformConstraint.from_max_z_rot = 180


            transformConstraint.map_to = "ROTATION"

            transformConstraint.to_min_x_rot = -150
            transformConstraint.to_max_x_rot = 150

            transformConstraint.to_min_y_rot = -150
            transformConstraint.to_max_y_rot = 150

            transformConstraint.to_min_z_rot = -150
            transformConstraint.to_max_z_rot = 150 
            
        createTransformConst("c_spine_04.x")
        createTransformConst("c_spine_03.x")
        createTransformConst("c_spine_02.x")
        createTransformConst("c_spine_01.x")

        #lock location c_spine_fk_bend and custom shape scale

        bpy.context.object.pose.bones["c_spine_fk_bend"].lock_location[0] = True
        bpy.context.object.pose.bones["c_spine_fk_bend"].lock_location[1] = True
        bpy.context.object.pose.bones["c_spine_fk_bend"].lock_location[2] = True

        bpy.context.object.pose.bones["c_spine_fk_bend"].custom_shape = bpy.data.objects["cs_spine_master"]

        bpy.data.objects[arm_name].pose.bones["c_spine_fk_bend"].custom_shape_scale_xyz[0] = 2.0
        bpy.data.objects[arm_name].pose.bones["c_spine_fk_bend"].custom_shape_scale_xyz[1] = 2.0
        bpy.data.objects[arm_name].pose.bones["c_spine_fk_bend"].custom_shape_scale_xyz[2] = 1.5

        bpy.context.object.pose.bones["c_spine_fk_bend"].custom_shape_transform = bpy.data.objects[arm_name].pose.bones["spine_04.x"]

        return {'FINISHED'}




def register():
    bpy.utils.register_class(FCHAR_OT_CreateSpineMaster_OP)

def unregister():
    bpy.utils.unregister_class(FCHAR_OT_CreateSpineMaster_OP)