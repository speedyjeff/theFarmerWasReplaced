# maze solver
# primary features:
#  depth first search to explore maze and build a tree
#  point to origin pathing (for quick paths without searches)
#  finding common pivot point in paths to avoid backtracking
#  option to change world size (smaller may offer a better balance of speed and chest payout)
#  every reexplore_rate times the maze is reexplored to find faster paths
# todo -
#  the tree operates as a single parent tree, but that is not true as the maze evolves
#   once the maze evolves it is more like a graph and less like a tree
start_over = True
on_loop = True
is_simulation = False
reexplore_rate = 400
world_size = 16 # get_world_size()
substance = world_size * 2**(num_unlocked(Unlocks.Mazes) - 1)

tree = []
max_parent = -1
# None is parent
opposite_direction = {None:None,North:South,South:North,East:West,West:East}
coordinates = {North:(1,0),South:(-1,0),East:(0,1),West:(0,-1)}

#
# convert an y,x world coordinate to a 1D array index
#
def get_index(y,x):
	return (y * world_size) + x

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
			tree[i][None] = None
			tree[i][North] = 0
			tree[i][South] = 0
			tree[i][East] = 0
			tree[i][West] = 0	
	else:
		# generate the maze tree structure (dfs)
		for x in range(world_size):
			for y in range(world_size):
				tree.append({None:None,North: 0, South: 0, East: 0, West: 0})

#
# depth first search of the entire maze (do not collect the treasure)
#
def dfs_explore(parent):
	x = get_pos_x()
	y = get_pos_y()
	index = get_index(y, x)
	
	# mark the parent
	if parent != None:
		dir = opposite_direction[parent]
		tree[index][dir] = max_parent
		# set the first parent seen, avoid cycles
		if tree[index][None] == None:
			tree[index][None] = dir

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
		dfs_explore(dir)

		# move back to current position
		odir = opposite_direction[dir]
		move(odir)

		# remove from neighbors
		neighbors.pop(index_dir)

# 
# compute the path back to the origin (using parent information)
#
def get_path_home(y,x):
	path = []
	while True:
		if x == 0 and y == 0:
			break
		index = get_index(y,x)
		dir = tree[index][None]
		if dir == None:
			print("failed to find parent")
		else:
			# go this direction
			y += coordinates[dir][0] 
			x += coordinates[dir][1]
			path.append((dir,y,x))
			
	return path

#
# identify the common part of these two paths (may be origin)
#
def find_pivot_point(path1,path2):
	# indicate overlapping parts of the paths - find the pivot point
	# the end of the paths is origin, so compare the ends of these paths
	i1 = len(path1) - 1
	i2 = len(path2) - 1
	# find all the matches y = [1], x = [2]
	matches = 0
	while i1 >= 0 and i2 >= 0 and path1[i1][1] == path2[i2][1] and path1[i1][2] == path2[i2][2]:
		i1 -= 1
		i2 -= 1
		matches += 1
	# the junction point is always a match, so subtract that
	matches -= 1
	i1 += 2
	i2 += 1	

	if matches > 0:
		return (matches, i1, i2)
	else:
		return (0,-1,-1)

#
# follow the path away from origin
#  pivot_start: starting point of the pivot
# 
def traverse_away_from_origin(path,pivot_start):
	# traverse against the stream of the path away from origin (eg starting point is origin*)
	length = len(path)
	if length > 0:
		i = length - 1
		# check for prunning
		if pivot_start >= 0:
			i = pivot_start
		# follow these directions
		while i >= 0:
			tup = path[i]
			dir = tup[0]
			# get the opposite direction
			dir = opposite_direction[dir]
			if dir != None and not move(dir):
				print("failed to move")
			i -= 1
			
	if not collect_treasure():
		print("failed to get treasure")

# 
# follow the path towards origin
#  pivot_start: starting point of the pivot_start
#  skip: number of paths entries to skip
#
def traverse_to_origin(path,pivot_start,skip):
	# traverse the path in the direction stored (eg follow parent info)
	length = len(path)
	if length > 0:
		# follow these directions
		i = 0
		while i < length:
			tup = path[i]
			dir = tup[0]
			if i == pivot_start:
				i += 1 + skip
			else:
				if dir != None and not move(dir):
					print("failed to move")
				i += 1

#
# init, explore, and run 300 times
#
done = False
while not done:
	if start_over:
		clear()
		till()
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, substance)
		
	# initialize the tree structure
	dfs_init()
	
	# explore the maze
	dfs_explore(None)
	
	from_current = []
	from_treasure = []
	for i in range(300):
		if reexplore_rate > 0 and i > 0 and i % reexplore_rate == 0:
			# go home
			traverse_to_origin(from_current,-1,0)
			# reexplore the maze
			dfs_init()
			dfs_explore(None)
			from_current = []
		
		# get path to treasure
		x,y = measure()
		from_treasure = get_path_home(y,x)
		
		# find the common pivot point
		matches,current_start,treasure_start = find_pivot_point(from_current,from_treasure)
		
		# move to treasure
		traverse_to_origin(from_current,current_start,matches)
		traverse_away_from_origin(from_treasure,treasure_start)

		# set path home
		from_current = from_treasure
		from_treasure = []
		
		# when simulating
		if is_simulation and num_items(Items.Gold) >= 9863168:
			done = True
			break
