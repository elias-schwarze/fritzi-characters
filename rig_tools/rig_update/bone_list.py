bone_list = {
    "bone_list": [
        {
            "new_parent_name": "foot_ik_root.l",
            "children_list": [
                "c_foot_ik.l"
            ],
            "old_parent_name": None,
            "do_mirror": True
        },
        {
            "new_parent_name": "fix_foot_ik.l",
            "children_list": [
                "c_p_foot_ik.l",
                "foot_ik.l",
                "c_foot_roll.l",
                "c_toes_pivot.l"
            ],
            "old_parent_name": None,
            "do_mirror": True
        },
        {
            "new_parent_name": "c_toes_end.l",
            "children_list": [
                "c_toes_ik_2.l",
                "v_toes_ik.l",
                "v_toes_ik_2.l",
                "fix_toes_ik.l",
                "freeze_toes_ik.l"
            ],
            "old_parent_name": None,
            "do_mirror": True
        },
        {
            "new_parent_name": "leg_pole_root.l",
            "children_list": [
                "c_leg_pole.l"
            ],
            "old_parent_name": None,
            "do_mirror": True
        },
        {
            "new_parent_name": "c_traj",
            "children_list": [
                "fix_traj",
                "c_root_settings"
            ],
            "old_parent_name": None,
            "do_mirror": False
        },
        {
            "new_parent_name": "fix_traj",
            "children_list": [
                "c_root_master.x",
                "head_scale_fix.x",
                "leg_stretch.l",
                "leg_stretch.r",
                "thigh_stretch.l",
                "thigh_stretch.r",
                "arm_stretch.l",
                "arm_stretch.r",
                "forearm_stretch.l",
                "forearm_stretch.r",
                "forearm.l",
                "forearm.r"
            ],
            "old_parent_name": "c_traj",
            "do_mirror": False
        },
        {
            "new_parent_name": "forearm.l",
            "children_list": [
                "ref_forearm_fk_pole.l",
                "c_arm_settings.l"
            ],
            "old_parent_name": "c_traj",
            "do_mirror": True
        },
        {
            "new_parent_name": "hand.l",
            "children_list": [
                "hand_grasp.l"
            ],
            "old_parent_name": "c_traj",
            "do_mirror": True
        },
        {
            "new_parent_name": "head_scale_fix.x",
            "children_list": [
                "v_head.x",
                "v_head_2.x",
                "freeze_head.x",
                "ref_head.x"
            ],
            "old_parent_name": "fix_traj",
            "do_mirror": False
        },
        {
            "new_parent_name": "head_scale_fix.x",
            "children_list": [
                "c_head_2.x"
            ],
            "old_parent_name": "c_head.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "head_scale_fix.x",
            "children_list": [
                "head.x"
            ],
            "old_parent_name": "c_head_2.x",
            "do_mirror": False
        },
        
        #This one is special
        {
            "new_parent_name": "head.x",
            "children_list": "*",
            "old_parent_name": "c_head_2.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "PAK_root_master.x",
            "children_list": [
                "c_root_master.x"
            ],
            "old_parent_name": "fix_traj",
            "do_mirror": False
        },
        {
            "new_parent_name": "root",
            "children_list": [
                "fix_spine_01.x",
                "c_spine_settings"
            ],
            "old_parent_name": "PAK_root_master.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "root",
            "children_list": [
                "c_root.x",
                "c_p_root_master.x"
            ],
            "old_parent_name": "c_root_master.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "fix_spine_01.x",
            "children_list": [
                "c_spine_01.x"
            ],
            "old_parent_name": "c_root_master.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "c_thigh_b.l",
            "children_list": [
                "c_thigh_fk_2.l",
                "v_thigh_fk.l",
                "v_thigh_fk_2.l",
                "freeze_thigh_fk.l",
                "fix_thigh_fk.l"
            ],
            "old_parent_name": "PAK_root_master.x",
            "do_mirror": True
        },
        {
            "new_parent_name": "fix_thigh_fk.l",
            "children_list": [
                "thigh_fk.l",
                "c_leg_fk.l"
            ],
            "old_parent_name": "c_thigh_fk.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "fix_leg_fk.l",
            "children_list": [
                "leg_fk.l",
                "c_foot_fk_scale_fix.l",
                "leg_fk_pre_pole.l"
            ],
            "old_parent_name": "c_leg_fk.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "c_foot_fk_scale_fix.l",
            "children_list": [
                "c_foot_fk_2.l",
                "v_foot_fk.l",
                "v_foot_fk_2.l",
                "fix_foot_fk.l",
                "freeze_foot_fk.l"
            ],
            "old_parent_name": "fix_leg_fk.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "fix_foot_fk.l",
            "children_list": [
                "foot_fk.l",
                "c_p_foot_fk.l"
            ],
            "old_parent_name": "c_foot_fk.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "leg.l",
            "children_list": [
                "c_leg_settings.l"
            ],
            "old_parent_name": "PAK_root_master.x",
            "do_mirror": True
        },
        {
            "new_parent_name": "fix_spine_01.x",
            "children_list": [
                "spine_01.x"
            ],
            "old_parent_name": "c_spine_01.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "spine_01.x",
            "children_list": [
                "fix_spine_02.x"
            ],
            "old_parent_name": "fix_spine_01.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "fix_spine_02.x",
            "children_list": [
                "c_spine_02.x"
            ],
            "old_parent_name": "c_spine_01.x",
            "do_mirror": False
        },

        #This one is special too
        {
            "new_parent_name": "spine_04.x",
            "children_list": "*",
            "old_parent_name": "c_spine_04.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "arm.l",
            "children_list": [
                "ref_arm_fk_pole.l"
            ],
            "old_parent_name": "fix_shoulder.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "c_hand_fk_scale_fix.l",
            "children_list": [
                "hand_fk.l",
                "v_hand_fk.l",
                "v_hand_fk_2.l"
            ],
            "old_parent_name": "forearm_fk.overwrite.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "c_hand_fk_scale_fix.l",
            "children_list": [
                "c_hand_fk_2.l"
            ],
            "old_parent_name": "c_hand_fk.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "forearm_fk.overwrite.l",
            "children_list": [
                "c_hand_fk_scale_fix.l"
            ],
            "old_parent_name": "forearm_fk.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "forearm_fk.l",
            "children_list": [
                "forearm_fk.overwrite.l"
            ],
            "old_parent_name": "fix_forearm_fk_2R_corr.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "fix_forearm_fk_2R_corr.l",
            "children_list": [
                "forearm_fk.l"
            ],
            "old_parent_name": "c_forearm_fk.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "arm_fk.overwrite.l",
            "children_list": [
                "c_forearm_fk.l"
            ],
            "old_parent_name": "c_arm_fk.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "arm_fk.l",
            "children_list": [
                "arm_fk.overwrite.l",
                "fix_forearm_fk_2P2.l",
                "fix_arm_fk_2P2.l"
            ],
            "old_parent_name": "fix_arm_fk.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "fix_arm_fk.l",
            "children_list": [
                "arm_fk.l"
            ],
            "old_parent_name": "c_arm_fk.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "fix_shoulder.l",
            "children_list": [
                "arm_ik.l",
                "shoulder.l",
                "arm.l",
                "arm_ik_nostr_scale_fix.l",
                "arm_twist.l",
                "c_arm_ik.l"
            ],
            "old_parent_name": "c_shoulder.l",
            "do_mirror": True
        },
        {
            "new_parent_name": "neck.x",
            "children_list": [
                "c_p_neck.x"
            ],
            "old_parent_name": "c_neck_2.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "spine_04.x",
            "children_list": [
                "neck.x"
            ],
            "old_parent_name": "c_neck_2.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "spine_04.x",
            "children_list": [
                "c_neck_2.x"
            ],
            "old_parent_name": "c_neck.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "spine_04.x",
            "children_list": [
                "fix_shoulder.l",
                "fix_arm_fk.l",
                "v_neck.x",
                "v_neck_2.x",
                "v_shoulder.l",
                "v_shoulder-2.l",
                "c_shoulder_2.l",
                "fix_shoulder.r",
                "fix_arm_fk.r",
                "v_shoulder.r",
                "v_shoulder-2.r",
                "c_shoulder_2.r",
                "freeze_shoulder.l",
                "freeze_arm_fk.l",
                "freeze_shoulder.r",
                "freeze_arm_fk.r",
                "freeze_neck.x"
            ],
            "old_parent_name": "fix_spine_04.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "fix_spine_04.x",
            "children_list": [
                "spine_04.x"
            ],
            "old_parent_name": "c_spine_04.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "fix_spine_04.x",
            "children_list": [
                "c_spine_04.x"
            ],
            "old_parent_name": "c_spine_03.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "spine_03",
            "children_list": [
                "fix_spine_04.x"
            ],
            "old_parent_name": "fix_spine_03.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "fix_spine_03.x",
            "children_list": [
                "spine_03.x"
            ],
            "old_parent_name": "c_spine_03.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "fix_spine_03.x",
            "children_list": [
                "c_spine_03.x"
            ],
            "old_parent_name": "c_spine_02.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "spine_02.x",
            "children_list": [
                "c_p_neck_01.x",
                "c_p_spine_02.x"
            ],
            "old_parent_name": "c_spine_02.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "spine_02",
            "children_list": [
                "fix_spine_03.x"
            ],
            "old_parent_name": "fix_spine_02.x",
            "do_mirror": False
        },
        {
            "new_parent_name": "fix_spine_02.x",
            "children_list": [
                "spine_02.x"
            ],
            "old_parent_name": "c_spine_02.x",
            "do_mirror": False
        }
        
    ]
}