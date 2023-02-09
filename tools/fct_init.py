from . import fchar_tools_op, fchar_tools_pnl

def register():
    fchar_tools_pnl.register()
    fchar_tools_op.register()

def unregister():
    fchar_tools_op.unregister()
    fchar_tools_pnl.unregister()