"""WATERLINE rim-footed weave, revision 4 (low flat float): first-pass float and structure check, then the SolidCraft script.
Usage: python gen_rim.py OUT.json [mooring]

Three tall ribs turn one way, three low ribs the other. Every foot sockets onto a low flat ring float: a foam
core in a polyethylene skin around an aluminium ladder frame, its top a few centimetres above the water.
A float fully under water was studied and set aside: with nothing but the rib feet at the surface it capsizes
in the storm case, and taut lines to the bed cannot follow the lake level. There is no mesh. Every figure is a first estimate from catalogue sizes and
stated assumptions. Nothing here is surveyed, tested or engineered; a marine engineer licensed in Ontario
sets the real values and stamps drawings before fabrication.
"""
import json, sys
from math import sin, cos, asin, acos, atan2, radians, degrees, sqrt, hypot, pi

# ---- sizes, mm ----
RING_R = 3350                      # centreline radius of the float; the rib feet stand on this circle
FLOAT_W, FLOAT_T = 600, 140        # float section: wide and thin with rounded edges, in four quarters. 130 gave under twice the weight
SKIN = 5                           # polyethylene skin, water grey
FRAME_B, FRAME_WALL = 100, 4.8     # 6061-T6 square tube. Two rings of it, inner and outer, run inside the float
FRAME_GAP = 400                    # between the two frame rings, joined by rungs
RUNG_KG = 24 * 0.4 * 2.0           # 24 rungs of 50 mm square tube
TUBE_D, TUBE_WALL = 152.4, 3.2     # 6061-T6 tube, the ribs
YAW, SPACING = 25, 900             # degrees each set turns from the shore line; mm between ribs of one set
# name, set (+1 tall, -1 low), place in its set, lean in degrees, rise in mm
RIBS = [('Rib 3 Water', 1, 0, 10, 1850), ('Rib 4 Time', 1, -1, 10, 1700), ('Rib 2 Leaf', 1, 1, 10, 1550),
        ('Rib 5 Air', -1, 0, 25, 1300), ('Rib 1 Warmth', -1, -1, 25, 1150), ('Rib 6 Sweetness', -1, 1, 25, 1000)]
SOCKET = (172, 300)                        # diameter, length of the foot socket collar
STRIP_D = 30                               # light strip and diffuser, socket to socket: one along the top of each rib, one along the underside
# The crown splice is a sleeve inside the tube with a flush seam, so the strip runs over it unbroken.
# The underside strip faces the water, so it is the one that reflects. Finish: float in water grey, so the ribs are the only warm thing.
# ---- allowances, kg ----
FOAM_KG_M3 = 33                                          # closed-cell foam: it is the buoyancy, so a holed skin does not sink it
FIXINGS_KG = 12 * 3 + 6 * 1.5 + 8 * 2.5 + 10            # foot sockets, crown sleeves, frame splice plates at the quarter joints, bolts
POWER_LIGHT_KG = 6 * 1.5 + 5 + 3 + 5 + 4               # panels, battery, box, cable, one lantern on a post
STRIP_KG_M = 2 * 0.35                                    # two light strips with channel and diffuser, per metre of rib
MOORING_KG = 20                                          # rope, shackles and the hanging share of chain, calm water
MARGIN = 1.10
RHO_PE, RHO_AL, E_AL = 955, 2700, 69e9
# ---- assumptions to be replaced by the engineer's values ----
WIND_KPA, CD = 0.8, 1.2            # gust pressure for a summer storm; drag factor of a round tube
WAVE_M = 0.4                       # height difference across the ring; stands in for about a 1 m harbour wave 17 m long
SCOPE = 5                          # mooring line length over water depth
STRESS_OK_MPA = 55                 # working stress allowed beside a weld in 6061-T6, about half its welded yield
COMPARTMENTS = 4
# watts per lit rib (a band on each of its two strips, 1.5 W each), idle draw of a lit rib's two strips (unlit ribs are switched off),
# ribs lit, hours, modem and controller, sun hours
LIT_W, STRIP_IDLE_W, LIT_AVG, NIGHT_H, STANDBY_WH, SUN_H_OCT = 3, 2.2, 2, 10, 15, 2.5

