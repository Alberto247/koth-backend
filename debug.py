import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
from config import *
from Hex import Hex
from hex_types import HEX_Type
from time import time

player_colors = {None: "white", 0: "g", 1: "b", 2: "r", 3: "c", 4: "m", 5: "y", 6: "salmon", 7: "darkorange",
                 8: "lime", 9: "violet", 10: "pink", 11: "grey", 12: "royalblue", 13: "palegreen", 14: "peru", 15: "orangered"}

def timer_func(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        #print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func


def plot(map, name = None):
    coord=[]
    colors=[]
    labels=[]
    for q in range(-SIDE, SIDE+1):
        for r in range(-SIDE, SIDE+1):
            s=-(q+r)
            if(-SIDE<=s and s<=SIDE):
                p=map[(q, r, s)]
                coord.append([q, r, s])
                colors.append([player_colors[p.get_owner_ID()]])
                hex_type=p.get_point_type()
                if(hex_type==HEX_Type.FLAG):
                    labels.append([f"S {p.get_current_value()}"])
                elif(hex_type==HEX_Type.WALL):
                    colors.pop()
                    colors.append(["black"])
                    labels.append([""])
                elif(hex_type==HEX_Type.FORT):
                    labels.append([f"H {p.get_current_value()}"])
                elif(hex_type==HEX_Type.CRYPTO_CRYSTAL):
                    colors.pop()
                    colors.append(["Green"])
                    labels.append(["CC"])
                elif(hex_type==HEX_Type.WEB_CRYSTAL):
                    colors.pop()
                    colors.append(["Yellow"])
                    labels.append(["WC"])
                elif(hex_type==HEX_Type.REV_CRYSTAL):
                    colors.pop()
                    colors.append(["Blue"])
                    labels.append(["RC"])
                elif(hex_type==HEX_Type.PWN_CRYSTAL):
                    colors.pop()
                    colors.append(["Purple"])
                    labels.append(["PC"])
                elif(hex_type==HEX_Type.MISC_CRYSTAL):
                    colors.pop()
                    colors.append(["Brown"])
                    labels.append(["MC"])
                elif(hex_type==HEX_Type.UNKNOWN_EMPTY):
                    colors.pop()
                    colors.append(["grey"])
                    labels.append([""])
                elif(hex_type==HEX_Type.UNKNOWN_OBJECT):
                    colors.pop()
                    colors.append(["Purple"])
                    labels.append([""])
                else:
                    labels.append([str(p.get_current_value())])

    assert(len(labels)==len(coord))

    hcoord = [c[0] for c in coord]

    # Vertical cartersian coords
    vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) /3. for c in coord]

    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')

    # Add some coloured hexagons
    for x, y, c, l in zip(hcoord, vcoord, colors, labels):
        color = c[0].lower()  # matplotlib understands lower case words for colours
        hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3., 
                            orientation=np.radians(30), 
                            facecolor=color, alpha=0.2, edgecolor='k')
        ax.add_patch(hex)
        # Also add a text label
        ax.text(x, y+0.2, l[0], ha='center', va='center', size=10)

    # Also add scatter points in hexagon centres
    ax.scatter(hcoord, vcoord, c=[c[0].lower() for c in colors], alpha=0.5)

    if name == None:
        plt.show(block=False)
    else:
        plt.savefig(name)
        plt.close()