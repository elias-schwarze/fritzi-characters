# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

from . import addon_updater_ops
from . import updater_ui

from .driver_generator import fdg_init
from .retarget_tools import frt_retarget_tools_op, frt_retarget_tools_pnl
from .chr_shader_tools import cst_init
from .mocap_retarget import fmr_init
from .rig_tools import fchar_rig_tools_op, fchar_rig_tools_pnl
from .cam_rig_auto_visibility import cav_init
from .animation_mover import anm_init
from .rig_tools import frt_init
from .property_bake import FPB_init
from .tools import fct_init
from .driver_generator.utility_functions.fdg_driver_utils import add_auto_link_handler, add_load_handler, remove_load_handler
from . import fchar_alerts_ops

bl_info = {
    "name": "fritziCharacters",
    "author": "Michael Schieber, Sophie Fink, Elias Schwarze",
    "description": "A suite of tools for character rigging in production",
    "blender": (3, 3, 0),
    "version": (1, 7, 3),
    "location": "3D Viewport > Properties panel (N) > FCHAR Tabs",
    "category": "Rigging"
}

classes = (
    updater_ui.DemoPreferences,
)


def register():
    addon_updater_ops.register(bl_info)

    for cls in classes:
        addon_updater_ops.make_annotations(cls)  # Avoid blender 2.8 warnings.
        bpy.utils.register_class(cls)

    fdg_init.register()
    cst_init.register()
    fmr_init.register()
    frt_retarget_tools_op.register()
    frt_retarget_tools_pnl.register()
    fchar_rig_tools_op.register()
    fchar_rig_tools_pnl.register()
    cav_init.register()
    anm_init.register()
    frt_init.register()
    FPB_init.register()
    fct_init.register()
    fchar_alerts_ops.register()
    add_auto_link_handler()
    add_load_handler()




def unregister():
    remove_load_handler()
    fchar_alerts_ops.unregister()
    fct_init.unregister()
    FPB_init.unregister()
    frt_init.unregister()
    anm_init.unregister()
    cav_init.unregister()
    fchar_rig_tools_pnl.unregister()
    fchar_rig_tools_op.unregister()
    frt_retarget_tools_pnl.unregister()
    frt_retarget_tools_op.unregister()
    fmr_init.unregister()
    cst_init.unregister()
    fdg_init.unregister()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    addon_updater_ops.unregister()