def tube_kg_m(d, wall, rho): return rho * pi * (d - wall) * wall / 1e6
def tube_i(d, wall): return pi / 64 * (d ** 4 - (d - 2 * wall) ** 4) / 1e12          # m4
def tube_s(d, wall): return tube_i(d, wall) / (d / 2000)                              # m3
def box_kg_m(b, wall, rho): return rho * (b ** 2 - (b - 2 * wall) ** 2) / 1e6
def box_s(b, wall): return (b ** 4 - (b - 2 * wall) ** 4) / 12 / (b / 2) / 1e9        # m3, square tube

def frame(name, s, k, lean, rise):
    a, t, d = radians(s * YAW), radians(lean), k * SPACING
    xd, n = (cos(a), sin(a), 0), (-sin(a), cos(a), 0)
    yd = (n[0] * sin(t), n[1] * sin(t), cos(t))
    return [d * n[0], d * n[1], 0], xd, yd, sqrt(RING_R ** 2 - d ** 2)   # origin, sketch x, sketch y, half span

def arc(r):  # each rib is one circular arc: one roller setting, two equal halves
    half, rise = frame(*r)[3], r[4]
    rad = (half ** 2 + rise ** 2) / (2 * rise)
    return rad, 2 * rad * asin(half / rad)   # bend radius, tube length

def at(r, a, base):  # point on the rib centreline at arc angle a from the crown, and the tangent there
    o, xd, yd, half = frame(*r); rad = arc(r)[0]
    u, v = rad * sin(a), rad * cos(a) - (rad - r[4])
    return ([o[k] + u * xd[k] + v * yd[k] + (base if k == 2 else 0) for k in range(3)],
            [cos(a) * xd[k] - sin(a) * yd[k] for k in range(3)])

def line(r, base, N=240):
    th = asin(frame(*r)[3] / arc(r)[0])
    return [at(r, -th + 2 * th * j / N, base)[0] for j in range(N + 1)]

# ---- weight ----
ring_m = 2 * pi * RING_R / 1000
rib_m = sum(arc(r)[1] for r in RIBS) / 1000
CORNER = 0.45 * FLOAT_T                                  # corner radius of the float section, mm
def wide(z):  # width of the float section at height z above its bottom, m
    e = min(z, FLOAT_T - z)
    cut = CORNER - sqrt(max(0, CORNER ** 2 - (CORNER - e) ** 2)) if e < CORNER else 0
    return (FLOAT_W - 2 * cut) / 1000
def wet(d, n=400): return sum(wide((k + .5) * d / n) for k in range(n)) * d / n / 1000   # m2 of section below draft d (mm)
section = wet(FLOAT_T)
W = {'float skin': RHO_PE * SKIN / 1000 * (2 * (FLOAT_W + FLOAT_T) - (8 - 2 * pi) * CORNER) / 1000 * ring_m,
     'float foam': FOAM_KG_M3 * (section - 2 * (FRAME_B / 1000) ** 2) * ring_m,
     'aluminium frame in the float': 2 * box_kg_m(FRAME_B, FRAME_WALL, RHO_AL) * ring_m + RUNG_KG,
     'six ribs': tube_kg_m(TUBE_D, TUBE_WALL, RHO_AL) * rib_m,
     'light strips along the ribs': STRIP_KG_M * rib_m,
     'sockets, sleeves, straps, bolts': FIXINGS_KG, 'power, navigation lights': POWER_LIGHT_KG, 'mooring gear carried': MOORING_KG}
total = sum(W.values()) * MARGIN

# ---- how deep it sits: fresh water, 1000 kg per cubic metre ----
def draft_for(kg):  # mm
    lo, hi = 0, FLOAT_T
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if wet(mid) * ring_m * 1000 < kg else (lo, mid)
    return lo
draft = draft_for(total) / 1000                                 # m
full = section * ring_m * 1000
width = wide(draft * 1000)                                      # waterline width of the float
stiff = 1000 * 9.81 * pi * (RING_R / 1000) ** 3 * width         # righting moment per radian of tilt, N m
BASE = FLOAT_T / 1000 - draft                                   # top of the float, where the rib feet stand, m above water

