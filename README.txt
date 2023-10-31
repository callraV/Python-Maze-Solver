Maze Clearing with A*Search Algorithm

This Python code implements a Maze Solver using the A* algorithm. The solver navigates through a maze and finds the shortest path to visit all rooms with rubbish while obeying weight and size limitations for rubbish collection. The code can be executed using the following steps:

1. Upon running the code, the initial maze with predefined rubbish and disposal room locations will be displayed. The program will prompt you to modify rubbish information or add/remove disposal rooms. Follow the instructions provided by the program to make the desired changes to the maze.

2. When prompted, you can choose the following options:
Option 1: Add rubbish to a room 
Option 2: Remove rubbish from a room 
Option 3: Add a Disposal Room 
Option 4: Remove a Disposal Room 
Option 5: Exit the Modification Phase 

3. After the modification phase, you will be asked to set weight and size limitations for rubbish collection. Enter the weight limit (in kg) and size limit (in m^3) as per your requirements. 

4. The code will then find the shortest path to collect rubbish while adhering to the weight and size limitations. The selected path, rooms traversed, and rubbish disposal will be displayed. The total path cost (number of steps) will also be shown.