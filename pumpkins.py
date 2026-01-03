# parallel approach to getting the largest pumpkin
clear()

def plant_field():
	for _ in range(get_world_size()):
		if get_entity_type() == Entities.Grass:
			till()
		plant(Entities.Pumpkin)
		# watering
		if num_items(Items.Water) > 0:
			if get_water() < 0.5:
				use_item(Items.Water)
		move(East)

def cleanup():
	cleaned = 1
	consecutive = 0
	while consecutive < 3:
		cleaned = 0
		for _ in range(get_world_size()):
			if get_entity_type() == Entities.Dead_Pumpkin:
				plant(Entities.Pumpkin)
				cleaned += 1
				consecutive = 0
			move(East)
		if cleaned == 0:
			consecutive += 1
			

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
	
	# plant pumpkins
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
	
	# cleanup
	handles = []
	for _ in range(max_drones()):
		hnd = spawn_drone(cleanup)
		if hnd != None:
			handles.append(hnd)
			move(North)
	cleanup()
	
	# wait for all the handles
	for h in handles:
		wait_for(h)
	go_home()
	
	# wait for all the handles
	for h in handles:
		wait_for(h)
	go_home()
	
	# harvest
	harvest()
