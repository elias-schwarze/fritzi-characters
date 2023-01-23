from . import FPB_property_bake_op, FPB_property_bake_pnl

def register():
    FPB_property_bake_op.register()
    FPB_property_bake_pnl.register()

def unregister():
    FPB_property_bake_pnl.unregister()
    FPB_property_bake_op.unregister()