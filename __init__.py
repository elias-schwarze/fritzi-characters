# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from .driver_generator import fdg_driver_gen_angles_pnl
from .driver_generator import fdg_driver_gen_angles_op
from .driver_generator.driver_functions import fdg_driver_functions


bl_info = {
    "name": "fritziCharacters",
    "author": "Michael Schieber, Sophie Fink, Elias Schwarze",
    "description": "A suite of tools for character rigging in production",
    "blender": (2, 93, 0),
    "version": (0, 0, 2),
    "location": "3D Viewport > Properties panel (N) > FCHAR Tabs",
    "warning": "Deactivate old version, then restart Blender before installing a newer version",
    "category": "Rigging"
}


def register():
    fdg_driver_functions.register()
    fdg_driver_gen_angles_op.register()
    fdg_driver_gen_angles_pnl.register()


def unregister():
    fdg_driver_gen_angles_pnl.unregister()
    fdg_driver_gen_angles_op.unregister()
    fdg_driver_functions.unregister()