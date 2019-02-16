from tkinter import *
from decimal import *

# METHODS #####################################


def render():

	depth = 5  # maximum ray depth
	setup_drawing_canvas()

	# center of projection
	xs, ys, zs = 0.0, 0.0, -800.0

	for pixel_x in range(1, 1201):

		screen_x = pixel_x - 600

		for pixel_y in range(1, 1201):

			screen_y = pixel_y - 600

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

		print("Maximum depth exceeded - return black.")
		return 0, 0, 0

	else:

		# check for intersection of ray with objects
		# and set rgb values corresponding to objects

		# set distance of closest object initially to a very large number
		t = 100000  # todo maybe set this to math.inf

		# initially no object has been intersected by the ray
		object_code = -1
		checkerboard_intersect,\
		t,\
		intersect_x, intersect_y, intersect_z = checkerboard_intersection(xs, ys, zs, ray_i, ray_j, ray_k, t)

		if checkerboard_intersect:

			object_code = 0
			if flag:
				print("Checkerboard intersected.")

		sphere1_intersect,\
		t,\
		intersect_x, intersect_y, intersect_z,\
		obj_normal_x, obj_normal_y, obj_normal_z = sphere1_intersection(xs, ys, zs, ray_j, ray_j, ray_k, t)

		if sphere1_intersect:

			object_code = 1
			if flag:
				print("Green sphere intersected.")

		sphere2_intersect, \
		t, \
		intersect_x, intersect_y, intersect_z, \
		obj_normal_x, obj_normal_y, obj_normal_z = sphere2_intersection(xs, ys, zs, ray_j, ray_j, ray_k, t)

		if sphere2_intersect:

			object_code = 2
			if flag:
				print("Reflective sphere intersected.")

		if object_code == 0:
			ir, ig, ib = checkerboard_point_intensity(intersect_x, intersect_y, intersect_z)
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
							ray_x: Decimal, ray_y: Decimal, ray_z: Decimal) -> [Decimal, Decimal, Decimal]:

	# normal of plane
	a, b, c = Decimal(0), Decimal(1), Decimal(0)

	# point on plane
	x1, y1, z1 = Decimal(0), Decimal(-500), Decimal(0)

	denom = 


# BUTTONS #####################################

def render():
	pass

# MAIN ########################################
root = Tk()

outer_frame = Frame(root)
outer_frame.pack()

w = Canvas(outer_frame, width=1200, height=1200)
w.pack()

render_button = Button(outer_frame, text="Render", command=render)
render_button.pack()

quit_button = Button(outer_frame, text="Quit", command=quit)
quit_button.pack()

root.mainloop()
