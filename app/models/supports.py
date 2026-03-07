"""Beam support types and DOF mapping."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel


class SupportType(StrEnum):
    """Boundary condition at a beam end (2D in-plane)."""

    FREE = "free"
    PINNED = "pinned"
    ROLLER_X = "roller_x"
    ROLLER_Y = "roller_y"
    FIXED = "fixed"


class SupportDof(BaseModel):
    """Degrees of freedom restraints at a support node."""

    dx: bool = False
    """Translation along X (beam axis)"""
    dy: bool = False
    """Translation along Y (vertical)"""
    dz: bool = True
    """Translation along Z (out-of-plane, always restrained for 2D)"""
    rx: bool = True
    """Rotation about X (out-of-plane, always restrained for 2D)"""
    ry: bool = True
    """Rotation about Y (out-of-plane, always restrained for 2D)"""
    rz: bool = False
    """Rotation about Z (in-plane rotation)"""

    def as_tuple(self) -> tuple[bool, bool, bool, bool, bool, bool]:
        """Return Pynite-compatible DOF tuple (DX, DY, DZ, RX, RY, RZ)."""
        return (self.dx, self.dy, self.dz, self.rx, self.ry, self.rz)


# 2D in-plane: DZ, RX, RY always restrained
_2D = dict(dz=True, rx=True, ry=True)

_SUPPORT_DOFS: dict[SupportType, SupportDof] = {
    SupportType.FREE: SupportDof(**_2D),
    SupportType.PINNED: SupportDof(dx=True, dy=True, **_2D),
    SupportType.ROLLER_X: SupportDof(dy=True, **_2D),
    SupportType.ROLLER_Y: SupportDof(dx=True, **_2D),
    SupportType.FIXED: SupportDof(dx=True, dy=True, rz=True, **_2D),
}


def support_dofs(st: SupportType) -> SupportDof:
    """Convert SupportType to its DOF restraints."""
    return _SUPPORT_DOFS[st]
