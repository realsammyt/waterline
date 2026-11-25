"""Blender: close-up studies of the WATERLINE model on a plain water plane.
Run: blender -b -P closeup.py -- MODEL.glb OUT_DIR
Writes night-strips.png and night-strips-above.png (all six strips lit full length, to show where they sit),
and day.png."""
import bpy, sys, math, os
from mathutils import Vector
glb, out = sys.argv[sys.argv.index('--') + 1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.samples = 96; sc.view_settings.view_transform = 'Standard'
sc.render.resolution_x, sc.render.resolution_y = 1600, 1000
lin = lambda h: tuple(((int(h[i:i + 2], 16) / 255) ** 2.2) for i in (1, 3, 5))
TONES = {'Warmth': '#d94fc7', 'Leaf': '#ffe08a', 'Water': '#cf5a36', 'Time': '#ff9a2e', 'Air': '#ff8fa8', 'Sweetness': '#9a86ff'}

def mat(name, color, metallic, rough):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1); b.inputs['Metallic'].default_value = metallic; b.inputs['Roughness'].default_value = rough
    return m
honey, grey = mat('honey', (.62, .36, .10), 1, .42), mat('float', (.20, .24, .27), 0, .75)
alu, solar, navm = mat('alu', (.45, .46, .48), 1, .5), mat('solar', (.02, .03, .07), 0, .2), mat('nav', (.9, .85, .5), 0, .4)
strips = {}
for o in bpy.data.objects:
    if o.type != 'MESH': continue
    n = o.name.lower(); o.data.materials.clear()
    for p in o.data.polygons: p.use_smooth = True
    if 'light strip' in n:
        v = next(k for k in TONES if k.lower() in n); m = strips.get(v) or mat('strip ' + v, (.8, .78, .72), 0, .35); strips[v] = m; o.data.materials.append(m)
    elif 'float' in n or 'aluminium ring' in n: o.data.materials.append(grey)   # ring and float in one water grey
    elif 'solar' in n: o.data.materials.append(solar)
    elif n.startswith('navigation light') and 'post' not in n: o.data.materials.append(navm)
    elif n.startswith('rib'): o.data.materials.append(honey)      # ribs and their foot sockets
    else: o.data.materials.append(alu)

bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, 0))
water = bpy.context.object; wm = mat('water', (.02, .05, .07), 0, .06); water.data.materials.append(wm)
world = bpy.data.worlds.new('w'); world.use_nodes = True; sc.world = world; bg = world.node_tree.nodes['Background']
sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sc.collection.objects.link(sun); sun.rotation_euler = (math.radians(55), 0, math.radians(140))
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam

def shot(name, pos, target=(0, 0, .8), lens=35):
    cam.location = pos; cam.data.lens = lens
    cam.rotation_euler = (Vector(target) - Vector(pos)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(out, name); bpy.ops.render.render(write_still=True); print('done', name)

def lights(on):
    for v, m in strips.items():
        b = m.node_tree.nodes['Principled BSDF']
        b.inputs['Emission Color'].default_value = (*lin(TONES[v]), 1); b.inputs['Emission Strength'].default_value = 4 if on else 0

# night: every strip lit along its whole length, which the work would rarely do; this is to show where the strips sit
bg.inputs['Color'].default_value = (.02, .04, .10, 1); bg.inputs['Strength'].default_value = .35; sun.data.energy = 0; lights(True)
shot('night-strips.png', (8.5, -10.5, 2.6))
shot('night-strips-shore.png', (0, -14, 1.7))
shot('night-strips-above.png', (0, -3.5, 15), target=(0, 0, 0), lens=32)
# day
bg.inputs['Color'].default_value = (.55, .68, .9, 1); bg.inputs['Strength'].default_value = .7; sun.data.energy = 3.5; lights(False)
wm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (.05, .12, .16, 1)
shot('day.png', (8.5, -10.5, 2.6))
