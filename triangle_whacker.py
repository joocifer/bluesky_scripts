#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from matplotlib.patches import FancyBboxPatch
import math
from shapely.geometry import Polygon

# 0. Dark-navy background + white text/grid
plt.style.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': '#001f3f',
    'axes.facecolor':   '#001f3f',
    'axes.edgecolor':   'white',
    'xtick.color':      'white',
    'ytick.color':      'white',
    'text.color':       'white',
    'grid.color':       'gray',
    'grid.linestyle':   '--'
})

# 1. Parse initial degrees from CLI
if len(sys.argv) > 1:
    try:
        init_deg = float(sys.argv[1])
    except ValueError:
        init_deg = 0.0
else:
    init_deg = 0.0

# 2. Original triangle & centroid
orig_verts = np.array([[-2, -1], [-2, 1], [0, 0]])
centroid   = orig_verts.mean(axis=0)
dx         = 4.0    # horizontal offset for rotated copy

# 3. Rotation angles (radians)
angle_orig = 0.0
angle_rel  = math.radians(init_deg)

# 4. Scale for real units (10 cm side ↔ plot units)
side_units = np.linalg.norm(orig_verts[0] - orig_verts[1])
scale_cm   = 10.0 / side_units

# 5. Rotate helper
def rotate(verts, pivot, theta):
    v = verts - pivot
    c, s = math.cos(theta), math.sin(theta)
    M    = np.array([[c, -s], [s,  c]])
    return (M @ v.T).T + pivot

# 6. Compute bounds so both triangles always fit
pivot_r = centroid + [dx, 0]
verts_o = rotate(orig_verts, centroid, angle_orig)
verts_r = rotate(rotate(orig_verts, centroid, angle_orig),
                 pivot_r, angle_rel)
all_verts  = np.vstack([verts_o, verts_r])
xmin, ymin = all_verts.min(axis=0) - 0.5
xmax, ymax = all_verts.max(axis=0) + 0.5

# 7. Figure & subplots layout
fig = plt.figure(figsize=(10, 6))
# set window title
try:
    fig.canvas.manager.set_window_title(f"Triangle Whacker ({init_deg:.1f})")
except Exception:
    pass

gs  = fig.add_gridspec(2, 2,
    width_ratios=[2,1], height_ratios=[5,1],
    wspace=0.3, hspace=0.3)

ax_tri  = fig.add_subplot(gs[0,0])
ax_tri.set_aspect('equal')
ax_tri.grid(True)
ax_tri.set_xlim(xmin, xmax)
ax_tri.set_ylim(ymin, ymax)

ax_code = fig.add_subplot(gs[0,1])
ax_code.axis('off')

ax_tri.set_title("Drag triangles or type degrees below")

# 8. Degrees_in text box (white label, black input, light grey bg, narrow)
ax_txt = fig.add_subplot(gs[1,0])
ax_txt.patch.set_facecolor('lightgrey')
text_box = TextBox(ax_txt, "Degrees_in", f"{init_deg:.1f}")
text_box.label.set_color('white')
text_box.text_disp.set_color('black')
# shrink the input box width
pos = text_box.ax.get_position()
text_box.ax.set_position([pos.x0, pos.y0, pos.width * 0.4, pos.height])

# 9. Reset button (smaller, darker-blue bg, yellow text)
ax_btn = fig.add_subplot(gs[1,1])
ax_btn.patch.set_alpha(0.0)
reset_btn = Button(
    ax_btn,
    "Reset Original",
    color='darkblue',
    hovercolor='#0000cd'
)
# rounded edges
btn_box = FancyBboxPatch(
    (0,0), 1, 1,
    boxstyle="round,pad=0.2",
    transform=reset_btn.ax.transAxes,
    facecolor='darkblue',
    edgecolor='none'
)
reset_btn.ax.add_patch(btn_box)
reset_btn.label.set_color('yellow')
# shrink button
bpos = reset_btn.ax.get_position()
reset_btn.ax.set_position([bpos.x0, bpos.y0, bpos.width * 0.6, bpos.height])

# 10. Initial triangles & matrix text (yellow)
patch_o = plt.Polygon(verts_o, facecolor='C0',
                      alpha=0.5, edgecolor='white')
patch_r = plt.Polygon(verts_r, facecolor='C1',
                      alpha=0.5, edgecolor='white')
orig_txt = ax_tri.text(
    *centroid, "", ha='center', va='center',
    fontsize=10, family='monospace', color='yellow'
)
rot_txt  = ax_tri.text(
    0, 0, "", ha='center', va='center',
    fontsize=10, family='monospace', color='yellow'
)
ax_tri.add_patch(patch_o)
ax_tri.add_patch(patch_r)

# 11. Interaction state
dragging, press_info = None, {}

