from .cst_vectorLightSelector import cst_vector_light_selector_op
from .cst_vectorLightSelector import cst_vector_light_selector_pnl

def register():
    cst_vector_light_selector_op.register()
    cst_vector_light_selector_pnl.register()

def unregister():
    cst_vector_light_selector_pnl.unregister()
    cst_vector_light_selector_op.unregister()
    