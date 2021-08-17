from .driver_functions import fdg_driver_functions

from .driver_gen_angles import fdg_driver_gen_angles_op
from .driver_gen_angles import fdg_driver_gen_angles_pnl

from .driver_gen_shapes import fdg_driver_gen_shapes_op
from .driver_gen_shapes import fdg_driver_gen_shapes_pnl

def register():
    fdg_driver_functions.register()

    fdg_driver_gen_angles_op.register()
    fdg_driver_gen_angles_pnl.register()

    fdg_driver_gen_shapes_op.register()
    fdg_driver_gen_shapes_pnl.register()

def unregister():
    fdg_driver_gen_shapes_pnl.unregister()
    fdg_driver_gen_shapes_op.unregister()

    fdg_driver_gen_angles_pnl.unregister()
    fdg_driver_gen_angles_op.unregister()

    fdg_driver_functions.unregister()