# ---- wind: every rib taken broadside at once, which overstates it ----
wind_n = WIND_KPA * 1000 * CD * (rib_m * TUBE_D / 1000 + 2 * RING_R / 1000 * BASE)
line_down_n = wind_n / SCOPE                                    # a loaded mooring line also pulls the edge down
storm_tilt = degrees((wind_n * 1.2 + line_down_n * RING_R / 1000) / stiff)
person_tilt = degrees(100 * 9.81 * RING_R / 1000 / stiff)

# ---- waves: buoyancy rises and falls around the ring and bends it. The two frame rings taken alone, which overstates it ----
frame_s = 2 * box_s(FRAME_B, FRAME_WALL)
wave_q = 1000 * 9.81 * FLOAT_W / 1000 * WAVE_M / 2              # N per metre of ring; a wave covers the whole width
wave_mpa = wave_q * (RING_R / 1000) ** 2 / 3 / frame_s / 1e6

# ---- ribs in wind: the tallest rib broadside, half its overturning taken at each foot ----
tall = max(RIBS, key=lambda rb: rb[4])
rib_wind_n = WIND_KPA * 1000 * CD * arc(tall)[1] / 1000 * TUBE_D / 1000
rib_mpa = rib_wind_n * 0.64 * tall[4] / 1000 / 2 / tube_s(TUBE_D, TUBE_WALL) / 1e6
foot_on_ring_mpa = rib_wind_n * 0.64 * tall[4] / 1000 / 2 / 2 / frame_s / 1e6   # shared two ways along the frame
# hum in steady wind: rough first sideways frequency (45 percent of a straight clamped beam of the same length)
dev = arc(tall)[1] / 1000
hum_hz = 0.45 * 3.565 * sqrt(E_AL * tube_i(TUBE_D, TUBE_WALL) / (tube_kg_m(TUBE_D, TUBE_WALL, RHO_AL) * dev ** 4))
hum_wind = hum_hz * TUBE_D / 1000 / 0.2                         # m/s at which shed eddies match that frequency

# ---- power ----
wh_day = ((LIT_W + STRIP_IDLE_W) * LIT_AVG * NIGHT_H + STANDBY_WH) * 1.2
panel_w = wh_day / (SUN_H_OCT * 0.65)

L = [line(rb, BASE * 1000) for rb in RIBS]
gap = min(hypot(hypot(p[0] - q[0], p[1] - q[1]), p[2] - q[2]) for i in range(6) for j in range(i) for p in L[i][::2] for q in L[j][::2])
top = max(p[2] for l in L for p in l) + TUBE_D / 2 + 10
strip_gap = gap - TUBE_D - 2 * (STRIP_D / 2 - 5)             # strips stand 10 mm proud of the tube

def cyl(name, base, axis, d, h): return {'command': 'solid.cylinder', 'params': {'diameter': d, 'height': h, 'base': [round(x, 2) for x in base], 'axis': [round(x, 5) for x in axis], 'body_name': name}}
def on_ring(deg, z, rad=RING_R): return [rad * cos(radians(deg)), rad * sin(radians(deg)), z], [-sin(radians(deg)), cos(radians(deg)), 0]   # point, tangent

