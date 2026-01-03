# systematic pattern to achieve longest snake
# todo - skip ahead if the apple is either far away or behind 
#        and the snake length would still fit
change_hat(Hats.Gray_Hat)
clear()
change_hat(Hats.Dinosaur_Hat)
while True:
	move(North)
	for i in range(get_world_size()):
		x = i
		for j in range(get_world_size()-2):
			if x % 2 == 0:
				y = j + 1
			else:
				y = get_world_size() - j - 1
			# move
			if x % 2 == 0:
				if not move(North):
					change_hat(Hats.Gray_Hat)
					change_hat(Hats.Dinosaur_Hat)
			else:
				if not move(South):
					change_hat(Hats.Gray_Hat)
					change_hat(Hats.Dinosaur_Hat)
		if i < get_world_size() - 1:					
			move(East)
	#move back
	move(South)
	for x in range(get_world_size()-1):
		move(West)
