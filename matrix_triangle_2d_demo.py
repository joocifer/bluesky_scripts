#!/usr/bin/python3

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

def rotation_matrix(angle_deg):
    """Return the 2×2 rotation matrix for angle_deg."""
    theta = np.deg2rad(angle_deg)
    return np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

def rotate(points, angle_deg, origin):
    """Rotate Nx2 points by angle_deg around origin."""
    R = rotation_matrix(angle_deg)
    return (points - origin) @ R.T + origin

def format_matrix(M):
    """Format a 2×2 matrix as two lines of text."""
    return f"[{M[0,0]:.2f}, {M[0,1]:.2f}]\n[{M[1,0]:.2f}, {M[1,1]:.2f}]"

def make_code_text(fig, angle_deg):
    """Draw or update the code snippet on the right, inserting numeric theta."""
    theta = np.deg2rad(angle_deg)
    lines = [
        "def rotate(points, angle_deg):",
        "    theta = np.deg2rad(angle_deg)",
        f"    R = np.array([[np.cos({theta:.4f}), -np.sin({theta:.4f})],",
        f"                  [np.sin({theta:.4f}),  np.cos({theta:.4f})]])",
        "    return points.dot(R.T), R, theta",
        "",
        f"angle_deg = {angle_deg:.2f}",
        f"theta     = {theta:.4f}  # radians"
    ]
    if hasattr(make_code_text, "txt"):
        make_code_text.txt.remove()
    make_code_text.txt = fig.text(
        0.78, 0.5, "\n".join(lines),
        va='center', ha='left',
        transform=fig.transFigure,
        fontsize=9,
        fontfamily='monospace',
        bbox=dict(boxstyle="square,pad=0.5",
                  facecolor="#f7f7f7", alpha=0.9)
    )

def main(initial_angle):
    scale = 2.0
    base = scale * np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [0.5, 0.8]
    ])
    centroid = base.mean(axis=0)

    # move triangles closer: centroids at ±1.0 units
    shift = 1.0
    left_shift  = np.array([-shift, 0])
    right_shift = np.array([ shift, 0])

    orig_angle = 0.0
    user_angle = initial_angle

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_axes([0.05, 0.15, 0.70, 0.80])   # main plot
    fig.subplots_adjust(right=0.75)

    # initial coords
    coords_orig = rotate(base, orig_angle, centroid) + left_shift
    coords_rot  = rotate(base, orig_angle + user_angle, centroid) + right_shift

    p_orig = plt.Polygon(coords_orig, facecolor='skyblue',
                         edgecolor='blue', alpha=0.6, picker=True)
    p_rot  = plt.Polygon(coords_rot,  facecolor='salmon',
                         edgecolor='red',  alpha=0.6, picker=True)
    ax.add_patch(p_orig)
    ax.add_patch(p_rot)

    txt_orig = ax.text(*(centroid + left_shift),
                       format_matrix(np.eye(2)),
                       ha='center', va='center', fontsize=8,
                       bbox=dict(boxstyle="round,pad=0.3",
                                 facecolor="white", alpha=0.8))
    txt_rot  = ax.text(*(centroid + right_shift),
                       format_matrix(rotation_matrix(user_angle)),
                       ha='center', va='center', fontsize=8,
                       bbox=dict(boxstyle="round,pad=0.3",
                                 facecolor="white", alpha=0.8))

    # fixed axes large enough for full rotation
    dists = np.linalg.norm(base - centroid, axis=1)
    max_r = dists.max() * 1.2
    ax.set_xlim(-shift - max_r, shift + max_r)
    ax.set_ylim(-max_r, max_r)
    ax.set_aspect('equal', 'box')
    ax.grid(True)
    ax.set_title("Interactive Side-by-Side 2D Rotation")

    make_code_text(fig, user_angle)

    # add TextBox for angle input
    tb_ax = fig.add_axes([0.25, 0.02, 0.50, 0.05])
    angle_box = TextBox(tb_ax, 'Angle (deg)', initial=str(initial_angle))

    dragging = {"which": None, "angle_offset": 0.0}

    def update_display():
        nonlocal coords_orig, coords_rot
        coords_orig = rotate(base, orig_angle, centroid) + left_shift
        coords_rot  = rotate(base, orig_angle + user_angle, centroid) + right_shift
        p_orig.set_xy(coords_orig)
        p_rot.set_xy(coords_rot)
        txt_rot.set_text(format_matrix(rotation_matrix(user_angle)))
        make_code_text(fig, user_angle)
        fig.canvas.draw_idle()

    def on_submit(text):
        nonlocal user_angle
        try:
            val = float(text)
        except ValueError:
            return
        user_angle = val
        update_display()

    def on_press(event):
        if event.inaxes != ax:
            return
        if p_orig.contains(event)[0]:
            dragging["which"] = "orig"
            click_ang = np.degrees(np.arctan2(
                event.ydata - centroid[1],
                event.xdata - centroid[0]))
            dragging["angle_offset"] = click_ang - orig_angle
        elif p_rot.contains(event)[0]:
            dragging["which"] = "rot"
        else:
            dragging["which"] = None

    def on_motion(event):
        nonlocal orig_angle, user_angle
        if dragging["which"] is None or event.inaxes != ax:
            return
        ang = np.degrees(np.arctan2(
            event.ydata - centroid[1],
            event.xdata - centroid[0]))
        if dragging["which"] == "orig":
            orig_angle = ang - dragging["angle_offset"]
        else:
            user_angle = ang - orig_angle
            angle_box.set_val(f"{user_angle:.2f}")
        update_display()

    angle_box.on_submit(on_submit)
    fig.canvas.mpl_connect('button_press_event', on_press)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Interactive rotation with mouse and text input"
    )
    parser.add_argument("angle", type=float,
                        help="Initial rotation angle in degrees")
    args = parser.parse_args()
    main(args.angle)
