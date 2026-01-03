# parallel insert sort for cactus harvest
clear()

def plant_field():
	for _ in range(get_world_size()):
		if get_entity_type() == Entities.Grass:
			till()
		plant(Entities.Cactus)
		move(East)

def sort_row():
	x = 0
	while x < get_world_size() - 1:
		cur = measure()
		next = measure(East)
		if next < cur:
			swap(East)
			# go back one and try again
			if x > 0:
				move(West)
				x -= 1
		else:
			move(East)
			x += 1

def sort_col():
	y = get_world_size() - 1
	while y > 0:
		cur = measure()
		next = measure(South)
		if next > cur:
			swap(South)
			# go back one and try again
			if y < get_world_size() - 1:
				move(North)
				y += 1
		else:
			move(South)
			y -= 1

def harvest_all():
	for _ in range(get_world_size()):
		for _ in range(get_world_size()):
			harvest()
			move(South)
		move(West)

def go_home():
	x = get_pos_x()
	y = get_pos_y()
	for _ in range(y):
		move(South)
	for _ in range(x):
		move(West)

while True:
	# go home
	go_home()
	
	# plant cactus
	handles = []
	for _ in range(max_drones()):
		hnd = spawn_drone(plant_field)
		if hnd != None:
			handles.append(hnd)
			move(North)
	plant_field()
	
	# wait for all the handles
	for h in handles:
		if h != None:
			wait_for(h)
	go_home()
	
	# sort rows
	handles = []
	for _ in range(max_drones()):
		hnd = spawn_drone(sort_row)
		if hnd != None:
			handles.append(hnd)
			move(North)
	sort_row()
	
	# wait for all the handles
	for h in handles:
		wait_for(h)
	go_home()
	
	# sort columns
	move(South)
	handles = []
	for _ in range(max_drones()):
		hnd = spawn_drone(sort_col)
		if hnd != None:
			handles.append(hnd)
			move(East)
	sort_col()
	
	# wait for all the handles
	for h in handles:
		wait_for(h)
	go_home()
	
	# harvest
	harvest()
