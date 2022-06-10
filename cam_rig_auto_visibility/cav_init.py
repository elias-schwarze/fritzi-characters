from . import cav_frame_handler_op, cav_frame_handler_pnl
def register():
    cav_frame_handler_op.register()
    cav_frame_handler_pnl.register()
def unregister():
    cav_frame_handler_pnl.unregister()
    cav_frame_handler_op.unregister()
    