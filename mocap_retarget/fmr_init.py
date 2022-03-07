from . import fmr_retarget_pnl
from . import fmr_retarget_op
from . import fmr_settings

def register():
    fmr_retarget_op.register()
    fmr_retarget_pnl.register()
    #fmr_settings.load_settings()

def unregister():
    #fmr_settings.write_settings()
    fmr_retarget_pnl.unregister()
    fmr_retarget_op.unregister()

