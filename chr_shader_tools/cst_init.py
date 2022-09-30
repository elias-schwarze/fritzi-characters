from .cst_ShaderController import cst_create_light_empty_op
from .cst_ShaderController import cst_vector_light_selector_op

from .cst_ShaderController import cst_create_shader_controller_op
from .cst_ShaderController import cst_select_shader_controller_op
from .cst_ShaderController import cst_remove_props_op
from .cst_ShaderController import cst_shader_controller_pnl

from .cst_shading_toolbox import cst_shading_tools_pnl
from .cst_shading_toolbox import cst_shading_tools_ops

def register():
    cst_create_shader_controller_op.register()
    cst_select_shader_controller_op.register()
    cst_remove_props_op.register()
    cst_shader_controller_pnl.register()
    cst_create_light_empty_op.register()
    cst_vector_light_selector_op.register()
    cst_shading_tools_ops.register()
    cst_shading_tools_pnl.register()

def unregister():
    cst_shading_tools_pnl.unregister()
    cst_shading_tools_ops.unregister()
    cst_vector_light_selector_op.unregister()
    cst_create_light_empty_op.unregister()
    cst_shader_controller_pnl.unregister()
    cst_remove_props_op.unregister()
    cst_select_shader_controller_op.unregister()
    cst_create_shader_controller_op.unregister()
    