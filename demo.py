# Infrastructure is responsible for software integration
# This task is to convert a 3D model to a Stonefish model then to sweep a parameter and visualize the result
# We receive a 3D model as an OnShape URDF export and convert to a Stonefish (our simulator) XML

# Skim these
# https://stonefish.readthedocs.io/en/latest/robots.html
# https://stonefish.readthedocs.io/en/latest/bodies.html

import numpy as np
import helpers

MATERIAL, LOOK, PHYSICS = "Aluminium", "grey", "submerged"


########### ADD CODE HERE ##########################################
# Stonefish only has these joint types: fixed, prismatic, revolute
JOINT_MAP = {"fixed": "fixed", "prismatic": "prismatic", "revolute": "revolute",
             "continuous": "revolute"}

root, links, joints = helpers.read_urdf("frame/urdf/frame.urdf")

# Find the base link of the tree - it is the one link that is NEVER a child

children = {j.find("child").get("link") for j in joints}

base = next(l.get("name") for l in links if l.get("name") not in children)

scene = ['<?xml version="1.0"?>', '<scenario>',
         f'  <material name="{MATERIAL}" density="2700.0"/>',
         f'  <look name="{LOOK}" gray="0.6"/>',
         f'  <robot name="{root.get("name")}" fixed="false">']

# Build the Stonefish model one link at a time
for l in links:
    tag = "base_link" if l.get("name") == base else "link"
    vx, vr = helpers.origin(l.find("visual"))
    mass = l.find("inertial/mass").get("value")
    scene += [f'  <{tag} name="{l.get("name")}" type="model" physics="{PHYSICS}" buoyant="true">',
              f'    <physical><mesh filename="{helpers.mesh_file(l)}" scale="1"/><origin xyz="{vx}" rpy="{vr}"/></physical>',
              f'    <material name="{MATERIAL}"/><look name="{LOOK}"/><mass value="{mass}"/>',
              f'  </{tag}>']

# Add in the joints, one joint at a time
for j in joints:
    jx, jr = helpers.origin(j)
    jtype  = JOINT_MAP[j.get("type")]
    parent = j.find("parent").get("link")
    child  = j.find("child").get("link")
    ax = j.find("axis")
    axis = f'<axis xyz="{ax.get("xyz")}"/>' if ax is not None and jtype != "fixed" else ''
    scene += [f'  <joint name="{j.get("name")}" type="{jtype}">',
              f'    <parent name="{parent}"/><child name="{child}"/>',
              f'    <origin xyz="{jx}" rpy="{jr}"/>{axis}',
              f'  </joint>']

scene += ['  </robot>', '</scenario>']
helpers.save_scene("frame.scn", scene)
print(f"converted {len(links)} links, {len(joints)} joints -> frame.scn")

# Sweep added leg mass, plot center of mass vs center of buoyancy
# Collect each part's mass (from the URDF) and its volume + world-z (from the mesh)
joint_z = {j.find("child").get("link"): float(helpers.origin(j)[0].split()[2]) for j in joints}

mass, vol, z, is_leg = [], [], [], []

for l in links:
    volume, z_centroid = helpers.stl_volume_and_z(helpers.mesh_file(l))
    mass.append(float(l.find("inertial/mass").get("value")))
    vol.append(volume)
    z.append(joint_z.get(l.get("name"), 0.0) + z_centroid)     # world height of this part
    is_leg.append(l.get("name").startswith("leg"))             # the swept parameter targets the legs

mass, vol, z, is_leg = map(np.array, (mass, vol, z, is_leg))

ballast = np.linspace(0, 2, 80)      # kg of ballast, split across the 4 legs

com_z = []

for b in ballast:
    # per-part mass with this much ballast added to the legs
    m = mass + is_leg * b / 4

    # center of mass height = mass-weighted average of z (in cm, so *100).
    com_z.append((m * z).sum() / m.sum() * 100)

# center of buoyancy height = VOLUME-weighted average of z (in cm)
cob_z = (vol * z).sum() / vol.sum() * 100

helpers.plot_stability(ballast, np.array(com_z), cob_z)