def update_display():
    # update window title with current degrees_in
    deg_window = angle_rel * 180/math.pi
    try:
        fig.canvas.manager.set_window_title(f"Triangle Whacker ({deg_window:.1f})")
    except Exception:
        pass

    # original triangle + matrix
    new_o = rotate(orig_verts, centroid, angle_orig)
    patch_o.set_xy(new_o)
    c_o, s_o = math.cos(angle_orig), math.sin(angle_orig)
    orig_txt.set_text(f"[[{c_o:.2f}, {-s_o:.2f}],\n [{s_o:.2f}, {c_o:.2f}]]")

    # rotated triangle + matrix
    temp_r = rotate(orig_verts, centroid, angle_orig)
    new_r  = rotate(temp_r, pivot_r, angle_rel)
    patch_r.set_xy(new_r)
    ctr_r = new_r.mean(axis=0)
    c_r, s_r = math.cos(angle_rel), math.sin(angle_rel)
    rot_txt.set_position(ctr_r)
    rot_txt.set_text(f"[[{c_r:.2f}, {-s_r:.2f}],\n [{s_r:.2f}, {c_r:.2f}]]")

    # rotation code snippet
    deg  = angle_rel * 180/math.pi
    rad  = math.radians(deg)
    c_rs, s_rs = math.cos(rad), math.sin(rad)
    snippet_rot = (
        f"degrees_in = {deg:.1f}\n"
        f"rads       = {rad:.3f}\n\n"
        f"cos(rads)  = {c_rs:.3f}\n"
        f"sin(rads)  = {s_rs:.3f}\n\n"
        f"matrix = [[{c_rs:.3f}, {-s_rs:.3f}],\n"
        f"          [{s_rs:.3f}, { c_rs:.3f}]]"
    )

    # collision detection + info
    poly_o = Polygon(new_o)
    poly_r = Polygon(new_r)
    inter  = poly_o.intersection(poly_r)
    coll   = not inter.is_empty
    area_u = inter.area if coll else 0.0
    area_cm= area_u * (scale_cm**2)
    if coll:
        bbox_vals = tuple(f"{v:.2f}" for v in inter.bounds)
        cent_xy   = inter.centroid.coords[0]
        cent_str  = f"({cent_xy[0]:.2f}, {cent_xy[1]:.2f})"
    else:
        bbox_vals, cent_str = "N/A", "N/A"

    snippet_coll = (
        f"# Collision  = {coll}\n"
        f"area_units² = {area_u:.3f}\n"
        f"area_cm²    = {area_cm:.1f}\n"
        f"bbox        = {bbox_vals}\n"
        f"centroid    = {cent_str}"
    )

    ax_code.clear(); ax_code.axis('off')
    ax_code.text(0, 1, snippet_rot,
                 family='monospace', va='top', color='white')
    color_coll = 'red' if coll else 'black'
    ax_code.text(0, 0.35, snippet_coll,
                 family='monospace', va='top', color=color_coll)

    fig.canvas.draw_idle()

def on_press(event):
    global dragging, press_info
    if event.inaxes != ax_tri: return
    ho, _ = patch_o.contains(event)
    hr, _ = patch_r.contains(event)
    if ho:
        dragging = 'orig'
        t0 = math.atan2(event.ydata-centroid[1],
                        event.xdata-centroid[0])
        press_info = {'t0': t0, 'a0': angle_orig}
    elif hr:
        dragging = 'rot'
        t0 = math.atan2(event.ydata-pivot_r[1],
                        event.xdata-pivot_r[0])
        press_info = {'t0': t0, 'a0': angle_rel}
    else:
        dragging = None

def on_motion(event):
    global angle_orig, angle_rel
    if dragging is None or event.inaxes != ax_tri: return
    base = centroid if dragging=='orig' else pivot_r
    θ    = math.atan2(event.ydata-base[1],
                      event.xdata-base[0])
    if dragging == 'orig':
        angle_orig = press_info['a0'] + (θ - press_info['t0'])
    else:
        angle_rel  = press_info['a0'] + (θ - press_info['t0'])
        text_box.set_val(f"{angle_rel*180/math.pi:.1f}")
    update_display()

def on_release(event):
    global dragging
    dragging = None

def on_text_submit(txt):
    global angle_rel
    try:
        angle_rel = math.radians(float(txt))
    except ValueError:
        return
    update_display()

def on_reset(event):
    global angle_orig
    angle_orig = 0.0
    update_display()

# 12. Connect callbacks & show
fig.canvas.mpl_connect('button_press_event',   on_press)
fig.canvas.mpl_connect('motion_notify_event',  on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)
text_box.on_submit(on_text_submit)
reset_btn.on_clicked(on_reset)

update_display()
plt.show()
