from config import SIDE
from hex_types import HEX_Type


def hex_length(hex):
    return (abs(hex.q) + abs(hex.r) + abs(hex.s)) // 2


def hex_distance(a, b):
    return hex_length(hex_subtract(a, b))


def hex_add(a, b):
    return Hex((a.q + b.q, a.r + b.r, a.s + b.s))


def hex_subtract(a, b):
    return Hex((a.q - b.q, a.r - b.r, a.s - b.s))


def hex_round(q, r, s):
    qi = int(round(q))
    ri = int(round(r))
    si = int(round(s))
    q_diff = abs(qi - q)
    r_diff = abs(ri - r)
    s_diff = abs(si - s)
    if q_diff > r_diff and q_diff > s_diff:
        qi = -ri - si
    else:
        if r_diff > s_diff:
            ri = -qi - si
        else:
            si = -qi - ri
    return Hex((qi, ri, si))


def hex_midpoint(a, b):
    return Hex(((a.q + b.q)/2, (a.r + b.r)/2, (a.s + b.s)/2))


def hex_lerp(a, b, t):
    return a[0] * (1.0 - t) + b[0] * t, a[1] * (1.0 - t) + b[1] * t, a[2] * (1.0 - t) + b[2] * t


def hex_linedraw(a, b):
    N = hex_distance(a, b)
    a_nudge = (a.q + 1e-06, a.r + 1e-06, a.s - 2e-06)
    b_nudge = (b.q + 1e-06, b.r + 1e-06, b.s - 2e-06)
    results = []
    step = 1.0 / max(N, 1)
    for i in range(0, N + 1):
        q, r, s = hex_lerp(a_nudge, b_nudge, step * i)
        results.append(hex_round(q, r, s))
    return results


class Hex:

    def __init__(self, location, point_type=HEX_Type.GRASS, owner_ID=None, current_value=0):
        if location[0]+location[1]+location[2] != 0:
            raise TypeError('Invalid coordinates')
        self.q = location[0]
        self.r = location[1]
        self.s = location[2]
        self.owner_ID = owner_ID
        self.current_value = current_value
        self.point_type = point_type

    def __repr__(self):
        return f"Hex {self.get_position_tuple()}, type: {self.get_point_type().name}, owner: {self.get_owner_ID()}"

    def set_point_type(self, point_type):
        self.point_type = point_type

    def set_current_value(self, current_value):
        self.current_value = current_value

    def set_owner_ID(self, owner):
        self.owner_ID = owner

    def get_point_type(self):
        return self.point_type

    def get_current_value(self):
        return self.current_value

    def get_owner_ID(self):
        return self.owner_ID

    def get_position_tuple(self):
        return (self.q, self.r, self.s)

    def is_neighbor(self, other):
        d = []
        d.append(self.q - other.q)
        d.append(self.r - other.r)
        d.append(self.s - other.s)

        if (0 in d and 1 in d and -1 in d):
            return True

        return False

    def get_neighbors(self):
        q = self.q
        r = self.r
        s = self.s

        neighbors = [
            (q+1, r-1, s),
            (q-1, r+1, s),
            (q+1, r, s-1),
            (q-1, r, s+1),
            (q, r+1, s-1),
            (q, r-1, s+1)
        ]
        to_remove = []
        for n in neighbors:
            if (abs(n[0]) > SIDE) or (abs(n[1]) > SIDE) or (abs(n[2]) > SIDE):
                to_remove.append(n)
        for x in to_remove:
            neighbors.remove(x)

        return neighbors

    def serializable(self):
        return (self.get_position_tuple(), self.get_point_type(),
                self.get_owner_ID(), self.get_current_value())
