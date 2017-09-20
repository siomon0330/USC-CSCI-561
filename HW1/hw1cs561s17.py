import sys
import collections
from collections import OrderedDict

#read the input information from the input file
inputFile = open(sys.argv[2], 'r')

#get the algorithm
algorithm = inputFile.readline().rstrip()
#get the initial amount of fuel
amountOfFuel = int(inputFile.readline().strip())
#get the start location
startPoint = inputFile.readline().strip()
#get the destination
destination = inputFile.readline().strip()
#get the graph information
remainingFile = inputFile.readlines()
neighbours = {}

#read the graph information and store it in the neighbour list
for line in remainingFile:
    information = line.split(':')
    node = information[0]
    children = information[1].split(',')
    dic = {}
    for child in children:
        child.strip()
        childInformation = child.split('-')
        childName = childInformation[0].strip()
        childAmount = int(childInformation[1])
        dic[childName] = childAmount

    neighbours[node] = dic

#close the input file
inputFile.close()


def findPath(startPoint, destination, parent):
    '''
    This method is to find the path from the start point to the destination
    Args:
        start point: the start location
        destination: the destination
        parent: a map which store the information of the parent node of each node on the path
    @Returns:
             a list which is the path
    '''
    path = []
    path.append(destination)
    #find the parent node of the parent node until reach the start point
    while destination != startPoint:
        path.append(parent[destination])
        destination = parent[destination]

    #reverse the path since we start with the destination
    path.reverse()
    return path


def usedFuel(startPoint, destination, parent):
    '''
        This method is to find the path from the start point to the destination
        Args:
            start point: the start location
            destination: the destination
            parent: a map which store the information of the parent node of each node on the path
        Returns:
                an int which stands for the amount of fuel
        '''

    totalFuel = 0
    while destination != startPoint:
        parentNode = parent[destination]
        totalFuel += neighbours.get(destination)[parentNode]
        destination = parentNode

    return totalFuel


def BFS(startPoint, destination, neighbours, amountOfFuel):
    '''
        This method using breadth first search to find the path from the start point to the destination
        Args:
            start point: the start location
            destination: the destination
            neighbours: a map which store the information of graph information
            amountOfFuel: the initial amount of fuel that can be used
        @Returns:
                 a tuple with the path and remaining amount of fuel if a path can be found
                 None if there is no path
        '''

    queue = []
    queue.append(startPoint)
    explored = [] #store the nodes that have been visited
    parent = {}
    while len(queue) > 0:
        node = queue.pop(0) #pop the node from the head of the queue
        explored.append(node)

        #if we have reached the destination
        if node == destination:
            #calculate the remaining fuel
            remainingFuel = amountOfFuel - usedFuel(startPoint, destination, parent)
            #return the path and remaining fuel
            return findPath(startPoint, destination, parent), remainingFuel
        else:
            # child list is used to store the possible children that can be added to the queue later
            childList = []
            for child in neighbours.get(node, []):
                  if child not in explored and child not in queue:
                      totalFuel = 0
                      temp = node
                      #calculate the fuel that has already been used
                      while temp != startPoint:
                          parentNode = parent[temp]
                          totalFuel += neighbours.get(temp)[parentNode]
                          temp = parentNode
                      #calculate the fuel that used to get to the child node
                      fuel = neighbours.get(node)[child]
                      #only add the node that satisfy the fuel constrains
                      if amountOfFuel - totalFuel >= fuel:
                         childList.append(child)
                         #mark the parent node
                         parent[child] = node
            #sort the child list alphabetically and add them to the queue
            childList.sort()
            queue.extend(childList)




