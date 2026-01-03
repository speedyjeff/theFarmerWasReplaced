# various scratch algorithms for solving the maze
start_over = True
on_loop = True
size = get_world_size()
substance = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
if start_over:
	clear()
	till()
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance)

max_int = 2147483648
tree = []
max_parent = -1

def get_index(y,x):
	dim = get_world_size()
	if y < 0 or y >= dim or x < 0 or x >= dim:
		return -1
	return (y * dim) + x

def opposite_direction(dir) :
	if dir == North:
		return South
	elif dir == South:
		return North
	elif dir == East:
		return West
	elif dir == West:
		return East
	else:
		return None

def collect_treasure():
	entity = get_entity_type()
	if entity == Entities.Treasure:
		if on_loop:
			use_item(Items.Weird_Substance, substance)
		else:
			harvest()
		return True
	return False

def greedy():
	maze = []
	
	# reset
	for y in range(get_world_size()):
		for x in range(get_world_size()):
			maze.append(0)
	
	# solve 
	while True:
		# position
		x = get_pos_x()
		y = get_pos_y()
		
		# treasure?
		if collect_treasure():
			break
	
		# update the current position in the maze
		index = get_index(y, x)
		maze[index] += 1
	
		# get the minimum
		m = max_int
		best_dirs = []
	
		# north
		if can_move(North):
			index = get_index(y+1, x)
			if maze[index] < m:
				m = maze[index]
				best_dirs = [North]
			elif maze[index] == m:
				best_dirs.append(North)
	
		# south
		if can_move(South):
			index = get_index(y-1, x)
			if maze[index] < m:
				m = maze[index]
				best_dirs = [South]
			elif maze[index] == m:
				best_dirs.append(South)
	
		# east
		if can_move(East):
			index = get_index(y, x+1)
			if maze[index] < m:
				m = maze[index]
				best_dirs = [East]
			elif maze[index] == m:
				best_dirs.append(East)

		# west
		if can_move(West):
			index = get_index(y, x-1)
			if maze[index] < m:
				m = maze[index]
				best_dirs = [West]
			elif maze[index] == m:
				best_dirs.append(West)
	
		# choose randomly from best directions
		index = (random() * len(best_dirs)) // 1
		dir = best_dirs[index]
	
		# move in chosen direction
		if dir == None or not move(dir):
			print("failed to move")

def dfs_init():
	if len(tree) > 0:
		# clear
		for i in range(len(tree)):
			tree[i][North] = 0
			tree[i][South] = 0
			tree[i][East] = 0
			tree[i][West] = 0
	else:
		# generate the maze tree structure (dfs)
		for x in range(get_world_size()):
			for y in range(get_world_size()):
				tree.append({North: 0, South: 0, East: 0, West: 0})
	dfs(None)
	
# depth first search of maze
def dfs(parent):
	x = get_pos_x()
	y = get_pos_y()
	index = get_index(y, x)
	
	# treasure?
	if collect_treasure():
		return -1

	# mark the parent
	if parent != None:
		dir = opposite_direction(parent)
		tree[index][dir] = max_parent

	# find unvisited neighbors
	neighbors = []

	# north
	if can_move(North):
		if tree[index][North] == 0:
			neighbors.append(North)
	# south
	if can_move(South):
		if tree[index][South] == 0:
			neighbors.append(South)
	# east
	if can_move(East):
		if tree[index][East] == 0:
			neighbors.append(East)
	# west
	if can_move(West):
		if tree[index][West] == 0:
			neighbors.append(West)
   
	# visit unvisited neighbors
	while len(neighbors) > 0:
		index_dir = (random() * len(neighbors)) // 1
		dir = neighbors[index_dir]

		# mark that we have visited this neighbor
		tree[index][dir] += 1

		# move in chosen direction
		move(dir)

		# dfs on that neighbor
		ret = dfs(dir)
		
		# check for end
		if ret < 0:
			return ret

		# move back to current position
		odir = opposite_direction(dir)
		move(odir)

		# remove from neighbors
		neighbors.pop(index_dir)
		
	return 0

def random_wanderer():
	while True:
		# treasure?
		entity = get_entity_type()
		if entity == Entities.Treasure:
			harvest()
			break
		
		# random move
		ran = random() * 4 // 1
		if ran == 0 and move(North):
			continue
		if ran == 1 and move(East):
			continue
		if ran == 2 and move(West):
			continue
		if ran == 3 and move(South):
			continue

for i in range(300):
	greedy()
