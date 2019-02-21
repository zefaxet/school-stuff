from tkinter import *
from decimal import *
from math import *

# METHODS #####################################

# set the precision for Decimal operations to 28 digits
getcontext().prec = 28


def render():

	depth = DEPTH  # maximum ray depth
	# setup_drawing_canvas()

	# center of projection
	xs, ys, zs = Decimal(0.0), Decimal(0.0), Decimal(-800.0)

	for pixel_x in range(1, WIDTH + 1):

		screen_x = pixel_x - Decimal(WIDTH) / 2

		for pixel_y in range(1, HEIGHT + 1):

			screen_y = pixel_y - Decimal(HEIGHT) / 2

			# compute vector for ray from center of projection through pixel
			ray_i = screen_x - xs
			ray_j = screen_y - ys
			ray_k = 0 - zs

			# trace the ray through the environment to obtain the pixel color
			ir, ig, ib = trace_ray(0, depth, xs, ys, zs, ray_i, ray_j, ray_k)

			put_pixel(pixel_x, pixel_y, ir, ig, ib)


def trace_ray(flag: int, level: int,
			xs: Decimal, ys: Decimal, zs: Decimal,
			ray_i: Decimal, ray_j: Decimal, ray_k: Decimal) -> [int, int, int]:

	if level == 0:

		# print("Maximum depth exceeded - return black.")
		return 0, 0, 0

	else:

		# check for intersection of ray with objects
		# and set rgb values corresponding to objects

		# set distance of closest object initially to a very large number
		t = [inf]

		# initially no object has been intersected by the ray
		object_code = -1

		# use an array-list to pass arguments by reference-ish
		intersect_refs = [None, None, None]
		normal_refs = [None, None, None]

		if checkerboard_intersection(xs, ys, zs, ray_i, ray_j, ray_k, t, intersect_refs):

			object_code = 0
			if flag:
				print("Checkerboard intersected.")

		if sphere1_intersection(xs, ys, zs, ray_i, ray_j, ray_k, t, intersect_refs, normal_refs):

			object_code = 1
			if flag:
				print("Green sphere intersected.")

		if sphere2_intersection(xs, ys, zs, ray_i, ray_j, ray_k, t, intersect_refs, normal_refs):

			object_code = 2
			if flag:
				print("Reflective sphere intersected.")

		intersect_x = intersect_refs[0]
		intersect_y = intersect_refs[1]
		intersect_z = intersect_refs[2]

		obj_normal_x = normal_refs[0]
		obj_normal_y = normal_refs[1]
		obj_normal_z = normal_refs[2]

		if object_code == 0:
			ir, ig, ib = checkerboard_point_intensity(level, ray_j, ray_j, ray_k,
												intersect_x, intersect_y, intersect_z)
		elif object_code == 1:
			ir, ig, ib = sphere1_point_intensity(level, ray_i, ray_j, ray_k,
												intersect_x, intersect_y, intersect_z,
												obj_normal_x, obj_normal_y, obj_normal_z)
		elif object_code == 2:
			ir, ig, ib = sphere2_point_intensity(level, ray_i, ray_j, ray_k,
												intersect_x, intersect_y, intersect_z,
												obj_normal_x, obj_normal_y, obj_normal_z)
		else:
			# set pixel color to background color (light blue)
			ir, ig, ib = 150, 150, 255

		return ir, ig, ib


def checkerboard_intersection(xs: Decimal, ys: Decimal, zs: Decimal,
							ray_x: Decimal, ray_y: Decimal, ray_z: Decimal,
							t: list, intersect_refs: list) -> bool:

	# normal of plane
	a, b, c = Decimal(0), Decimal(1), Decimal(0)

	# point on plane
	x1, y1, z1 = BOARD_POSITION

	# compute intersection of ray with plane
	denom = a * ray_x + b * ray_y + c * ray_z

	if abs(denom) <= 0.001:

		return False

	else:

		d = a * x1 + b * y1 + c * z1
		t_object = -(a * xs + b * ys + c * zs - d) / denom
		x = xs + ray_x * t_object
		y = ys + ray_y * t_object
		z = zs + ray_z * t_object
		if z < 0 or z > 8000 or t_object < 0:
			# print("No visible intersection.")
			return False
		elif t[0] < t_object:
			return False
			# print("Another object is closer")
		else:
			t[0] = t_object
			intersect_refs[0] = x
			intersect_refs[1] = y
			intersect_refs[2] = z
			return True


