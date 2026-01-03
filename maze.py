# maze solver
# primary features:
#  depth first search to explore maze and build a tree
#  point to origin pathing (for quick paths without searches)
#  path pruning to find closer points of intersection
#  option to change world size (smaller may offer a better balance of speed and chest payout)
#  every reexplore_rate times the maze is reexplored to find faster paths
# todo -
#  two paths are generated every turn, BUT the exact same path (but reverse) is needed for the next round
#   so reuse that path (faster?)
#  opposite direciton could be a dictionary (faster?)
#  get_index has a call to get_world_size and an check that never is used (faster?)
#  the tree operates as a single parent tree, but that is not true as the maze evolves
#  dfs init, on clear, is slow
start_over = True
on_loop = True
reexplore_rate = 50
size = get_world_size()
size = 16
substance = size * 2**(num_unlocked(Unlocks.Mazes) - 1)

max_int = 2147483648
tree = []
max_parent = -1
directions = [North,South,East,West]
coords = [(1,0),(-1,0),(0,1),(0,-1)]

#
# convert an y,x world coordinate to a 1D array index
#
def get_index(y,x):
	dim = get_world_size()
	if y < 0 or y >= dim or x < 0 or x >= dim:
		return -1
	return (y * dim) + x

#
# flip the direction
#
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

#
# check if this is a treasure and collect or respawn the treasure
#
def collect_treasure():
	entity = get_entity_type()
	if entity == Entities.Treasure:
		if on_loop:
			use_item(Items.Weird_Substance, substance)
		else:
			harvest()
		return True
	return False

#
# initialize the tree data structure
#
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

#
# depth first search of the entire maze (do not collect the treasure)
#
def dfs_explore(parent):
	x = get_pos_x()
	y = get_pos_y()
	index = get_index(y, x)
	
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
		ret = dfs_explore(dir)
		
		# check for end
		if ret < 0:
			return ret

		# move back to current position
		odir = opposite_direction(dir)
		move(odir)

		# remove from neighbors
		neighbors.pop(index_dir)
		
	return 0

# 
# compute the path back to the origin (using parent information)
#  is_from_home: need to flip the directions (eg going the opposite direction to current location)
#  prune: find parts of the path that are duplicates (eg do not need to go home every time)
#
def dfs_back_home(y,x,is_from_home,path,prune):
	path_index = 0
	while True:
		if x == 0 and y == 0:
			break
		index = get_index(y,x)
		# go to parent
		found = False
		for i in range(len(directions)):
			if tree[index][directions[i]] == max_parent:
				# go this direction
				y += coords[i][0] 
				x += coords[i][1]
				dir = directions[i]
				if is_from_home:
					dir = opposite_direction(dir)
				path.insert(path_index, (dir,y,x))
				found = True
				if not is_from_home:
					path_index += 1
				break
		if not found:
			print("failed to find parent")
	
	if prune and path_index > 0:
		# remove overlapping parts of the path, starting at path_index
		start = path_index - 1
		end = path_index
		length = len(path)
		# find all the matches y = [1], x = [2]
		matches = 0
		while start >= 0 and end < length and path[start][1] == path[end][1] and path[start][2] == path[end][2]:
			start -= 1
			end += 1
			matches += 1
		# the junction point is always a match, so subtract that
		matches -= 1
		start += 2
		if matches > 0:
			# add a prune hint to the path
			path.append((None,start,matches*2))

	return path

#
# get the path back home and then to the destination
#
def dfs_get_path(dy,dx):
	# dx destination
	# dy destination
	# path to append too
	# return a stack of moves to the next destination
	x = get_pos_x()
	y = get_pos_y()
	
	# traverse from the destination back home (but insert forward movement)
	path = dfs_back_home(dy,dx,True,[],False)
	
	# traverse parents back up to home
	path = dfs_back_home(y,x,False,path,True)

	return path

#
# follow the path
#  prune: prunning information is encoded as a None element which is last in the array
#
def dfs_traverse_path(path,get_treasure):
	length = len(path)
	if length > 0:
		# check for prunning
		start = -1
		skip = 0
		if path[length-1][0] == None:
			start = path[length-1][1]
			skip = path[length-1][2]
		# follow these directions
		i = 0
		while i < length:
			tup = path[i]
			dir = tup[0]
			if i == start:
				i += skip
			else:
				if dir != None and not move(dir):
					print("failed to move")
				i += 1
			
	if get_treasure and not collect_treasure():
		print("failed to get treasure")

#
# init, explore, and run 300 times
#
while True:
	if start_over:
		clear()
		till()
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, substance)
		
	# initialize the tree structure
	dfs_init()
	
	# explore the maze
	dfs_explore(None)
	
	for i in range(300):
		if reexplore_rate > 0 and i > 0 and i % reexplore_rate == 0:
			# go home
			y = get_pos_y()
			x = get_pos_x()
			path = dfs_back_home(y,x,False,[],False)
			dfs_traverse_path(path,False)
			# reexplore the maze
			dfs_init()
			dfs_explore(None)
		
		# to treasure (first go home)
		x,y = measure()
		path = dfs_get_path(y,x)
		
		# move to the destination
		dfs_traverse_path(path,True)	
