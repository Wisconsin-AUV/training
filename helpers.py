import xml.etree.ElementTree as ET, struct
import numpy as np
import matplotlib.pyplot as plt


def read_urdf(path):
    """Return (root, links, joints) parsed from a URDF file."""
    root = ET.parse(path).getroot()
    return root, root.findall("link"), root.findall("joint")


def origin(elem):
    """Read an <origin xyz rpy/> child as two strings; default to zeros."""
    o = elem.find("origin")
    if o is None:
        return "0 0 0", "0 0 0"
    return o.get("xyz", "0 0 0"), o.get("rpy", "0 0 0")


def mesh_file(link):
    """Mesh filename of a link, with the ROS 'package://' prefix removed."""
    filename = link.find("visual/geometry/mesh").get("filename")
    return filename.replace("package://", "")


def stl_volume_and_z(path):
    """Volume (m^3) and the z-height of the centroid of a binary STL mesh."""
    data = open(path, "rb").read()
    n = struct.unpack("<I", data[80:84])[0]
    tri = np.frombuffer(data, np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]), n, 84)["v"]
    signed_vol = np.einsum("ij,ij->i", tri[:, 0], np.cross(tri[:, 1], tri[:, 2])) / 6.0
    volume = abs(signed_vol.sum())
    z_centroid = (tri[:, :, 2].mean(1) * signed_vol).sum() / signed_vol.sum()
    return volume, z_centroid


def save_scene(path, lines):
    """Write the assembled Stonefish scene (a list of lines) to disk."""
    with open(path, "w") as f:
        f.write("\n".join(lines))


def plot_stability(ballast, com_z_cm, cob_z_cm, out="com_cob.png"):
    """Plot swept CoM height against the constant CoB height, then save + show."""
    plt.figure(figsize=(8, 5))
    plt.plot(ballast, com_z_cm, color="tomato", lw=2, label="Center of mass  z")
    plt.axhline(cob_z_cm, color="seagreen", lw=2, label="Center of buoyancy  z")
    plt.fill_between(ballast, com_z_cm, cob_z_cm, where=(com_z_cm <= cob_z_cm), color="seagreen", alpha=0.12)
    plt.fill_between(ballast, com_z_cm, cob_z_cm, where=(com_z_cm >  cob_z_cm), color="tomato",  alpha=0.12)
    plt.xlabel("ballast mass added to the legs  (kg)")
    plt.ylabel("height  z  (cm)")
    plt.title("Frame self-rights once CoB sits above CoM")
    plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout()
    plt.savefig(out, dpi=110)
    plt.show()