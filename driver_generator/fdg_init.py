from .driver_functions import fdg_driver_functions

from .driver_gen_angles import fdg_driver_gen_angles_op
from .driver_gen_angles import fdg_driver_gen_angles_pnl
from .driver_gen_angles import fdg_driver_gen_angles_remove_op

from .driver_gen_shapes import fdg_driver_gen_shapes_op
from .driver_gen_shapes import fdg_driver_gen_shapes_pnl
from .driver_gen_shapes import fdg_driver_gen_shapes_remove_op

from .driver_gen_camera import fdg_driver_gen_camera_op
from .driver_gen_camera import fdg_driver_gen_camera_pnl
from . import fdg_driver_gen_pnl

from .driver_gen_outlines import fdg_driver_gen_outlines_ops
from .driver_gen_outlines import fdg_driver_gen_outlines_pnl

def register():
    fdg_driver_gen_pnl.register()

    fdg_driver_functions.register()

    fdg_driver_gen_angles_op.register()
    fdg_driver_gen_angles_remove_op.register()
    fdg_driver_gen_angles_pnl.register()

    fdg_driver_gen_shapes_op.register()
    fdg_driver_gen_shapes_remove_op.register()
    fdg_driver_gen_shapes_pnl.register()

    fdg_driver_gen_outlines_ops.register()
    fdg_driver_gen_outlines_pnl.register()

    fdg_driver_gen_camera_op.register()
    fdg_driver_gen_camera_pnl.register()

def unregister():
    fdg_driver_gen_camera_pnl.unregister()
    fdg_driver_gen_camera_op.unregister()

    fdg_driver_gen_outlines_pnl.unregister()
    fdg_driver_gen_outlines_ops.unregister()

    fdg_driver_gen_shapes_pnl.unregister()
    fdg_driver_gen_shapes_remove_op.unregister()
    fdg_driver_gen_shapes_op.unregister()

    fdg_driver_gen_angles_pnl.unregister()
    fdg_driver_gen_angles_remove_op.unregister()
    fdg_driver_gen_angles_op.unregister()

    fdg_driver_functions.unregister()

    fdg_driver_gen_pnl.unregister()