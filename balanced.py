# basic script to grind for all the basic resources
clear()

def farm():
	change_hat(Hats.Top_Hat)
	while True:
		for i in range(get_world_size()):
			# col
			x = get_pos_x()
			for j in range(get_world_size()):
				y = get_pos_y()
				# harvest
				if can_harvest():
					harvest()
				# till
				if get_entity_type() == Entities.Grass:
					till()
					
				# pumpkin
				if x > 6 and y < 11:
					plant(Entities.Pumpkin)
				# trees and bushes
				elif y <= 9:
					if y % 2 == 0:
						if x % 2 == 0:
							plant(Entities.Tree)
						else:
							plant(Entities.Grass)
					else:
						if x % 2 != 0:
							plant(Entities.Tree)
						else:
							plant(Entities.Grass)
				# sunflower
				elif y >= 12 and y <= 15:
						plant(Entities.Sunflower)
				# cactus
				elif y > 15 and x < 8:
					plant(Entities.Cactus)
				# grass and carrots
				else:
					if x < 11:
						plant(Entities.Grass)
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
		for _ in range(get_world_size() / num):
			move(East)
farm()
