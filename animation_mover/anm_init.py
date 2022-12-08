from . import anm_mover_pnl
from . import anm_mover_op
from . import anm_copy_ops

def register():
    anm_mover_pnl.register()
    anm_mover_op.register()
    anm_copy_ops.register()

def unregister():
    anm_copy_ops.unregister()
    anm_mover_op.unregister()
    anm_mover_pnl.unregister()
    