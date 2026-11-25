"""Write the SolidCraft script for WATERLINE v0.5. Usage: python gen_model.py OUT.json [yaw_deg lean_deg]
yaw turns alternate ribs left and right seen from above; lean tips alternate ribs forward and back."""
import json, sys
from math import sin, cos, radians
def frame(yaw, lean):  # sketch x and y axes in world coordinates
    a, t = radians(yaw), radians(lean)
    return (cos(a), sin(a), 0), (-sin(a) * sin(t), cos(a) * sin(t), cos(t))
# span, rise in mm, front to back: same six ribs as simulators/weave.html and docs/rings-on-mother.md
RIBS = [(5140, 1420), (5440, 1640), (6000, 2000), (5820, 1830), (5320, 1560), (4940, 1300)]
VALUES = ['Warmth', 'Leaf', 'Water', 'Time', 'Air', 'Sweetness']
yaw, lean = (float(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) > 3 else (0, 0)
n = 6
c = []
def cmd(command, **params): c.append({'command': command, 'params': params})
def par(name, mm, comment): cmd('parameters.add', name=name, expression=str(mm), unit='mm', comment=comment)

par('disc_d', 7000, 'mother disc, outside of rim')
par('rim_d', 300, 'rim pipe, centre on the waterline, so the top is 150 above water')
par('tube_d', 150, 'rib tube')
par('rib_base', 150, 'height of the rib ends above water')
par('spacing', 440, 'gap between rib planes')
for i, (span, rise) in enumerate(RIBS, 1):
    par(f'span{i}', span, f'rib {i} {VALUES[i-1]}')
    par(f'rise{i}', rise, f'rib {i} {VALUES[i-1]}')

# world: Z up, water at Z=0, the viewer on shore looks along Y
cmd('solid.torus', major='disc_d/2 - rim_d/2', minor='rim_d/2', body_name='Rim')
cmd('solid.cylinder', diameter='disc_d - rim_d', height=6, base=[0, 0, -3], body_name='Mesh')
for i in range(1, n + 1):
    sk = f'Rib {i} path'
    s = 1 if i % 2 else -1
    xd, yd = frame(s * yaw, s * lean)
    cmd('sketch.create', name=sk, plane={'origin': [0, f'{i - 3.5} * spacing', 'rib_base'], 'x_dir': list(xd), 'y_dir': list(yd)})
    cmd('sketch.equation_curve', x=f'span{i} / 2 * cos(t)', y=f'rise{i} * sin(t)', start=0, end='pi')
    cmd('sketch.finish')
    # s1: the id SolidCraft gives the first spline of a sketch
    cmd('solid.pipe', path_sketch=sk, path=['s1'], diameter='tube_d', body_name=f'Rib {i} {VALUES[i-1]}')
json.dump({'commands': c}, open(sys.argv[1], 'w', encoding='utf-8'), indent=1)
