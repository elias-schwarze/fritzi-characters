from .rig_update import frt_rig_updater_op
from .rig_update import frt_rig_updater_pnl

def register():
    frt_rig_updater_pnl.register()
    frt_rig_updater_op.register()
    

def unregister():
    
    frt_rig_updater_op.unregister()
    frt_rig_updater_pnl.unregister()