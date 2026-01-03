# quick way to harvest a lot of a single crop
clear()

def farm():
	while True:
		for i in range(get_world_size()):
			x = get_pos_x()
			for j in range(get_world_size()):
				y = get_pos_y()
				if get_entity_type() == Entities.Grass:
					till()
				if can_harvest():
					harvest()
				if y == 0 or y == get_world_size() -1:
					plant(Entities.Sunflower)
				else:
					plant(Entities.Carrot)
				# watering
				if num_items(Items.Water) > 0:
					if get_water() < 0.5:
						use_item(Items.Water)
				# move
				move(North)

num = max_drones()
for _ in range(num):
	spawned = spawn_drone(farm)
	if spawned:
		for x in range(get_world_size() / num):
			move(East)
farm()
