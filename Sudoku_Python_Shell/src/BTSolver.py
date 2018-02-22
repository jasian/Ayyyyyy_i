import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time

from collections import defaultdict
class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork.ConstraintNetwork(gb)
        self.hassolution = False
        self.gameboard = gb
        self.trail = trail

        self.varHeuristics = var_sh
        self.valHeuristics = val_sh
        self.cChecks = cc
        self.FCFlag = False

    # ==================================================================
    # Consistency Checks
    # ==================================================================

    # Basic consistency check, no propagation done
    def assignmentsCheck ( self ):
        for c in self.network.getConstraints():
            if not c.isConsistent():
                return False
        return True

    """
        Part 1 TODO: Implement the Forward Checking Heuristic

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        Note: remember to trail.push variables before you change their domain
        Return: true is assignment is consistent, false otherwise
    """
    def forwardChecking ( self ):
        print("ENTER: forwardChecking Function");
        print(self.gameboard);
        
        #if forwardChecking() hasn't been called yet then FCFlag = False
        if (self.FCFlag == False):
            print("flag is false");
            constraints = self.network.getModifiedConstraints();
            for constraint in constraints:
                #return false if domain == 0 
                if not constraint.isConsistent():
                    return False;
                
                print(str(constraint));
                
                #Collecting all the values that are preassigned
                valuesToRemove = [];
                for v in constraint.vars:
#                     print ("v.getValues() = ", v.getValues());
                    if (len(v.getValues()) == 1):
                        valuesToRemove.append(v.getValues()[0]);
                
#                 print("valuesToRemove: ", valuesToRemove);            
                #start deleting from neighbor's domains
                for v in constraint.vars:
                    for toRemoveValue in valuesToRemove:
                        #before you remove you push into the trail
                        self.trail.placeTrailMarker();
                        self.trail.push( v );
                        
                        #Return false if the value you want to remove is the only one left in domain
                        #Therefore, the domain would've been 0
#                         if (len(v.getValues()) == 1 and v.getValues()[0] == toRemoveValue):
#                             return False;
                        
                        v.removeValueFromDomain(toRemoveValue);
            print("end of changing preassigned variables")            
            #First loop is officially done and all preassigned values are set
            self.FCFlag = True;
        
        #every other call 
        else:
            print("flag is True");
            constraints = self.network.getModifiedConstraints();
            for constraint in constraints:
                print(str(constraint));
                if not constraint.isConsistent():
                    return False;
                                #Collecting all the values that are preassigned
                valuesToRemove = [];
                for v in constraint.vars:
#                     print ("v.getValues() = ", v.getValues());
                    if (v.isModified()):
                        print("this value is modified: ", str(v));
                        valuesToRemove.append(v.getValues()[0]);
                
#                 print("valuesToRemove: ", valuesToRemove);            
                #start deleting from neighbor's domains
                for v in constraint.vars:
                    for toRemoveValue in valuesToRemove:
                        #before you remove you push into the trail
                        self.trail.placeTrailMarker();
                        self.trail.push( v );
                        
                        #Return false if the value you want to remove is the only one left in domain
                        #Therefore, the domain would've been 0
#                         if (len(v.getValues()) == 1 and v.getValues()[0] == toRemoveValue):
#                             return False;
                        v.removeValueFromDomain(toRemoveValue);
                #delete first value that is modified
#                 valueToRemove = constraint.vars[0];
#                 self.trail.placeTrailMarker();
#                 self.trail.push(valueToRemove );
#                 v.removeValueFromDomain(toRemoveValue);
                
#                 for v in constraint.vars:
#                     print ("v.getValues() = ", v.getValues());
                                
        print("END OF: forwardChecking Function");

        return True

    """
        Part 2 TODO: Implement both of Norvig's Heuristics

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        (2) If a constraint has only one possible place for a value
            then put the value there.

        Note: remember to trail.push variables before you change their domain
        Return: true is assignment is consistent, false otherwise
    """
    def norvigCheck ( self ):
        return False

    """
         Optional TODO: Implement your own advanced Constraint Propagation

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournCC ( self ):
        return None

    # ==================================================================
    # Variable Selectors
    # ==================================================================

    # Basic variable selector, returns first unassigned variable
    def getfirstUnassignedVariable ( self ):
        for v in self.network.variables:
            if not v.isAssigned():
                return v

        # Everything is assigned
        return None

    """
        Part 1 TODO: Implement the Minimum Remaining Value Heuristic

        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):
        min_variable = self.getfirstUnassignedVariable();
        for v in self.network.variables:
            if not v.isAssigned():
                if (v.size() < min_variable.size()):
                    min_variable = v;
        
        return min_variable;
                    

#         # Everything is assigned
#         return None

    """
        Part 2 TODO: Implement the Degree Heuristic

        Return: The unassigned variable with the most unassigned neighbors
    """
    def getDegree ( self ):
        return None

    """
        Part 2 TODO: Implement the Minimum Remaining Value Heuristic
                       with Degree Heuristic as a Tie Breaker

        Return: The unassigned variable with, first, the smallest domain
                and, second, the most unassigned neighbors
    """
    def MRVwithTieBreaker ( self ):
        return None

    """
         Optional TODO: Implement your own advanced Variable Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVar ( self ):
        return None

    # ==================================================================
    # Value Selectors
    # ==================================================================

    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Part 1 TODO: Implement the Least Constraining Value Heuristic

        The Least constraining value is the one that will knock the least
        values out of it's neighbors domain.

        Return: A list of v's domain sorted by the LCV heuristic
                The LCV is first and the MCV is last
    """
    def getValuesLCVOrder ( self, v ):
        domain_freq = defaultdict(int);
        neighbors = self.network.getNeighborsOfVariable(v); #neighbors that share a constraint
        for neighbor in neighbors: 
            for value in neighbor.getValues():
                domain_freq[value] += 1;
        
#         print("before, ", lil_dict); 
        sorted_dict = sorted(domain_freq.items(), key = lambda x:x[1]);
        result = [value[0] for value in sorted_dict]; 
        
        print(self.gameboard);
#         print("after, ", sorted_dict);
#         print("result, ", result);
        return result;
        #return sorted_dict;

    """
         Optional TODO: Implement your own advanced Value Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVal ( self, v ):
        return None

    # ==================================================================
    # Engine Functions
    # ==================================================================

    def solve ( self ):
        if self.hassolution:
            return

        # Variable Selection
        v = self.selectNextVariable()

        # check if the assigment is complete
        if ( v == None ):
            for var in self.network.variables:

                # If all variables haven't been assigned
                if not var.isAssigned():
                    print ( "Error" )

            # Success
            self.hassolution = True
            return

        # Attempt to assign a value
        for i in self.getNextValues( v ):

            # Store place in trail and push variable's state on trail
            self.trail.placeTrailMarker()
            self.trail.push( v )

            # Assign the value
            v.assignValue( i )

            # Propagate constraints, check consistency, recurse
            if self.checkConsistency():
                self.solve()

            # If this assignment succeeded, return
            if self.hassolution:
                return

            # Otherwise backtrack
            self.trail.undo()

    def checkConsistency ( self ):
        if self.cChecks == "forwardChecking":
            return self.forwardChecking()

        if self.cChecks == "norvigCheck":
            return self.norvigCheck()

        if self.cChecks == "tournCC":
            return self.getTournCC()

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "Degree":
            return self.getDegree()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()

        if self.varHeuristics == "tournVar":
            return self.getTournVar()

        else:
            return self.getfirstUnassignedVariable()

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )

        if self.valHeuristics == "tournVal":
            return self.getTournVal( v )

        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)