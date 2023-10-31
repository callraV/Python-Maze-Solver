import numpy as np
import heapq  # priority queue

 

#----------------------------CREATE MAZE---------------------------------------

 


class Room:

 

  def __init__(self):
    self.neighbors = []
    self.rubbish = [0, 0]  # size, weight
    self.disposal_room = False

 


class MazeSolver:

 

  def __init__(self):
    self.maze = []

 

  def create_maze(self, rows, columns):
    self.maze = np.empty((rows, columns), dtype=object)
    for row in range(rows):
      for column in range(columns):
        neighbors = []
        if column % 2 == 0:  # Even columns
          if row > 0:
            neighbors.append(["Top", (row - 1, column)])  # Top
          if row < rows - 1:
            neighbors.append(["Bottom", (row + 1, column)])  # Bottom

 

          if column > 0:
            neighbors.append(["Left", (row, column - 1)])  # Left
            if row < rows - 1:
              neighbors.append(["Bottom Left",
                                (row + 1, column - 1)])  # Bottom Left

 

          if column < columns - 1:
            neighbors.append(["Right", (row, column + 1)])  # Right
            if row < rows - 1:
              neighbors.append(["Bottom Right",
                                (row + 1, column + 1)])  # Bottom Right
        else:  # Odd columns
          if row > 0:
            neighbors.append(["Top", (row - 1, column)])  # Top
          if row < rows - 1:
            neighbors.append(["Bottom", (row + 1, column)])  # Bottom

 

          if column > 0:
            neighbors.append(["Left", (row, column - 1)])  # Left
            if row > 0:
              neighbors.append(["Top Left", (row - 1, column - 1)])  # Top Left

 

          if column < columns - 1:
            neighbors.append(["Right", (row, column + 1)])  # Right
            if row > 0:
              neighbors.append(["Top Right",
                                (row - 1, column + 1)])  # Top Right

 

        self.maze[row][column] = Room()
        self.maze[row][column].neighbors = neighbors

 

    return self.maze

 

  def add_rubbish(self, room, rubbish):
    row = room[0]
    column = room[1]
    self.maze[row][column].rubbish = rubbish

  def remove_rubbish(self):
      while True:
          try:
              row = int(input("\nEnter the row of the room with rubbish to remove: "))
              column = int(input("\nEnter the column of the room with rubbish to remove: "))
              if row >= 0 and row < len(self.maze) and column >= 0 and column < len(self.maze[0]):
                  return row, column
              else:
                  print("Invalid coordinates. Please re-enter.")
          except ValueError:
              print("Invalid input. Please enter integers for row and column.")

 

  def set_disposal_room(self, row, column):
    self.maze[row][column].disposal_room = True

 

  def remove_disposal_room(self):
      while True:
          try:
              row = int(input("\nEnter the row of the disposal room to remove: "))
              column = int(input("\nEnter the column of the disposal room to remove: "))
              if row >= 0 and row < len(self.maze) and column >= 0 and column < len(self.maze[0]):
                  return row, column
              else:
                  print("Invalid coordinates. Please re-enter.")
          except ValueError:
              print("Invalid input. Please enter integers for row and column.")

 

  def display_maze(self):
    for row in self.maze:
      for room in row:
        print(room.rubbish, end="")
      print()

 

  def get_neighbors(self, room):  # FOR CHECKING if there is any teleportation
    row, column = room
    neighbors = []

 

    for neighbor in self.maze[row][column].neighbors:
      neighbors.append(neighbor)

 

    return neighbors

 

  def get_rubbish(self, room):
    row, column = room
    return self.maze[row][column].rubbish

 

  def get_rubbish_locations(self):
    rubbish_locations = []
    for row in range(len(self.maze)):
      for column in range(len(self.maze[0])):
        if self.maze[row][column].rubbish != [0, 0]:
          rubbish_locations.append((row, column))
    return rubbish_locations



  def get_disposal_rooms(self):
    disposal_rooms = []
    for row in range(len(self.maze)):
      for column in range(len(self.maze[0])):
        if self.maze[row][column].disposal_room:
          disposal_rooms.append((row, column))
    return disposal_rooms



#----------------------------A* ALGORITHM---------------------------------------

 

#--------------------------HEURISTIC--------------------------

 

  def heuristic(self, room, target):
    return abs(room[0] - target[0]) + abs(room[1] - target[1])  # Manhattan distance

 

