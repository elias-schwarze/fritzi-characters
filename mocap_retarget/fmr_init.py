from . import fmr_retarget_pnl
from . import fmr_retarget_op

def register():
    fmr_retarget_op.register()
    fmr_retarget_pnl.register()

def unregister():
    fmr_retarget_pnl.unregister()
    fmr_retarget_op.unregister()

