import heapq
from heapq import heappush, heappop

class PriorityQueue:   

    def __init__(self):
       print "Constructed a priority queue!"   
       self.entry_finder = {}               #contains all entries(tuples for items)
       self.pq=[]                           #heap for entries: items-priorities-counter
       self.counter=0                       #Position of each element

    def push(self,item, priority):
        self.counter += 1
        entry = [priority, self.counter, item]  
        self.entry_finder[item] = entry
        heappush(self.pq, entry)        
        print 'Pushed succesfully item',item,'(priority:',priority,')'

    def pop(self):
        'Remove and return the lowest priority item'
        while self.pq:
            priority, self.counter, item = heappop(self.pq)
            print 'Popped item ',item,'(priority:',priority,')','succcesfully'
            return item        
        
    def isEmpty(self):
        if self.counter==0: return 1
        else: return 0

    def update(self,item,priority):
        if item in self.entry_finder:                       #if item exists in entries/priority queue
            if priority < self.entry_finder[item][0]:       #do the update accordingly...
                print 'Changed priority of item',item,'from',self.entry_finder[item][0],'to',priority    
                self.entry_finder[item][0]=priority
                 

def PQSort(IntList):
    z=PriorityQueue()       #temporary priority queue to sort the integer list
    temp=[]                 #temporary list to return the sorted integer list
    for x in IntList:
        z.push(x,x)
    for x in IntList:
        t=z.pop()
        temp.append(t)      #sending items to temp list to return them back sorted..

    return temp


if __name__ == "__main__":
    q=PriorityQueue() 
    q.push("task3", 3)
    q.push("task3", 4)
    q.push("task2",0)
    q.update("task3",2)
    q.pop()
    q.pop()
    q.pop()
    
    print '\n'
    IntList=[0,5,2,7,4,1,3]
    x=PQSort(IntList)
    
    

