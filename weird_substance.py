# script to grind the harvest of weird substance
clear()

def farm():
	while True:
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				if can_harvest():
					harvest()
				if get_entity_type() == Entities.Grass:
					till()
				plant(Entities.Grass)
				use_item(Items.Fertilizer)
				#move
				move(North)

for _ in range(max_drones()):
	if spawn_drone(farm):
		move(East)
farm()