def checkerboard_point_intensity(level: int, ray_x: Decimal, ray_y: Decimal, ray_z: Decimal,
								x: Decimal, y: Decimal, z: Decimal) -> tuple:

	# a red and white checkered plane
	
	# normal of the plane
	nx, ny, nz = Decimal(0), Decimal(1), Decimal(0)
	
	# normal of the incoming ray vector
	magnitude = (ray_x ** 2 + ray_y ** 2 + ray_z ** 2).sqrt()
	ray_x_norm = ray_x / magnitude
	ray_y_norm = ray_y / magnitude
	ray_z_norm = ray_z / magnitude
	
	magnitude = (nx ** 2 + ny ** 2 + nz ** 2).sqrt()
	nx_norm = nx / magnitude
	ny_norm = ny / magnitude
	nz_norm = nz / magnitude
	
	# calculate reflection vector
	cosine_phi = (-ray_x_norm * nx_norm) + (-ray_y_norm * ny_norm) + (-ray_z_norm * nz_norm)
	
	if cosine_phi > 0:

		rx = - nx_norm - (ray_x_norm) / (2 * -cosine_phi)
		ry = ny_norm - (-ray_y_norm) / (2 * -cosine_phi)
		rz = nz_norm - (-ray_z_norm) / (2 * cosine_phi)

	elif cosine_phi == 0:

		rx = ray_x_norm
		ry = ray_y_norm
		rz = ray_z_norm

	else:

		rx = -nx_norm + (-ray_x_norm) / (2 * cosine_phi)
		ry = -ny_norm + (-ray_y_norm) / (2 * cosine_phi)
		rz = -nz_norm + (-ray_z_norm) / (2 * cosine_phi)

	# trace the reflection ray
	ir, ig, ib = trace_ray(0, level - 1, x, y + Decimal(0.000001), z, rx, ry, rz)
	
	# compute local at intersection point
	color_flag = 1 if x >= 0 else 0
	if abs(fmod(x, 400.0)) > 200.0:
		color_flag = not color_flag
	if abs(fmod(z, 400.0)) > 200.0:
		color_flag = not color_flag

	if color_flag:

		# red
		ir_local = 255
		ig_local = 0
		ib_local = 0

	else:

		# white
		ir_local = 255
		ig_local = 255
		ib_local = 255

	# if [ir, ig, ib] != [255, 255, 255] and [ir, ig, ib] != [255, 0, 0]:
	# 	print(pixel_x, ir, ig, ib, level)

	# add effect of local color
	ir = int(.3 * ir + .7 * ir_local)
	ig = int(.3 * ig + .7 * ig_local)
	ib = int(.3 * ib + .7 * ib_local)

	return ir, ig, ib


def sphere1_intersection(xs: Decimal, ys: Decimal, zs: Decimal,
						ray_x: Decimal, ray_y: Decimal, ray_z: Decimal,
						t: list, intersect_refs: list, normal_refs: list) -> bool:

	# center of sphere
	l = Decimal(SPHERE1_POSITION[0])
	m = Decimal(SPHERE1_POSITION[1])
	n = Decimal(SPHERE1_POSITION[2])

	# radius of sphere
	r = Decimal(SPHERE1_RADIUS)

	# compute intersection of ray with sphere
	asphere = ray_x ** 2 + ray_y ** 2 + ray_z ** 2
	bsphere = 2 * ray_x * (xs - l) + 2 * ray_y * (ys - m) + 2 * ray_z * (zs-n)
	csphere = l ** 2 + m ** 2 + n ** 2 + xs ** 2 + ys ** 2 + zs ** 2 + 2 * (-l * xs - m * ys - n * zs) - r ** 2

	disc = bsphere ** 2 - 4 * asphere * csphere

	if disc < 0:
		return False
	else:

		ts1 = (-bsphere + disc.sqrt()) / (2 * asphere)
		ts2 = (-bsphere - disc.sqrt()) / (2 * asphere)
		tsphere = min(ts1, ts2)
		if t[0] < tsphere:
			return False
		elif tsphere < 0:
			return False
		else:
			t[0] = tsphere
			intersect_refs[0] = xs + ray_x * tsphere
			intersect_refs[1] = ys + ray_y * tsphere
			intersect_refs[2] = zs + ray_z * tsphere
			normal_refs[0] = intersect_refs[0] - l
			normal_refs[1] = intersect_refs[1] - m
			normal_refs[2] = intersect_refs[2] - n
			return True


