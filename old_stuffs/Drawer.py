# Class example. A class is nothing more than a way to wrap a bunch of
# variables and functions together under one 'roof'. Objects of a function
# have access to all the members (variables) of the class and can call
# the methods (functions) associated with the class. Here we have a class:
# Drawer. Drawer objects have 3 members: numForks, numSpoons, and
# numSpatulas. Representing (obviosuly) the number of forks, spoons, and
# spatulas associated with an object. Drawer objects also have 1 method
# addFork() which will increment the number of forks they have by 1.

class Drawer:
    # this is the 'constructor' for our class. when we make an object of
    # this class we will run this method
    def __init__(self, numForks, numSpoons, numSpatulas):
        # self.numForks is a 'member' of class Drawer
        # this means it is a variable that is associated with this class
        # all objects of this class will have access to these variables
        # In this line we assign the number of forks that was passed to the
        # constuctor to this variable
        self.numForks = numForks
        # obviously same thing here...but these are spoons
        self.numSpoons = numSpoons
        # you guessed it...these are spatulas
        self.numSpatulas = numSpatulas


    # this is a 'class method'. this means every object of this class
    # can call this method. it will increase the fork count of this object
    # by...one
    def addFork(self):
        self.numForks += 1

    # Lets print the contents of the drawer. We will give it the 'id' of the
    # drawer so we know what the hell we're printing.
    def printContents(self, drawerID):
        print 'drawer%s contains %s forks, %s spoons and %s spatulas' % \
            (drawerID, self.numForks, self.numSpoons, self.numSpatulas)

def main():
    # let's make a Drawer object. Imagine this is a drawer in your kitchen.
    # You have lots of drawers in your kitchen, this particular one has 5
    # forks, 7 spoons, and no spatulas
    drawer0 = Drawer(5,7,0)
    # lets print out the contents of the drawer. We could access each of the
    # objects members.
    print 'Drawer0: %s forks, %s spoons and %s spatulas' % \
        (drawer0.numForks, drawer0.numSpoons, drawer0.numSpatulas)

    # But wait! Drawer objects have a method to do this...why dont we use that?
    drawer0.printContents(0)

    # Now let's make another drawer for your kitchen. This one doesn't have
    # forks and spoons...but a shit load of spatulas
    drawer1 = Drawer(0,0,100)
    
    # Better check whats in it
    drawer1.printContents(1)

    # Hey look! You've bought a new fork. Maybe you will put it with the
    # spatulas...
    drawer1.addFork()

    # Let's check whats in drawer1 again...
    drawer1.printContents(1)

    # drawer0 and drawer1 are objects of class Drawer. They each have their
    # own variables numForks, numSpoons and numSpatulas. Both objects can
    # call addFork() and printContents()

    # Does this line work?? Why / why not?
    # printContents()

if __name__ == '__main__':
    main()
