from . import fmr_retarget_pnl
from . import fmr_retarget_op
from . import fmr_scale_list_op

def register():
    fmr_retarget_op.register()
    fmr_retarget_pnl.register()
    fmr_scale_list_op.register()
    
def unregister():
    fmr_scale_list_op.unregister()
    fmr_retarget_pnl.unregister()
    fmr_retarget_op.unregister()