#------------------------RUBBISH-----------------------------

 

  def get_closest_rubbish(self, room):  # find the closest rubbish
    closest_rubbish = None
    min_distance = float("inf")  # unknown distance is set to infinity

 

    for row, column in self.get_rubbish_locations():
      distance = self.heuristic(room,
                                (row, column))  # find distance using heuristic
      if distance < min_distance:
        min_distance = distance
        closest_rubbish = (row, column)

 

    return closest_rubbish

 

  def shortest_path_to_rubbish(self,
                               start, current_weight, current_size):  # find path to the closest rubbish
    priority_queue = []
    heapq.heappush(priority_queue, (0, start, []))
    visited = set()

 

    while priority_queue:
      _, current_room, path = heapq.heappop(priority_queue)
      if current_room in visited:
        continue

 

      visited.add(current_room)

 

      if self.get_rubbish(current_room) != [0, 0]:
        return path + [(current_room, self.get_rubbish(current_room))]

 

      neighbors = self.get_neighbors(current_room)
      for direction, next_room in neighbors:
        if next_room not in visited:
          next_path = path + [(next_room, self.get_rubbish(next_room))
                              ]  # G-SCORE
          priority = len(next_path) + self.heuristic(
            next_room, self.get_closest_rubbish(
              next_room))  # F-SCORE = g-score + heuristic
          heapq.heappush(priority_queue, (priority, next_room, next_path))

 

    return None

 

#-----------------------DISPOSAL ROOM----------------------------

 

  def get_closest_disposal(self, room):  # find the closest disposal
    closest_disposal = None
    min_distance = float("inf")  # unknown distance is set to infinity

 

    for row, column in self.get_disposal_rooms():
      distance = self.heuristic(room,
                                (row, column))  # find distance using heuristic
      if distance < min_distance:
        min_distance = distance
        closest_disposal = (row, column)

 

    return closest_disposal

 

  def shortest_path_to_disposal(self,
                                start):  # find path to the closest disposal
    priority_queue = []
    heapq.heappush(priority_queue, (0, start, []))
    visited = set()

 

    while priority_queue:
      _, current_room, path = heapq.heappop(priority_queue)
      if current_room in visited:
        continue

 

      visited.add(current_room)

 

      if self.maze[current_room[0]][current_room[1]].disposal_room:
        return path + [current_room]

 

      neighbors = self.get_neighbors(current_room)
      for direction, next_room in neighbors:
        if next_room not in visited:
          next_path = path + [current_room]  # G-SC0RE
          priority = len(next_path) + self.heuristic(
            next_room, self.get_closest_disposal(
              next_room))  # F-SCORE = g-score + heuristic
          heapq.heappush(priority_queue, (priority, next_room, next_path))

 

    return None

 


#----------------------------SET THE MAZE--------------------------------------

 

# Create a maze solver instance
solver = MazeSolver()

 

# Create maze
maze = solver.create_maze(6, 9)

 

# Add rubbish ([row, column], [size, weight])
solver.add_rubbish([5, 0], [10, 1])
solver.add_rubbish([3, 1], [30, 3])
solver.add_rubbish([2, 2], [5, 1])
solver.add_rubbish([1, 3], [5, 1])
solver.add_rubbish([4, 3], [5, 2])
solver.add_rubbish([2, 4], [10, 2])
solver.add_rubbish([4, 4], [20, 1])
solver.add_rubbish([1, 6], [10, 2])
solver.add_rubbish([4, 6], [5, 2])
solver.add_rubbish([0, 7], [30, 1])
solver.add_rubbish([3, 7], [20, 2])
solver.add_rubbish([1, 8], [10, 3])

 

# Set disposal room's location (row, column)
solver.set_disposal_room(0, 5)
solver.set_disposal_room(5, 2)
solver.set_disposal_room(5, 8)

 

# Print the initial map
print("Initial Map:")
solver.display_maze()

 

# Get disposal rooms locations
disposal_rooms = solver.get_disposal_rooms()

 

print("\nDisposal rooms' locations:")
print(disposal_rooms)

 

# Get rubbish locations and total
rubbish_locations = solver.get_rubbish_locations()

 

print("\nRubbish' locations:")
print(rubbish_locations)

 

print("\nTotal number of rubbish:")
print(len(rubbish_locations))

 

