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
            "new_parent_name": "spine_03.x",
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
            "new_parent_name": "spine_02.x",
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

        
    ],
    "constraint_update_list":
    [
        {
            "bone_name": "fix_leg_rm.l",
            "constraints":
            [
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of Arm",
                    "target_bone_name": "leg.l",
                    "do_mirror": True
            
                },
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of Root",
                    "target_bone_name": "root",
                    "do_mirror": True
            
                }
            ]
        },
        {
            "bone_name": "c_leg_rm.l",
            "constraints":
            [
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of Arm",
                    "target_bone_name": "leg.l",
                    "do_mirror": True
            
                },
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of Root",
                    "target_bone_name": "root",
                    "do_mirror": True
            
                }
            ]
        },
        {
            "bone_name": "c_arm_rm.l",
            "constraints":
            [
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of Arm",
                    "target_bone_name": "forearm.l",
                    "do_mirror": True
            
                },
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of Root",
                    "target_bone_name": "root",
                    "do_mirror": True
            
                }
            ]
        },
        {
            "bone_name": "fix_arm_rm.l",
            "constraints":
            [
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of Arm",
                    "target_bone_name": "forearm.l",
                    "do_mirror": True
            
                },
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of Root",
                    "target_bone_name": "root",
                    "do_mirror": True
            
                }
            ]
        },
        {
            "bone_name": "c_foot_ik_2.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Constraining Overwrite",
                    "target_bone_name": "c_foot_ik.l",
                    "do_mirror": True
            
                }
            ]
        },
        {
            "bone_name": "fix_foot_ik.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms (Old Connection)",
                    "target_bone_name": "c_foot_ik.l",
                    "do_mirror": True
            
                }
            ]
        },
        {
            "bone_name": "fix_toes_ik.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms (Old Connection)",
                    "target_bone_name": "c_toes_ik.l",
                    "do_mirror": True
            
                }
            ]
        },
        {
            "bone_name": "leg_pole_root.l",
            "constraints":
            [
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of_local",
                    "target_bone_name": "c_foot_ik.l",
                    "do_mirror": True
            
                }
            ]
        },
        {
            "bone_name": "fix_leg_pole.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms (Old Connection)",
                    "target_bone_name": "c_leg_pole.l",
                    "do_mirror": True
            
                }
            ]
        },
        {
            "bone_name": "c_forearm_fk_2P.l",
            "constraints": "ALL_INVERSE",
            "do_mirror": True          
        },
        {
            "bone_name": "c_arm_fk_2P.l",
            "constraints": "ALL_INVERSE",
            "do_mirror": True
        },
        {
            "bone_name": "eyes",
            "constraints":
            [
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of",
                    "target_bone_name": "head.x",
                    "do_mirror": False
            
                }
            ]
        },
        {
            "bone_name": "c_root_settings",
            "constraints":
            [
                {
                    "constraint_type": "COPY_LOCATION",
                    "constraint_name": "Copy Location",
                    "target_bone_name": "root",
                    "do_mirror": False
            
                }
            ]
        },
        {
            "bone_name": "c_root_rm",
            "constraints":
            [
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation.002",
                    "target_bone_name": "c_pos",
                    "do_mirror": False
            
                },
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation.001",
                    "target_bone_name": "c_traj",
                    "do_mirror": False
            
                },
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation",
                    "target_bone_name": "root",
                    "do_mirror": False
            
                }
            ]
        },
        {
            "bone_name": "hand.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "rotFK",
                    "target_bone_name": "hand_fk.l",
                    "do_mirror": True
            
                }
            ]
        },
        {
            "bone_name": "root",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms Overwrite (Old Connection)",
                    "target_bone_name": "c_root_master.x",
                    "do_mirror": False
            
                }
            ]
        },
        {
            "bone_name": "c_spine_rm",
            "constraints":
            [
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation.002",
                    "target_bone_name": "c_pos",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation.001",
                    "target_bone_name": "c_traj",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation",
                    "target_bone_name": "root",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "fix_shoulder.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms Overwrite (Old Connection)",
                    "target_bone_name": "c_shoulder.l",
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "fix_leg_rm.l",
            "constraints":
            [
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of Arm",
                    "target_bone_name": "leg.l",
                    "do_mirror": True
            
                },
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of Root",
                    "target_bone_name": "root",
                    "do_mirror": True
            
                }
            ]
        },
        {
            "bone_name": "c_leg_rm.l",
            "constraints":
            [
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of Arm",
                    "target_bone_name": "leg.l",
                    "do_mirror": True
            
                },
                {
                    "constraint_type": "CHILD_OF",
                    "constraint_name": "Child Of Root",
                    "target_bone_name": "root",
                    "do_mirror": True
            
                }
            ]
        },
        {
            "bone_name": "fix_leg_fk.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms (Old Connection)",
                    "target_bone_name": "c_leg_fk.l",
                    "do_mirror": True
            
                }
            ]
            
        },
        {
            "bone_name": "toes_01.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "ik_rot",
                    "target_bone_name": "fix_toes_ik.l",
                    "do_mirror": True
            
                },
                {
                    "constraint_type": "COPY_SCALE",
                    "constraint_name": "ik_scale",
                    "target_bone_name": "fix_toes_ik.l",
                    "do_mirror": True
            
                }
            ]
            
        },
        {
            "bone_name": "fix_leg_fk.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms (Old Connection)",
                    "target_bone_name": "c_leg_fk.l",
                    "do_mirror": True
            
                }
            ]
            
        },
        {
            "bone_name": "fix_thigh_fk.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms (Old Connection)",
                    "target_bone_name": "c_thigh_fk.l",
                    "do_mirror": True
            
                }
            ]
            
        },
        {
            "bone_name": "c_arm_fk_2R.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Influence Off",
                    "target_bone_name": "arm_fk.l",
                    "do_mirror": True
            
                }
            ]
            
        },
        {
            "bone_name": "hand_fk.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms Overwrite (Old Connection)",
                    "target_bone_name": "c_hand_fk.l",
                    "do_mirror": True
            
                }
            ]
            
        },
        {
            "bone_name": "forearm_fk.overwrite.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms Overwrite (Old Connection)",
                    "target_bone_name": "c_forearm_fk.l",
                    "do_mirror": True
            
                }
            ]
            
        },
        {
            "bone_name": "fix_forearm_fk_connector.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_LOCATION",
                    "constraint_name": "Copy Location",
                    "target_bone_name": "arm_fk.l",
                    "do_mirror": True
            
                }
            ]
            
        },
        {
            "bone_name": "c_forearm_fk_2R.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Influence Off",
                    "target_bone_name": "forearm_fk.l",
                    "do_mirror": True
            
                }
            ]
            
        },
        {
            "bone_name": "fix_forearm_fk_2R.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_LOCATION",
                    "constraint_name": "Copy Location",
                    "target_bone_name": "arm_fk.l",
                    "do_mirror": True
            
                }
            ]
            
        },
        {
            "bone_name": "v_forearm_fk_2R.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_LOCATION",
                    "constraint_name": "Copy Location <- Vererbung vom Oberarm <- bei FK Test",
                    "target_bone_name": "arm_fk.l",
                    "do_mirror": True
            
                }
            ]
            
        },
        {
            "bone_name": "arm_fk.overwrite.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms Overwrite (Old Connection)",
                    "target_bone_name": "c_arm_fk.l",
                    "do_mirror": True
            
                }
            ]
            
        },
        {
            "bone_name": "leg_ik_nostr.l",
            "constraints":
            [
                {
                    "constraint_type": "IK",
                    "constraint_name": "IK",
                    "target_bone_name": "fix_leg_pole.l",
                    "do_mirror": True
                }
            ]
        }
    
    ],
    "constraint_add_list":
    [
        {
            "bone_name": "c_head.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms",
                    "target": "xxx_rig",
                    "bone": "v_head_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_head_2.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "c_head_2.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms",
                    "target": "xxx_rig",
                    "bone": "v_head.x",
                    "mix": "AFTER_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_head.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "head.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms B (Correction)",
                    "target": "xxx_rig",
                    "bone": "v_head_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms A (Mocap)",
                    "target": "xxx_rig",
                    "bone": "v_head.x",
                    "mix": "AFTER_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                }
                #,
                #{
                #    "constraint_type": "COPY_TRANSFORMS",
                #    "constraint_name": "Copy Transforms Overwrite (Old Connection)",
                #    "target": "xxx_rig",
                #    "bone": "c_head.x",
                #    "mix": "REPLACE",
                #    "target_space": "WORLD",
                #    "owner_space": "WORLD",
                #    "do_mirror": False
                #}
            ]
        },
        {
            "bone_name": "c_neck.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms",
                    "target": "xxx_rig",
                    "bone": "v_neck_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_neck_2.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "c_neck_2.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms",
                    "target": "xxx_rig",
                    "bone": "v_neck.x",
                    "mix": "AFTER_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_neck.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "neck.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms B (Correction)",
                    "target": "xxx_rig",
                    "bone": "v_neck_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms A (Mocap)",
                    "target": "xxx_rig",
                    "bone": "v_neck.x",
                    "mix": "AFTER_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                }
                #,
                #{
                #    "constraint_type": "COPY_TRANSFORMS",
                #    "constraint_name": "Copy Transforms Overwrite (Old Connection)",
                #    "target": "xxx_rig",
                #    "bone": "c_neck.x",
                #    "mix": "REPLACE",
                #    "target_space": "WORLD",
                #    "owner_space": "WORLD",
                #    "do_mirror": False
                #}
            ]
        },
        {
            "bone_name": "spine_01.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms B (Correction)",
                    "target": "xxx_rig",
                    "bone": "v_spine_01_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms A (Mocap)",
                    "target": "xxx_rig",
                    "bone": "v_spine_01.x",
                    "mix": "AFTER_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms Overwrite (Old Connection)",
                    "target": "xxx_rig",
                    "bone": "c_spine_01.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "spine_02.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms B (Correction)",
                    "target": "xxx_rig",
                    "bone": "v_spine_02_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms A (Mocap)",
                    "target": "xxx_rig",
                    "bone": "v_spine_02.x",
                    "mix": "AFTER_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms Overwrite (Old Connection)",
                    "target": "xxx_rig",
                    "bone": "c_spine_02.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "spine_03.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms B (Correction)",
                    "target": "xxx_rig",
                    "bone": "v_spine_03_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms A (Mocap)",
                    "target": "xxx_rig",
                    "bone": "v_spine_03.x",
                    "mix": "AFTER_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms Overwrite (Old Connection)",
                    "target": "xxx_rig",
                    "bone": "c_spine_03.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "spine_04.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms B (Correction)",
                    "target": "xxx_rig",
                    "bone": "v_spine_04_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms A (Mocap)",
                    "target": "xxx_rig",
                    "bone": "v_spine_04.x",
                    "mix": "AFTER_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms Overwrite (Old Connection)",
                    "target": "xxx_rig",
                    "bone": "c_spine_04.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "c_arm_fk.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_LOCATION",
                    "constraint_name": "Copy Location from Correction if \"Locking_M\" ≥ 0",
                    "target": "xxx_rig",
                    "bone": "arm_fk.l",
                    "mix": None,
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation from Correction if \"Locking_M\" ≥ 0",
                    "target": "xxx_rig",
                    "bone": "arm_fk.l",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_LOCATION",
                    "constraint_name": "Copy Location from Mocap if \"Locking_M\" < 0",
                    "target": "xxx_rig",
                    "bone": "fix_shoulder.l",
                    "mix": None,
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation from Mocap if \"Locking_M\" < 0",
                    "target": "xxx_rig",
                    "bone": "fix_shoulder.l",
                    "mix": "BEFORE",
                    "target_space": "LOCAL_WITH_PARENT",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "arm_fk.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation O1",
                    "target": "xxx_rig",
                    "bone": "v_arm_fk_2R.l",
                    "mix": "AFTER",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation O2",
                    "target": "xxx_rig",
                    "bone": "v_arm_fk_2P.l",
                    "mix": "AFTER",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation O2 (Fake-IK) muss noch",
                    "target": "xxx_rig",
                    "bone": "v_arm_fk_2P.limited.l",
                    "mix": "AFTER",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "c_forearm_fk.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_LOCATION",
                    "constraint_name": "Copy Location from Correction if \"Locking_M\" ≥ 0",
                    "target": "xxx_rig",
                    "bone": "forearm_fk.l",
                    "mix": None,
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation from Correction if \"Locking_M\" ≥ 0",
                    "target": "xxx_rig",
                    "bone": "forearm_fk.l",
                    "mix": "REPLACE",
                    "target_space": "LOCAL_WITH_PARENT",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_LOCATION",
                    "constraint_name": "Copy Location from Mocap if \"Locking_M\" < 0",
                    "target": "xxx_rig",
                    "bone": "fix_arm_fk.l",
                    "mix": None,
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation from Mocap if \"Locking_M\" < 0",
                    "target": "xxx_rig",
                    "bone": "fix_arm_fk.l",
                    "mix": "BEFORE",
                    "target_space": "LOCAL_WITH_PARENT",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "forearm_fk.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_LOCATION",
                    "constraint_name": "Copy Location <- Vererbung vom Oberarm",
                    "target": "xxx_rig",
                    "bone": "arm_fk.l",
                    "head_tail": 1.0,
                    # head_tail ist neu dazugekommen
                    "mix": None,
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation U_R",
                    "target": "xxx_rig",
                    "bone": "v_forearm_fk_2R.l",
                    "mix": "AFTER",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_ROTATION",
                    "constraint_name": "Copy Rotation U_P",
                    "target": "xxx_rig",
                    "bone": "v_forearm_fk_2P.l",
                    "mix": "AFTER",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "DAMPED_TRACK",
                    "constraint_name": "Damped Track <- bei Free Hand-Pole only!",
                    "target": "xxx_rig",
                    "bone": "c_forearm_fk_2P.l",
                    "mix": None,
                    "track_axis": "TRACK_Y",
                    # track_axis ist neu dazu gekommen
                    "target_space": None,
                    "owner_space": None,
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "c_hand_fk.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms",
                    "target": "xxx_rig",
                    "bone": "v_hand_fk_2.l",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_hand_fk_2.l",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "c_hand_fk_2.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms",
                    "target": "xxx_rig",
                    "bone": "v_hand_fk.l",
                    "mix": "AFTER_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_hand_fk.l",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "c_shoulder.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms",
                    "target": "xxx_rig",
                    "bone": "v_shoulder-2.l",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_shoulder-2.l",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "c_spine_04.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms",
                    "target": "xxx_rig",
                    "bone": "v_spine_04_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_spine_04_2.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "c_spine_03.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms",
                    "target": "xxx_rig",
                    "bone": "v_spine_03_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_spine_03_2.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "c_spine_02.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms",
                    "target": "xxx_rig",
                    "bone": "v_spine_02_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_spine_02_2.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "c_spine_01.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms",
                    "target": "xxx_rig",
                    "bone": "v_spine_01_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_spine_01_2.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "c_root_master.x",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Copy Transforms",
                    "target": "xxx_rig",
                    "bone": "v_root_master_2.x",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": False
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_root_master_2.x",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": False
                }
            ]
        },
        {
            "bone_name": "c_leg_pole.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Value (CleanUp)",
                    "target": "xxx_rig",
                    "bone": "v_leg_pole_2.l",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_leg_pole_2.l",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "c_foot_ik.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Value (CleanUp)",
                    "target": "xxx_rig",
                    "bone": "v_foot_ik_2.l",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_foot_ik_2.l",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "c_toes_ik.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Value (CleanUp)",
                    "target": "xxx_rig",
                    "bone": "v_toes_ik_2.l",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_toes_ik_2.l",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "c_thigh_fk.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Value (CleanUp)",
                    "target": "xxx_rig",
                    "bone": "v_thigh_fk_2.l",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_thigh_fk_2.l",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "c_leg_fk.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Value (CleanUp)",
                    "target": "xxx_rig",
                    "bone": "v_leg_fk_2.l",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_leg_fk_2.l",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                }
            ]
        },
        {
            "bone_name": "c_foot_fk.l",
            "constraints":
            [
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Value (CleanUp)",
                    "target": "xxx_rig",
                    "bone": "v_foot_fk_2.l",
                    "mix": "BEFORE_SPLIT",
                    "target_space": "LOCAL",
                    "owner_space": "LOCAL",
                    "do_mirror": True
                },
                {
                    "constraint_type": "COPY_TRANSFORMS",
                    "constraint_name": "Influence Off",
                    "target": "xxx_rig",
                    "bone": "v_foot_fk_2.l",
                    "mix": "REPLACE",
                    "target_space": "WORLD",
                    "owner_space": "WORLD",
                    "do_mirror": True
                }
            ]
        }
    
    ],
    "bone_visualization_list":
    [
        {
            "bone_name": "c_arm_twist_offset.l",
            "custom_object" : "cs_arrow_twist.v2",
            "scale":
            {
                "X": 4.0,
                "Y": 4.0,
                "Z": 4.0
            },
            "rot":
            {
                "Y": 180
            },
            "do_mirror": True
        },
        {
            "bone_name": "c_arm_ik.l",
            "custom_object": "cs_tube.arm",
            "scale_drv":
            {
                "X": "(var*-1+1)*1.5",
                "Y": "(var*-1+1)*0.5",
                "Z": "(var*-1+1)*1.5"
            },
            "rot":
            {
                "X": 180
            },
            "do_mirror": True

        },
        {
            "bone_name": "c_arm_fk.l",
            "custom_object": "cs_circle_arm_double",
            "scale_drv":
            {
                "X": "(var*-0.175)+1",
                "Y": "(var*-0.175)+1",
                "Z": "(var*-0.175)+1"
            },
            "rot":
            {
                "X": 180,
                "Z": 90
            },
            "clear_overwrite_transform": True,
            "do_mirror": True

        },
        {
            "bone_name": "c_forearm_fk.l",
            "custom_object": "cs_circle_arm_double",
            "scale_drv":
            {
                "X": "(var*-0.175)+1",
                "Y": "(var*-0.175)+1",
                "Z": "(var*-0.175)+1"
            },
            "loc":
            {
                "Y": 0.018
            },
            "rot":
            {
                "X": 180,
                "Z": 90
            },
            "clear_overwrite_transform": True,
            "do_mirror": True

        },
        {
            "bone_name": "c_hand_fk.l",
            "scale_drv":
            {
                "X": "(var*-0.9)+1",
                "Y": "(var*-0.9)+1",
                "Z": "(var*-0.9)+1"
            },
            "do_mirror": True

        },
        {
            "bone_name": "c_hand_fk_2.l",
            "scale_drv":
            {
                "X": "ik_fk_switch*1.0",
                "Y": "ik_fk_switch*0.75",
                "Z": "ik_fk_switch*1.0"
            },
            "bone_grp": "correction.l",
            "do_mirror": True

        },
        {
            "bone_name": "c_hand_ik.l",
            "scale_drv":
            {
                "X": "(var*-1+1)*0.9",
                "Y": "(var*-1+1)*0.9",
                "Z": "(var*-1+1)*0.9"
            },
            "do_mirror": True
        },
        {
            "bone_name": "c_hand_ik_2.l",
            "scale_drv":
            {
                "X": "(1-ik_fk_switch)*1.0",
                "Y": "(1-ik_fk_switch)*0.3",
                "Z": "(1-ik_fk_switch)*1.0"
            },
            "do_mirror": True
        },
        {
            "bone_name": "c_root_master.x",
            "scale":
            {
                "X": 0.550
            },
            "do_mirror": False
        },
        {
            "bone_name": "c_spine_fk_bend",
            "overwrite_transform": "spine_04.x",
            "do_mirror": False
        },
        {
            "bone_name": "c_root_master_2.x",
            "overwrite_transform": "c_p_root_master.x",
            "do_mirror": False
        },
        {
            "bone_name": "c_root_bend.x",
            "scale":
            {
                "X": 1.4,
                "Y": 1.4,
                "Z": 1.4
            },
            "loc":
            {
                "Y": -0.03
            },
            "do_mirror": False
        },
        {
            "bone_name": "c_root.x",
            "scale":
            {
                "X": 1.1,
                "Y": 1.1,
                "Z": 1.1
            },
            "loc":
            {
                "Y": -0.03
            },
            "do_mirror": False
        },
        {
            "bone_name": "c_spine_01_2.x",
            "overwrite_transform": "c_p_spine_01.x",
            "do_mirror": False
        },
        {
            "bone_name": "c_spine_02_2.x",
            "overwrite_transform": "c_p_spine_02.x",
            "do_mirror": False
        },
        {
            "bone_name": "c_neck.x",
            "loc":
            {
                "Y": 0.025
            },
            "clear_overwrite_transform": True,
            "do_mirror": False
        },
        {
            "bone_name": "c_neck_2.x",
            "custom_object": "cs_arrow_cross.head",
            "scale":
            {
                "X": 0.360,
                "Y": 0.360,
                "Z": 0.360
            },
            "loc":
            {
                "Y": 0.025
            },
            "rot":
            {
                "X": -90
            },
            "bone_grp": "correction.x",
            "do_mirror": False
        },
        {
            "bone_name": "c_head.x",
            "scale":
            {
                "X": 0.150,
                "Y": 0.150,
                "Z": 0.150
            },
            "loc":
            {
                "Y": 0.07
            },
            "do_mirror": False
        },
        {
            "bone_name": "c_head_2.x",
            "custom_object": "cs_arrow_cross.head",
            "scale":
            {
                "X": 0.250,
                "Y": 0.250,
                "Z": 0.250
            },
            "loc":
            {
                "Y": 0.025
            },
            "rot":
            {
                "X": -90
            },
            "bone_grp": "correction.x",
            "do_mirror": False
        },
        {
            "bone_name": "c_leg_pole.l",
            "custom_object": "cs_sphere_2",
            
            "rot":
            {
                "X": 90,
                "Y": 90
            },
            "do_mirror": True
        },
        {
            "bone_name": "c_thigh_b.l",
            "loc":
            {
                "Y": 0.03,
                "Z": 0.05
            },
            "do_mirror": True
        },
        {
            "bone_name": "c_thigh_ik.l",
            "custom_object": "cs_tube.arm",
            
            "scale_drv":
            {
                "X": "(var*-1+1)*1.5",
                "Y": "(var*-1+1)*1.5"
            },
            "rot":
            {
                "X": 180,
                "Y": -90
            },
            "do_mirror": False
        },
        {
            "bone_name": "c_thigh_ik.r",
            "custom_object": "cs_tube.arm",
            
            "scale_drv":
            {
                "X": "(var*-1+1)*1.5",
                "Y": "(var*-1+1)*1.5"
            },
            "rot":
            {
                "X": 180,
                "Y": 90
            },
            "do_mirror": False
        },
        {
            "bone_name": "c_thigh_fk.l",
            "custom_object": "cs_circle_arm_double",
            "scale_drv":
            {
                "X": "(var*-0.14)+1",
                "Y": "(var*-0.14)+1",
                "Z": "(var*-0.14)+1"
            },
            "loc":
            {
                "X": -0.007
            },
            "rot":
            {
                "X": 90,
                "Y": 90
            },
            "do_mirror": False
        },
        {
            "bone_name": "c_thigh_fk.r",
            "custom_object": "cs_circle_arm_double",
            "scale_drv":
            {
                "X": "(var*-0.14)+1",
                "Y": "(var*-0.14)+1",
                "Z": "(var*-0.14)+1"
            },
            "loc":
            {
                "X": 0.007
            },
            "rot":
            {
                "X": -90,
                "Y": 90
            },
            "do_mirror": False
        },
        {
            "bone_name": "c_leg_fk.l",
            "custom_object": "cs_circle_arm_double",
            "scale_drv":
            {
                "X": "(var*-0.1)+1",
                "Y": "(var*-0.1)+1",
                "Z": "(var*-0.1)+1"
            },
            "loc":
            {
                "X": -0.025,
                "Y": 0.038
            },
            "rot":
            {
                "X": 90,
                "Y": 90
            },
            "do_mirror": False
        },
        {
            "bone_name": "c_leg_fk.r",
            "custom_object": "cs_circle_arm_double",
            
            "scale_drv":
            {
                "X": "(var*-0.1)+1",
                "Y": "(var*-0.1)+1",
                "Z": "(var*-0.1)+1"
            },
            "loc":
            {
                "X": 0.025,
                "Y": 0.038
            },
            "rot":
            {
                "X": -90,
                "Y": 90
            },
            "do_mirror": False
        },
        {
            "bone_name": "c_foot_ik_2.l",
            "overwrite_transform": "c_p_foot_ik.l",
            "do_mirror": True
        },
        {
            "bone_name": "c_foot_fk_2.l",
            "overwrite_transform": "c_p_foot_fk.l",
            "do_mirror": True
        },
        {
            "bone_name": "c_toes_ik.l",
            "loc":
            {
                "X": 0.007,
                "Y": 0.04
            },
            "do_mirror": False
        },
        {
            "bone_name": "c_toes_ik.r",
            "loc":
            {
                "Y": 0.04
            },
            "do_mirror": False
        }      
    ]
}