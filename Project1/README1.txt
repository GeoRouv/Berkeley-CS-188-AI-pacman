The first 6 out of 8 queries were implemented.

search.py:

-The Node class proposed by the class assistants was not used. Instead of a node, I push into the structure of each algorithm a tuple containing the state
of each node and the actions that have been done there (for DFS-BFS that).

-UCS is pushing a tuple containing the previous tuple mentioned, plus the
path cost to there.

-In A * i push a tuple containing the previous tuple mentioned, plus
(path cost up to the heuristic value of the junction).

-In each algorithm, before I push a node, I check if it has been revisited before.

-All implementations were done according to the slides "Search in Graph" of the course.

searchAgents.py:

-The class of question 5 was completed as requested.

-For Question 6, I'm calculating the Manhattan distance from the current position-state I'm in
to the nearest corner of the grid each time and return it as a heuristic value h.

-For Question 7, although the implementation is unsuccessful, I assume that the heuristic value h
we are looking for is the Manhattan distance between the position we are and the closest position where there is food.

More comments in the code.