if __name__ == '__main__':
    print('WEIGHT, kg'); [print(f'  {k:34} {v:6.0f}') for k, v in W.items()]
    print(f'  {"total with 10 percent margin":34} {total:6.0f}')
    print(f'FLOAT  can carry {full:.0f} kg fully under, {full / total:.1f} times the weight; with one quarter lost {full * (COMPARTMENTS - 1) / COMPARTMENTS / total:.1f} times')
    print(f'  {FLOAT_W} wide by {FLOAT_T} thick; sits {draft * 1000:.0f} mm deep; top of float and rib feet {BASE * 1000:.0f} mm, top of work {top:.0f} mm above water')
    print(f'  100 kg more sinks it {100 / (ring_m * width * 1000) * 1000:.0f} mm; 100 kg on the edge tilts it {person_tilt:.2f} degrees')
    print(f'WIND  {wind_n / 1000:.1f} kN sideways at {WIND_KPA} kPa on everything at once; storm tilt with line pull {storm_tilt:.1f} degrees')
    print(f'ANCHORS  each must hold about {wind_n / 1000:.1f} kN sideways (wind can line up with one line); a plain block needs about {wind_n / 9.81 / 0.5 / (1 - 1 / 2.4):.0f} kg of concrete at friction 0.5')
    print(f'WAVES  {WAVE_M} m waves bend the aluminium frame to about {wave_mpa:.0f} MPa if it worked alone (limit used {STRESS_OK_MPA})')
    print(f'RIBS  tallest rib in the gust: {rib_wind_n:.0f} N, {rib_mpa:.0f} MPa at the foot, {foot_on_ring_mpa:.0f} MPa into the frame')
    print(f'  hum: sideways frequency about {hum_hz:.0f} Hz, matched by a steady {hum_wind:.0f} m/s wind; fit a hanging damper inside each rib')
    print(f'POWER  {wh_day:.0f} Wh a day; about {panel_w:.0f} W of panel for October sun; battery about {wh_day * 3:.0f} Wh for three dull days')
    print(f'RIBS  {rib_m:.1f} m of tube, {2 * rib_m:.0f} m of light strip; closest tubes {gap - TUBE_D:.0f} mm apart, {strip_gap:.0f} mm counting the strips')
    for rb in RIBS:
        rad, ln = arc(rb); half = frame(*rb)[3]
        print(f'  {rb[0]:16} span {2 * half / 1000:.2f} m  rise {rb[4] / 1000:.2f} m  bend radius {rad / 1000:.2f} m  tube {ln / 1000:.2f} m  foot angle {degrees(asin(half / rad)):.0f} deg')
    # self-checks: the build stops if a margin is lost
    assert strip_gap >= 150, strip_gap                                    # tubes and strips clear each other by 150 mm
    assert full >= 2 * total and full * (COMPARTMENTS - 1) / COMPARTMENTS > 1.3 * total
    assert BASE * 1000 <= 80                                              # the point of this float: its top stays within 80 mm of the water
    assert max(wave_mpa, rib_mpa, foot_on_ring_mpa) <= STRESS_OK_MPA
    assert top <= 2200                                                    # not too tall: the call asks for that

    zr = BASE * 1000; zb = -draft * 1000; zf = (zr + zb) / 2          # top, bottom and middle of the float, mm from the water
    section_plane = {'origin': [0, 0, 0], 'x_dir': [1, 0, 0], 'y_dir': [0, 0, 1]}
    def ring_body(name, x0, x1, z0, z1, radius=None):                   # a section drawn at +X and turned about the vertical axis
        shape = ({'command': 'sketch.rectangle.rounded', 'params': {'p0': [x0, z0], 'p1': [x1, z1], 'radius': radius}} if radius
                 else {'command': 'sketch.rectangle.two_point', 'params': {'p0': [x0, z0], 'p1': [x1, z1]}})
        return [{'command': 'sketch.create', 'params': {'name': name + ' section', 'plane': section_plane}}, shape, {'command': 'sketch.finish', 'params': {}},
                {'command': 'solid.revolve', 'params': {'axis': 'Z', 'sketch': name + ' section', 'body_name': name}}]
    c = ring_body('Float', RING_R - FLOAT_W / 2, RING_R + FLOAT_W / 2, zb, zr, CORNER)
    # the frame runs inside the float, so these two bodies overlap it on purpose
    for tag, rr in (('inner', RING_R - FRAME_GAP / 2), ('outer', RING_R + FRAME_GAP / 2)):
        c += ring_body(f'Frame ring {tag}', rr - FRAME_B / 2, rr + FRAME_B / 2, zf - FRAME_B / 2, zf + FRAME_B / 2)
    for rb in RIBS:
        o, xd, yd, half = frame(*rb); th = asin(half / arc(rb)[0]); sk = rb[0] + ' path'
        c += [{'command': 'sketch.create', 'params': {'name': sk, 'plane': {'origin': [o[0], o[1], zr], 'x_dir': list(xd), 'y_dir': list(yd)}}},
              {'command': 'sketch.arc.three_point', 'params': {'start': [round(half, 3), 0], 'end': [-round(half, 3), 0], 'through': [0, rb[4]]}},
              {'command': 'sketch.finish', 'params': {}},
              # a1: the id SolidCraft gives the first arc of a sketch
              {'command': 'solid.pipe', 'params': {'path_sketch': sk, 'path': ['a1'], 'diameter': TUBE_D, 'body_name': rb[0]}}]
        # light strips: concentric arcs along the top and the underside of the tube, the paths the colour bands travel
        rad = arc(rb)[0]; ths = th - (SOCKET[1] + 10) / rad   # from the top of one socket to the top of the other
        for tag, off in (('top', TUBE_D / 2 - 5), ('under', -(TUBE_D / 2 - 5))):
            ro = rad + off
            c += [{'command': 'sketch.create', 'params': {'name': f'{sk} light {tag}', 'plane': {'origin': [o[0], o[1], zr], 'x_dir': list(xd), 'y_dir': list(yd)}}},
                  {'command': 'sketch.arc.three_point', 'params': {'start': [round(ro * sin(ths), 3), round(ro * cos(ths) - (rad - rb[4]), 3)], 'end': [-round(ro * sin(ths), 3), round(ro * cos(ths) - (rad - rb[4]), 3)], 'through': [0, rb[4] + off]}},
                  {'command': 'sketch.finish', 'params': {}},
                  {'command': 'solid.pipe', 'params': {'path_sketch': f'{sk} light {tag}', 'path': ['a1'], 'diameter': STRIP_D, 'body_name': rb[0].replace('Rib', f'Light strip {tag}')}}]
        for side, a in (('A', th), ('B', -th)):                           # socket collars: the rib slides on and is bolted through
            p, t = at(rb, a, zr); inward = [-x if a > 0 else x for x in t]
            c.append(cyl(f'{rb[0]} socket {side}', p, inward, SOCKET[0], SOCKET[1]))
    top_ring = zr
    for i, deg in enumerate((59, 69, 79, 101, 111, 121)):                 # solar panels lying flat on the float, away from the shore
        c.append({'command': 'solid.box', 'params': {'corner': [-250, RING_R - 150, top_ring + 2], 'length': 500, 'width': 300, 'height': 20, 'body_name': f'Solar panel {i + 1}'}})
        c.append({'command': 'solid.move', 'params': {'bodies': [f'Solar panel {i + 1}'], 'angle': f'{deg - 90} deg', 'origin': [0, 0, 0]}})
    c.append({'command': 'solid.box', 'params': {'corner': [-150, RING_R - 100, top_ring], 'length': 300, 'width': 200, 'height': 80, 'body_name': 'Battery and control box'}})
    for i, deg in enumerate((90,)):                                       # navigation light: self-contained, own power, on the side away from the shore.
        # The front post was removed at the artist's direction. How many lights are required is the harbour authority's call.
        p, _ = on_ring(deg, top_ring, RING_R + FRAME_GAP / 2)
        c += [cyl(f'Navigation light post {i + 1}', p, [0, 0, 1], 48, 900), cyl(f'Navigation light {i + 1}', [p[0], p[1], p[2] + 900], [0, 0, 1], 130, 130)]
    if 'mooring' in sys.argv:                                             # illustration only: depth is not surveyed
        depth = 6000
        for i, deg in enumerate((90, 210, 330)):
            p, _ = on_ring(deg, zf); e = [(RING_R + depth * SCOPE * 0.98) * cos(radians(deg)), (RING_R + depth * SCOPE * 0.98) * sin(radians(deg)), -depth]
            d = [e[k] - p[k] for k in range(3)]; n = hypot(hypot(d[0], d[1]), d[2])
            c += [cyl(f'Mooring line {i + 1}', p, [x / n for x in d], 30, n),
                  {'command': 'solid.box', 'params': {'corner': [e[0] - 400, e[1] - 400, -depth - 300], 'length': 800, 'width': 800, 'height': 300, 'body_name': f'Anchor {i + 1}'}}]
    json.dump({'commands': c}, open(sys.argv[1], 'w', encoding='utf-8'), indent=1)