def sphere1_point_intensity(level: int, ray_x: Decimal, ray_y: Decimal, ray_z: Decimal,
							x: Decimal, y: Decimal, z: Decimal,
							nx: Decimal, ny: Decimal, nz: Decimal):

	magnitude = (ray_x ** 2 + ray_y ** 2 + ray_z ** 2).sqrt()
	ray_x_norm = ray_x / magnitude
	ray_y_norm = ray_y / magnitude
	ray_z_norm = ray_z / magnitude

	magnitude = (nx ** 2 + ny ** 2 + nz ** 2).sqrt()
	nx_norm = nx / magnitude
	ny_norm = ny / magnitude
	nz_norm = nz / magnitude

	# calculate reflection vector

	cosine_phi = (-ray_x_norm * nx_norm) + (-ray_y_norm * ny_norm) + (-ray_z_norm * nz_norm)

	if cosine_phi > 0:

		rx = nx_norm - (-ray_x_norm) / (2 * cosine_phi)
		ry = ny_norm - (-ray_y_norm) / (2 * cosine_phi)
		rz = nz_norm - (-ray_z_norm) / (2 * cosine_phi)

	elif cosine_phi == 0:

		rx = ray_x_norm
		ry = ray_y_norm
		rz = ray_z_norm

	else:

		rx = -nx_norm + (-ray_x_norm) / (2 * cosine_phi)
		ry = -ny_norm + (-ray_y_norm) / (2 * cosine_phi)
		rz = -nz_norm + (-ray_z_norm) / (2 * cosine_phi)

	# trace the reflection ray
	ir, ig, ib = trace_ray(0, level - 1, x, y, z, rx, ry, rz)

	# add effect of local color
	ir = int(.7 * ir + .3 * 200)
	ig = int(.7 * ig + .3 * 240)
	ib = int(.7 * ib + .3 * 0)
	
	ir, ig, ib = get_lit_color([ir, ig, ib], [nx_norm, ny_norm, nz_norm])

	return ir, ig, ib


def sphere2_intersection(xs: Decimal, ys: Decimal, zs: Decimal,
						ray_x: Decimal, ray_y: Decimal, ray_z: Decimal,
						t: list, intersect_refs: list, normal_refs: list) -> bool:
	
	# center of sphere
	l = Decimal(SPHERE2_POSITION[0])
	m = Decimal(SPHERE2_POSITION[1])
	n = Decimal(SPHERE2_POSITION[2])

	# radius of sphere
	r = Decimal(SPHERE2_RADIUS)

	# compute intersection of ray with sphere
	asphere = ray_x ** 2 + ray_y ** 2 + ray_z ** 2
	bsphere = 2 * ray_x * (xs - l) + 2 * ray_y * (ys - m) + 2 * ray_z * (zs - n)
	csphere = l ** 2 + m ** 2 + n ** 2 + xs ** 2 + ys ** 2 + zs ** 2 + 2 * (-l * xs - m * ys - n * zs) - r ** 2

	disc = bsphere ** 2 - 4 * asphere * csphere

	if disc < 0:
		return False
	else:

		ts1 = (-bsphere + disc.sqrt()) / (2 * asphere)
		ts2 = (-bsphere - disc.sqrt()) / (2 * asphere)
		tsphere = min(ts1, ts2)
		if t[0] < tsphere:
			# another object is closer
			return False
		elif tsphere < 0:
			return False
		else:
			t[0] = tsphere
			intersect_refs[0] = xs + ray_x * tsphere
			intersect_refs[1] = ys + ray_y * tsphere
			intersect_refs[2] = zs + ray_z * tsphere
			normal_refs[0] = intersect_refs[0] - l
			normal_refs[1] = intersect_refs[1] - m
			normal_refs[2] = intersect_refs[2] - n
			return True


def sphere2_point_intensity(level: int, ray_x: Decimal, ray_y: Decimal, ray_z: Decimal,
							x: Decimal, y: Decimal, z: Decimal,
							nx: Decimal, ny: Decimal, nz: Decimal):
	
	magnitude = (ray_x ** 2 + ray_y ** 2 + ray_z ** 2).sqrt()
	ray_x_norm = ray_x / magnitude
	ray_y_norm = ray_y / magnitude
	ray_z_norm = ray_z / magnitude

	magnitude = (nx ** 2 + ny ** 2 + nz ** 2).sqrt()
	nx_norm = nx / magnitude
	ny_norm = ny / magnitude
	nz_norm = nz / magnitude

	# calculate reflection vector

	cosine_phi = (-ray_x_norm * nx_norm) + (-ray_y_norm * ny_norm) + (-ray_z_norm * nz_norm)

	if cosine_phi > 0:

		rx = nx_norm - (-ray_x_norm) / (2 * cosine_phi)
		ry = ny_norm - (-ray_y_norm) / (2 * cosine_phi)
		rz = nz_norm - (-ray_z_norm) / (2 * cosine_phi)

	elif cosine_phi == 0:

		rx = ray_x_norm
		ry = ray_y_norm
		rz = ray_z_norm

	else:

		rx = -nx_norm + (-ray_x_norm) / (2 * cosine_phi)
		ry = -ny_norm + (-ray_y_norm) / (2 * cosine_phi)
		rz = -nz_norm + (-ray_z_norm) / (2 * cosine_phi)

	# trace the reflection ray
	ir, ig, ib = trace_ray(0, level - 1, x, y, z, rx, ry, rz)

	# add effect of local color
	ir = int(.7 * ir + .3 * 255)
	ig = int(.7 * ig + .3 * 0)
	ib = int(.7 * ib + .3 * 255)
	
	ir, ig, ib = get_lit_color([ir, ig, ib], [nx_norm, ny_norm, nz_norm])

	return ir, ig, ib