def DFS(startPoint, destination, neighbours, amountOfFuel):
    '''
        This method using depth first search to find the path from the start point to the destination
        Args:
            start point: the start location
            destination: the destination
            neighbours: a map which store the information of graph information
            amountOfFuel: the initial amount of fuel that can be used
        @Returns:
                 a tuple with the path and remaining amount of fuel if a path can be found
                 None if there is no path
        '''

    stack = []
    explored = [] #store the nodes that have been visited
    parent = {}
    stack.append(startPoint)
    while len(stack) > 0:
        node = stack.pop() #pop the node from the tail of the stack
        if node not in explored:
            explored.append(node)

            #if we reach the destination
            if node == destination:
                #calculate the remaining fuel that has already been used
                remainingFuel = amountOfFuel - usedFuel(startPoint, destination, parent)
                #return the path and the remaining fuel
                return findPath(startPoint, destination, parent), remainingFuel

            else:
                 #child list is used to store the possible children that can be added to the stack later
                 childList = []
                 for child in neighbours.get(node, []):
                     if child not in explored:
                         totalFuel = 0
                         temp =node
                         #calculate the fuel that has already used
                         while temp != startPoint:
                             parentNode = parent[temp]
                             totalFuel += neighbours.get(temp)[parentNode]
                             temp = parentNode
                         #calculate the fuel that used to reach the child node
                         fuel = neighbours.get(node)[child]
                         #only add the node that satisfy the fuel constrains
                         if amountOfFuel - totalFuel >= fuel:
                             childList.append(child)
                             parent[child] = node
                 #sort the child list alphabetically and add them to the stack
                 childList.sort()
                 childList.reverse()
                 stack.extend(childList)



def UCS(startPoint, destination, neighbours, amountOfFuel):
    '''
        This method using depth first search to find the path from the start point to the destination
        Args:
            start point: the start location
            destination: the destination
            neighbours: a map which store the information of graph information
            amountOfFuel: the initial amount of fuel that can be used
        @Returns:
                 a tuple with the path and remaining amount of fuel if a path can be found
                 None if there is no path
        '''

    pq = [] #store the node
    pqWithDistance = [] # store the node with distance to the start point
    explored = [] #store the nodes that have been visited
    parent = {}
    pqWithDistance.append(Node(startPoint, 0))
    pq.append(startPoint)



    while len(pq) > 0:
        node = pqWithDistance.pop().name
        pq.remove(node)
        explored.append(node)

        #if we reach the destination
        if node == destination:
            #calculate the remaining fuel that has already been used
            remainingFuel = amountOfFuel - usedFuel(startPoint, destination, parent)
            #return the path and the remaining fuel
            return findPath(startPoint, destination, parent), remainingFuel
        else:

          for child in neighbours.get(node, []):
              totalFuel = 0
              temp = node
              # calculate the fuel that has already used
              while temp != startPoint:
                  parentNode = parent[temp]
                  totalFuel += neighbours.get(parentNode)[temp]
                  temp = parentNode
              # calculate the fuel that used to reach the child node
              fuel = neighbours.get(node)[child]
              totalFuel += fuel

              if child not in explored and child not in pq:
                  temp = node
                  # only add the node that satisfy the fuel constrains
                  if amountOfFuel >= totalFuel:
                      pqWithDistance.append(Node(child, totalFuel))
                      pq.append(child)
                      parent[child] = node

              # update the distance of the node that is in the queue
              if child in pq:
                  for item in pqWithDistance:
                      if item.name == child:
                          if item.distance > totalFuel:
                              item.distance = totalFuel
                              parent[child] = node
          #sort the nodes in the priority queue according to their distance to the start point
          pqWithDistance.sort()



class Node(object):
    '''
    This class represents a single node with two attributes: name, and its distance to the start point
    '''
    def __init__(self, name, distance):
        self.name = name
        self.distance = distance
        
    def __str__(self):
        return str(self.__dict__)

    #compare the node according to their distance and name 
    def __cmp__(self, other):
        if self.distance == other.distance:
            return cmp(other.name, self.name)
        else:
            return cmp(other.distance, self.distance)



def do_the_output(result):
    output = open('output.txt', 'w')
    if result != None:
        path = result[0]
        write_info = ''
        for node in path:
            write_info = write_info + node + '-'
        write_info = write_info[:-1]
        write_info = write_info + " "
        write_info = write_info + str(result[1])
        output.write(write_info)
    else:
        write_info = 'No Path'
        output.write(write_info)


def process():

    if algorithm == 'BFS':

        #result is a tuple: index 0 is the path and index 1 is the remaining fuel
        result = BFS(startPoint, destination, neighbours, amountOfFuel)
        do_the_output(result)


    elif algorithm == 'DFS':
        # result is a tuple: index 0 is the path and index 1 is the remaining fuel
        result = DFS(startPoint, destination, neighbours, amountOfFuel)
        do_the_output(result)

    else:
        
        # result is a tuple: index 0 is the path and index 1 is the remaining fuel
        result = UCS(startPoint, destination, neighbours, amountOfFuel)
        do_the_output(result)



if __name__ == '__main__':
    process()














































