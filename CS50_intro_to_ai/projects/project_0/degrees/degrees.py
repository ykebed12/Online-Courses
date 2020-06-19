import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
# "Jon Doe" -> 23421
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
# 1242 -> {name: "john", birth: bday, movies: [2133,3142,13134]}
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
# 
movies = {}

# keep track of people visited
vstd_people = []

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

def reverse_path(node):
    """
    Returns the solution of the shortest_path given the target node
    by traversing up the parent nodes and inserting them into a list
    until it reaches a "NoneType" parent.
    """
    path_lst = []
    
    # Loop that adds each node to the list with each element as this
    # format: (movie_id, person_id)
    while node is not None:
        path_lst = [(node.action, node.state)] + path_lst
        node = node.parent
    
    return path_lst

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    
    Function that gets a path from source to target using
    breadth first search (Graph) where the source and target
    are person_ids that represent "nodes" and the movies
    are represented as the path.
    """
    
    # If source is target, there are 0 degrees of separation
    if source == target:
        return []

    queue = QueueFrontier()     # Queue is used to keep neighboring nodes
    visited_people = []         # Keeps visited person_id's/"nodes"
    parent_node = None          # First node is None, Dummy node

    # Loop that looks at nieghboring nodes, of each visited node until
    # it finds 
    while True:

        # add neighbors to queue as node structures IF not visited before 
        for (movie_id, person_id) in neighbors_for_person(source):
            if person_id not in visited_people:
                queue.add(Node(person_id, parent_node, movie_id))

        # Solution does not exist if queue is empty so exit the loop
        if queue.empty():
            break
        
        # pop node from queue
        node = queue.remove()

        if node.state == target:
            # Solution found so exit loop and return solution
            return reverse_path(node)
        else:
            # Solution not found yet, so set node as parent_node then
            # add the node to visited nodes and search next neighbors
            parent_node = node
            source = node.state
            visited_people.append(node.state)
    
    # No possible path
    return None

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