def put_pixel(pixel_x: int, pixel_y: int, ir: int, ig: int, ib: int):

	ir = min(ir, 244)
	ig = min(ig, 244)
	ib = min(ib, 244)
	ir = max(ir, 16)
	ig = max(ig, 16)
	ib = max(ib, 16)

	color = "#{}{}{}".format(*list(map(lambda i: str(hex(i))[2::], [ir, ig, ib])))
	surface.put(color, (pixel_x, HEIGHT - pixel_y))


def get_lit_color(base_color, normal, specular_reflectivity=[Decimal(1), Decimal(1), Decimal(1)]):
	
	global LIGHT_SOURCE_POSITION
	
	ambient_component = map(lambda k, i: k * i, base_color, AMBIENT_INTENSITY)
	
	point_intensity = LIGHT_SOURCE_COLOR
	magnitude = LIGHT_SOURCE_POSITION[0] ** 2 + LIGHT_SOURCE_POSITION[1] ** 2 + LIGHT_SOURCE_POSITION[2] ** 2
	magnitude = sqrt(magnitude)
	light_position = list(map(lambda i: Decimal(i / magnitude), LIGHT_SOURCE_POSITION))
	
	# assume normal is already normalized
	cos_fi = normal[0] * -light_position[0] + normal[1] * -light_position[1] + normal[2] * -light_position[2]
	diffuse_component = map(lambda i, k: max(Decimal(i) * Decimal(k) * -cos_fi, 0), point_intensity, base_color)
	
	zero = Decimal(0)
	
	if cos_fi == zero:
		reflection_vector = light_position
	elif cos_fi > zero:
		reflection_vector = map(lambda n, l: n - (-l / (2*cos_fi)), normal, light_position)
	else:
		reflection_vector = map(lambda n, l: (n * -1) + (-l / (2*cos_fi)), normal, light_position)
	
	reflection_vector = list(reflection_vector)
	magnitude = reflection_vector[0] ** 2 + reflection_vector[1] ** 2 + reflection_vector[2] ** 2
	magnitude = magnitude.sqrt()
	reflection_vector = list(map(lambda i: i / magnitude, reflection_vector))
	cos_theta = VIEW_VECTOR[0] * reflection_vector[0] + VIEW_VECTOR[1] * reflection_vector[1] + VIEW_VECTOR[2] * reflection_vector[2]
	specular_component = map(lambda i, k: 255 * (max(Decimal(i) * k * cos_theta, 0) ** SPECULAR_N), point_intensity, specular_reflectivity)
	
	return list(map(lambda a, b, c: int(Decimal(a) + b + c), ambient_component, diffuse_component, specular_component))


# MAIN ########################################

WIDTH = 600
HEIGHT = 400

DEPTH = 2

BOARD_POSITION = [0, -200, 0]

SPHERE1_POSITION = [-50, -150, 400]
SPHERE1_RADIUS = 50

SPHERE2_POSITION = [100, -100, 500]
SPHERE2_RADIUS = 100

AMBIENT_INTENSITY = [0.4, 0.4, 0.4]
LIGHT_SOURCE_COLOR = [1.0, 1.0, 1.0]
LIGHT_SOURCE_POSITION = [1.0, 1.0, -1.0]

VIEW_VECTOR = [Decimal(0), Decimal(0), Decimal(1)]
SPECULAR_N = Decimal(7)

root = Tk()

outer_frame = Frame(root)
outer_frame.pack()

w = Canvas(outer_frame, width=WIDTH, height=HEIGHT)
w.pack()

surface = PhotoImage(width=WIDTH, height=HEIGHT)
w.create_image((int(WIDTH / 2), int(HEIGHT / 2)), image=surface)

render_button = Button(outer_frame, text="Render", command=render)
render_button.pack()

quit_button = Button(outer_frame, text="Quit", command=quit)
quit_button.pack()

render()

root.mainloop()