# Get user input for adding or removing rubbish, and adding or removing disposal rooms
while True:
    option = input("\nDo you wish to modify rubbish info or add/remove disposal room? (Enter 1/2/3/4/5) \n 1 - add rubbish \n 2 - remove rubbish \n 3 - add disposal room \n 4 - remove disposal room \n 5 - no/done \nChoice:")

    if option == '1':
        while True:
            try:
                room_input = input("Enter the row and column of the room to add rubbish (Please use comma to separate the values, e.g., 4,1): ").split(",")
                if len(room_input) == 2:
                    room = [int(val) for val in room_input]
                    if 0 <= room[0] < len(solver.maze) and 0 <= room[1] < len(solver.maze[0]):
                        break
                    else:
                        print("Invalid coordinates. Please re-enter.")
                else:
                    print("Invalid input. Please enter both row and column separated by a comma.")
            except ValueError:
                print("Invalid input. Please re-enter.")
    
        while True:
            try:
                rubbish_input = input("Enter the rubbish info [weight, size] (Please use comma to separate the values, e.g., 20,4): ").split(",")
                if len(rubbish_input) == 2:
                    rubbish = [int(val) for val in rubbish_input]
                    break
                else:
                    print("Invalid input. Please enter both weight and size separated by a comma.")
            except ValueError:
                print("Invalid input. Please re-enter.")
    
        solver.add_rubbish(room, rubbish)
        rubbish_locations = solver.get_rubbish_locations()




    elif option == '2':
        row, column =solver.remove_rubbish()
        solver.add_rubbish([row, column], [0, 0])
        rubbish_locations = solver.get_rubbish_locations()

 

    elif option == '3':
        while True:
            try:
                row, column = [int(x) for x in input("Enter the row and column of the room to add disposal room (Please use comma to seperate the values): ").split(",")]
                if row >= 0 and row < len(solver.maze) and column >= 0 and column < len(solver.maze[0]):
                  solver.set_disposal_room(row, column)
                  break
                else:
                  print("Invalid coordinates. Please re-enter")
            except ValueError:
                print("Invalid input. Please re-enter.")
        disposal_room = solver.get_disposal_rooms()

    elif option == '4':
        row, column = solver.remove_disposal_room()
        solver.maze[row][column].disposal_room = False
        disposal_room = solver.get_disposal_rooms()

    elif option == '5':
        break

    else:
        print("Invalid option. Please re-enter.")

 


print("\nCurrent Map:")
solver.display_maze()

 

print("\nCurrent disposal rooms' locations:")
print(solver.get_disposal_rooms())

 

print("\nCurrent  Rubbish' locations:")
print(solver.get_rubbish_locations())

 

#-----------------------------FIND PATH----------------------------------------

 

# Find the shortest path to visit all rooms with rubbish
path = []
current_room = (0, 0)

 

#-----------SET LIMITATIONS (rubbish bin)------------

 

# rubbish = [weight, size]
weight_limit = int(input("\nEnter the weight limit (in kg): "))
size_limit = int(input("\nEnter the size limit (in m^3): "))
current_weight = 0
current_size = 0

 

if weight_limit < 0 or size_limit < 0:
  print("Weight and size limit needs to be more than 0")
  exit()

 

#--------------------------------------

 

print("\nSelected Path:")
print(current_room)  # starting room

 

while len(rubbish_locations
          ) > 0:  # check if theres still any rubbish still in the maze

 

  if current_weight < weight_limit and current_size < size_limit:  # check whether limit have been met
    #if limit has not been met,
    next_path = solver.shortest_path_to_rubbish(
      current_room, current_weight, current_size)  # find the rooms (path) that leads to the nearest rubbish

 

    if next_path:
      next_room, rubbish = next_path[
        0]  # extracts the next room's coordinate and the rubbish
      path.append((next_room, rubbish))  # mark room as traversed
      current_room = next_room  # move to tge bext room

 

      if solver.maze[next_room].rubbish != [
          0, 0
      ]:  # check if the next room has rubbish in it
        # if room has rubbish,
        rubbish_locations.remove(next_room)
        current_weight += solver.maze[next_room].rubbish[0]
        current_size += solver.maze[next_room].rubbish[1]
        print(
          f"{current_room} - Rubbish {solver.maze[next_room].rubbish} found! Now carrying {current_weight}kg/{current_size}m^3 rubbish."
        )
        solver.add_rubbish(next_room, [0, 0])  # clean rubbish
      elif solver.maze[
          next_room].disposal_room == True:  # check if the next room is a disposal room
        # if room is a disposal room
        print(f"{current_room} - Disposal room found! Disposing rubbish")
        current_weight = 0  # empty bin
        current_size = 0
      else:
        # if its a regular room
        print(current_room)

 

  else:
    print("         Limit met! Moving to disposal room...")

 

    # Find the shortest path to the nearest disposal room
    disposal_path = solver.shortest_path_to_disposal(current_room)
    del disposal_path[0]

 

    # Print the shortest path to the nearest disposal room
    for room in disposal_path:
      path.append(room)
      if solver.maze[room].disposal_room == True:
        print(f"{room} - Disposal room found! Disposing rubbish")
        current_weight = 0
        current_size = 0
        current_room = room
        continue
      else:
        print(room)

 

# Navigate to disposal room one last time if there's no more rubbish
print(
  "         No more rubbish in maze! Moving to disposal room one last time...")
disposal_path = solver.shortest_path_to_disposal(current_room)
del disposal_path[0]

 

for room in disposal_path:
  path.append(room)
  if solver.maze[room].disposal_room == True:
    print(f"{room} - Disposal room found! Disposing rubbish")
  else:
    print(room)

 

print(f"\nTotal path cost: {len(path)}")
print("\nProblem solved. Exitting program...")