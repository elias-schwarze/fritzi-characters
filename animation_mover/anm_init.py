from . import anm_mover_pnl
from . import anm_mover_op

def register():
    anm_mover_pnl.register()
    anm_mover_op.register()

def unregister():
    anm_mover_op.unregister()
    anm_mover_pnl.unregister()
