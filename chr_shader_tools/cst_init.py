from .cst_vectorLightSelector import cst_vector_light_selector_op
from .cst_vectorLightSelector import cst_vector_light_selector_pnl

from .cst_createShaderController import cst_create_shader_controller_op
from .cst_createShaderController import cst_create_shader_controller_pnl

def register():
    cst_create_shader_controller_op.register()
    cst_create_shader_controller_pnl.register()
    cst_vector_light_selector_op.register()
    cst_vector_light_selector_pnl.register()

def unregister():
    cst_vector_light_selector_pnl.unregister()
    cst_vector_light_selector_op.unregister()
    cst_create_shader_controller_pnl.unregister()
    cst_create_shader_controller_op.unregister()
    