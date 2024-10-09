


class QuadTree:
    power = [1 << i for i in range(21)]  # Equivalent to 2^i for i in [0, 20]

    def __init__(self, n):
        self.data = 0
        self.s = n
        self.q1 = None
        self.q2 = None
        self.q3 = None
        self.q4 = None

    def __del__(self):
        # Destructor to clean up child nodes
        del self.q1
        del self.q2
        del self.q3
        del self.q4
 

    def reduce(self):
        """Consolidate the quad tree if possible."""
        # First, try to reduce each child node
        if self.q1 is not None:
            self.q1.reduce()
            self.q2.reduce()
            self.q3.reduce()
            self.q4.reduce()

        # Now check if all child nodes are leaf nodes and have the same value
        if (self.q1 is not None and self.q2 is not None and
            self.q3 is not None and self.q4 is not None and
            self.q1.data == self.q2.data == self.q3.data == self.q4.data and
            self.q1.q1 is None and self.q2.q1 is None and 
            self.q3.q1 is None and self.q4.q1 is None):

            self.data = self.q1.data
            del self.q1, self.q2, self.q3, self.q4
            self.q1 = None
            self.q2 = None
            self.q3 = None
            self.q4 = None

    def set(self, x1, y1, x2, y2, b):
        
        # Check if the entire area corresponds to this node's region
        if (x1 == 0 and y1 == 0 and 
            x2 == (self.power[self.s] - 1) and 
            y2 == (self.power[self.s] - 1)
        ):
            self.data = b
            # Clear child nodes if they exist
            if self.q1 is not None:
                del self.q1
                del self.q2
                del self.q3
                del self.q4
                self.q1 = None
                self.q2 = None
                self.q3 = None
                self.q4 = None
            
            return

        # If this node has no children yet, create them if needed
        if self.q1 is None:
            if self.data == b:
                return
            
            # Create child nodes with the same data as the current node
            self.q1 = QuadTree(self.s - 1)
            self.q1.data = self.data
            
            self.q2 = QuadTree(self.s - 1)
            self.q2.data = self.data
            
            self.q3 = QuadTree(self.s - 1)
            self.q3.data = self.data
            
            self.q4 = QuadTree(self.s - 1)
            self.q4.data = self.data

        mid = self.power[self.s - 1]  # Calculate the midpoint
        
        # Determine which quadrant to set the value in based on coordinates
        if x1 >= mid:
            if y1 >= mid:  # Bottom right quadrant
                self.q4.set(x1 - mid, y1 - mid, x2 - mid, y2 - mid, b)
                # self.reduce()
                return
            
            if y2 < mid:  # Top right quadrant
                self.q2.set(x1 - mid, y1, x2 - mid, y2, b)
                # self.reduce()
                return
            
            # Crosses middle line vertically
            self.q2.set(x1 - mid, y1, x2 - mid, mid - 1, b)
            self.q4.set(x1 - mid, 0, x2 - mid, y2 - mid, b)
            # self.reduce()
            return
        
        if x2 < mid:
            if y1 >= mid:  # Bottom left quadrant
                self.q3.set(x1, y1 - mid, x2, y2 - mid, b)
                # self.reduce()
                return
            
            if y2 < mid:  # Top left quadrant
                self.q1.set(x1, y1, x2, y2, b)
                # self.reduce()
                return
            
            # Crosses middle line vertically
            self.q1.set(x1, y1, x2, mid - 1, b)
            self.q3.set(x1, 0, x2, y2 - mid, b)
            # self.reduce()
            return
        
        if y1 >= mid:  # Crosses middle line horizontally
            self.q3.set(x1, y1 - mid, mid - 1, y2 - mid, b)
            self.q4.set(0, y1 - mid, x2 - mid, y2 - mid, b)
            # self.reduce()
            return
        
        if y2 < mid:  # Crosses middle line horizontally
            self.q1.set(x1, y1, mid - 1, y2, b)
            self.q2.set(0, y1, x2 - mid, y2, b)
            # self.reduce()
            return
        
        # Set values in all quadrants when fully contained within this node's region
        self.q1.set(x1, y1, mid - 1, mid - 1, b)
        self.q2.set(0, y1, x2 - mid, mid - 1, b)
        self.q3.set(x1, 0, mid - 1, y2 - mid, b)
        self.q4.set(0, 0, x2 - mid, y2 - mid,b)

        # Reduce tree after setting values to consolidate nodes if possible.
        # self.reduce()

    def count_nodes(self):
        """Count the number of nodes in the quadtree."""
        if self.q1 is None:
            return 1
        return 1 + self.q1.count_nodes() + self.q2.count_nodes() + self.q3.count_nodes() + self.q4.count_nodes()


    # Retrieves the value at a specific coordinate (x1, y1). It navigates through child nodes based on which quadrant contains the point.
    def get(self, x1, y1):
        if not any([self.q1, self.q2, self.q3, self.q4]):
            return self.data

        mid = (self.power[self.s]) // 2

        if x1 >= mid:
            if y1 >= mid:
                return self.q4.get(x1 - mid, y1 - mid)
            return self.q2.get(x1 - mid, y1)

        if y1 >= mid:
            return self.q3.get(x1, y1 - mid)

        return self.q1.get(x1, y1)

    # Returns the current size(s) of the quadtree node.
    def size(self):
        return self.s

    def complement(self):
        if not any([self.q1, self.q2, self.q3, self.q4]):
                # Leaf node case
                if isinstance(self.data, tuple) and len(self.data) == 3:
                    # Invert each color channel (R, G, B)
                    self.data = tuple(255 - value for value in self.data)
                return


        # Recursive complement calls on child nodes
        if self.q1:
            self.q1.complement()
        if self.q2:
            self.q2.complement()
        if self.q3:
            self.q3.complement()
        if self.q4:
            self.q4.complement()

    def resize(self, m):
        if m == self.s:
            return  # No change needed

        if m > self.s:
            self.s = m  # Increase the size

            if self.q1 is not None:  # If there are child nodes, resize them
                self.q1.resize(m - 1)
                self.q2.resize(m - 1)
                self.q3.resize(m - 1)
                self.q4.resize(m - 1)
            return

        if self.q1 is not None:  # If there are child nodes
            if m == 0:  # If resizing to zero
                x = QuadTree.power[self.s]
                if x * x <= 2 * self.m():  # Check area condition
                    self.data = 1
                else:
                    self.data = 0

                # Clear child nodes
                del self.q1, self.q2, self.q3, self.q4
                self.q1 = None
                self.q2 = None
                self.q3 = None
                self.q4 = None

                self.s = 0  # Set size to zero
                return

            # Resize child nodes recursively
            self.q1.resize(m - 1)
            self.q2.resize(m - 1)
            self.q3.resize(m - 1)
            self.q4.resize(m - 1)
            self.reduce()  # Reduce the tree if necessary (implement reduce logic as needed)

        # Finally set the new size
        self.s = m

    def area(self):
        """Calculate the area covered by this quad tree."""
        if self.q1 is not None:
            return self.q1.area() + self.q2.area() + self.q3.area() + self.q4.area()

        return QuadTree.power[self.s] ** 2 if self.data == 1 else 0

    def equate(self, Q):
        """Equate this quad tree with another.
             Example usage:
             qt1 = QuadTree(5)
             qt2 = QuadTree(5)
             qt1.set(0, 0, 31, 31, 0)    Set some values in qt1
             qt2.equate(qt1)             Equate qt2 with qt1
             qt2.print_tree()            Print the structure of qt2 to verify it matches qt1
        """

        # Copy properties from another quad tree.
        self.s = Q.s
        self.data = Q.data

        # If Q has no children, clear this node's children
        if Q.q1 is None:
            if self.q1 is not None:
                del self.q1
                del self.q2
                del self.q3
                del self.q4
                self.q1 = None
                self.q2 = None
                self.q3 = None
                self.q4 = None
            return

        # If this node has no children, create them
        if self.q1 is None:
            self.q1 = QuadTree(self.s - 1)
            self.q2 = QuadTree(self.s - 1)
            self.q3 = QuadTree(self.s - 1)
            self.q4 = QuadTree(self.s - 1)

        # Recursively equate each child node with the corresponding child from Q
        if Q.q1 is not None:
            self.q1.equate(Q.q1)
        if Q.q2 is not None:
            self.q2.equate(Q.q2)
        if Q.q3 is not None:
            self.q3.equate(Q.q3)
        if Q.q4 is not None:
            self.q4.equate(Q.q4)

    def getRect(self, x1, y1, x2, y2):
        if self.q1 is None:
            return self.data  # Return the data if it's a leaf node

        # Check if the entire area is covered by this quad tree
        if (
            x1 == 0
            and y1 == 0
            and x2 == QuadTree.power[self.s] - 1
            and y2 == QuadTree.power[self.s] - 1
        ):
            return 2  # Indicates full coverage

        mid = QuadTree.power[self.s - 1]  # Calculate the midpoint

        # Check which quadrant to call based on coordinates
        if x1 >= mid:  # Right half
            if y1 >= mid:  # Bottom right quadrant
                return self.q4.getRect(x1 - mid, y1 - mid, x2 - mid, y2 - mid)
            elif y2 < mid:  # Top right quadrant
                return self.q2.getRect(x1 - mid, y1, x2 - mid, y2)
            else:  # Crosses middle line vertically
                a = self.q2.getRect(x1 - mid, y1, x2 - mid, mid - 1)
                if a == 2:
                    return 2
                b = self.q4.getRect(x1 - mid, 0, x2 - mid, y2 - mid)
                if b != a:
                    return 2
                return a

        elif x2 < mid:  # Left half
            if y1 >= mid:  # Bottom left quadrant
                return self.q3.getRect(x1, y1 - mid, x2, y2 - mid)
            elif y2 < mid:  # Top left quadrant
                return self.q1.getRect(x1, y1, x2, y2)
            else:  # Crosses middle line vertically
                a = self.q1.getRect(x1, y1, x2, mid - 1)
                if a == 2:
                    return 2
                b = self.q3.getRect(x1, 0, x2, y2 - mid)
                if b != a:
                    return 2
                return a

        elif y1 >= mid:  # Bottom half (crosses horizontal line)
            a = self.q3.getRect(x1, y1 - mid, x2, y2 - mid)
            if a == 2:
                return 2
            b = self.q4.getRect(0, y1 - mid, x2 - mid, y2 - mid)
            if b != a:
                return 2
            return a

        elif y2 < mid:  # Top half (crosses horizontal line)
            a = self.q1.getRect(x1, y1, x2, y2)
            if a == 2:
                return 2
            b = self.q2.getRect(0, y1, x2 - mid, y2)
            if b != a:
                return 2
            return a

        # Check all quadrants for overlap and consistency
        a = self.q1.getRect(x1, y1, mid - 1, mid - 1)
        if a == 2:
            return 2

        b = self.q2.getRect(0, y1, x2 - mid, mid - 1)
        if b != a:
            return 2

        b = self.q3.getRect(x1, 0, mid - 1, y2 - mid)
        if b != a:
            return 2

        b = self.q4.getRect(0, 0, x2 - mid, y2 - mid)
        if b != a:
            return 2

        return a


    def inext(self, x1, y1, m, Q):
        a = Q.getRect(x1, y1, x1 + QuadTree.power[m] - 1, y1 + QuadTree.power[m] - 1)

        if a == 2:
            # Initialize child quadrants because the region is mixed
            self.q1 = QuadTree(self.s - 1)
            self.q2 = QuadTree(self.s - 1)
            self.q3 = QuadTree(self.s - 1)
            self.q4 = QuadTree(self.s - 1)

            # Recursive calls to fill quadrants, similar to C++ code
            if m > 0:
                self.q1.inext(x1, y1, m - 1, Q)
                self.q2.inext(x1 + QuadTree.power[m - 1], y1, m - 1, Q)
                self.q3.inext(x1, y1 + QuadTree.power[m - 1], m - 1, Q)
                self.q4.inext(x1 + QuadTree.power[m - 1], y1 + QuadTree.power[m - 1], m - 1, Q)
            return

        self.data = a
        return

    def extract(self, x1, y1, m):
        """Extract a sub-quadtree from this quad tree."""
        q = QuadTree(m)  # Create a new quadtree for the sub-region
        q.inext(x1, y1, m, self)  # Fill the new quadtree with data from the current one
        self.equate(q)  # Replace the current quadtree's data with the extracted sub-quadtree
        return self  # Return the modified current quadtree

    def print_tree(self):
        """Print the size and data of the current node and recursively print child nodes."""
        print(f"Size: {self.s}, Data: {self.data}")

        if self.q1 is not None:  # Check if any child exists
            if self.q1:
                self.q1.print_tree()  # Recursively print q1
            if self.q2:
                self.q2.print_tree()  # Recursively print q2
            if self.q3:
                self.q3.print_tree()  # Recursively print q3
            if self.q4:
                self.q4.print_tree()  # Recursively print q4


