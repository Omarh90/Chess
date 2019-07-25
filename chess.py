

"""
Chess Traversal Chess Board Function:

Calculates shortest distance piece must traverse on chess board
 to get from start to stop position, constrained by occupied positions.
 Currently only configured for knights.

 Note: solutions are not unique! Alternative minimal paths
 exist between any two given points.

Parameters:

  positions (str): start and stop position of chess board in chess board notation,
      separated by space. (e.g. 'A1 C5')

  occupied_spaces=['start', positions] (str): inaccessible positions on chess board.
      'start' indicates default starting positions for black side pieces.

  piece='knight' (str): piece being moved. Currently only configured for knight.
    
Output:

  (str) Moves traversed from start point to end without landing on occupied spaces,
            in chess board notation separated by space. (e.g. 'A1 B3 C5')

Author:
    Omar Ali (Omarh90@gmail.com)
    Written 7/2019
"""

def move(positions, occupied_spaces=None, piece='knight'):
    import pandas as pd
    import re
    
    class Graph:
    
        #TODO: No colors of pieces indicated. Add in new dimension
        def __init__(self, tup, occupied_t=set(), ht=0, parent=None):
            
            #Green: untraversed; Red: traversed
            # Not to be confused with black/white demarcation of opposing chess pieces
            self.color='green'
            Graph.occupied_nodes=occupied_t

            self.height=ht
            self.node=tup
            self.parent=parent

            # Define dataframe with chess move graph
            if not self.parent:
                Graph.flat_df=pd.DataFrame(columns=['position', 'move', 'color', 'parent'])
            t1_df=pd.DataFrame({'position':[self.node], 'move':[self.height], 'color':[self.color], 'parent':[self.parent]})
            Graph.flat_df = Graph.flat_df.append(t1_df, ignore_index=True)

    
        def set_target(self, target):
            # Set target position
            self.target=target

        
        def generate_children(self, index):
            # Generate possible moves
            
            # Designate position as traversed
            self.color='red' 
            Graph.flat_df.color[index]=self.color

            # Update constraints on possible moves    
            self.traversed_nodes=set(Graph.flat_df.position)
            self.forbidden_nodes=self.traversed_nodes.union(Graph.occupied_nodes)

            # All possible moves of a knight from a given position,
            #  including boundaries of chess board, and ignoring occupied positions and
            #  already traversed positions.
            self.children=generate_moves(self.node, self.forbidden_nodes, piece)
            # Initialize and grow list of graph nodes being generated
            if not self.parent:
                Graph.t0_ls=[]   
            for t in self.children:
                t0=Graph(t, Graph.occupied_nodes, self.height+1, self.node)
                Graph.t0_ls.append(t0)

        def generate_recur(self):
            # Generate graph recursively
            
            i=0
            while len(Graph.flat_df[Graph.flat_df.color=='green'])>0 and \
                  len(Graph.flat_df[Graph.flat_df.position==self.target])==0 and \
                  i <= len(Graph.t0_ls):
                # Recursively generate new moves for each member new node.
                #  Stop as at first appearance of target (e.g. shortest distance),
                #  or once every position is covered.

                try:
                    Graph.t0_ls[i].generate_children(i)
                except IndexError:
                    # Endpoint failure. Return critical error.
                    return error2
                except:
                    # Return general error.
                    return error0
                i=i+1
            return Graph.flat_df
        
        def traceback(self, Gr_df):
    
            # Once target is located, trace back steps to initial position.
            Graph.flat_df=Gr_df
            moves_ls=[self.target]
            try:
                # Find parent of position matching target
                x1=Graph.flat_df[Graph.flat_df['position']==self.target]['parent'].get_values()[0]
            except:
                # If target not found, return critical error.
                return error2
            x2=x1
            
            # Maximum number of moves made
            move0=Graph.flat_df['move'].max()
            
            while move0>1:
                # Cycle backwards from child to parent nodes until root is found.
                #  Record each node in list.
                move0=move0-1
                moves_ls.append(x2)
                x2=Graph.flat_df[(Graph.flat_df['position']==x1) & \
                                 (Graph.flat_df['move']==move0)]['parent'].get_values()[0]
                x1=x2
            moves_ls.reverse()
            return moves_ls
    
    
    def chess_to_tup(p, inverse=False):
        
        """
        Converts algebraic chess notation of position on chess board to x-y coordinate tuple
           or vis versa (for inverse=True).

        Input:
            p (tuple or string): chess board position, indicated by tuple or chess board notation (e.g. 'H2')
            
            inverse (bool): If false, converts position from chess board notation to tuple. If true, tuple to chess.

        Output: equivalent chess board position (tuple or string).
        """
    
        # x-position of chess board in algebraic notation.
        x={'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8}
        x_inv={1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H'}
    
        if not inverse:
        # Go from chess notation to tuple
            try:
                # Clean user input or raise error if invalid.
                p.upper().strip()
                p=re.sub('\s','',p)
    
                # Raise error if out of bounds
                if re.search('[A-H][1-8]',p):
                    t=(int(x[p[0]]),int(p[1]))
                    return t
    
                else:
                    # Out of bounds error
                    return 1
    
            except:
                # General error: Invalid input
                return None 
        else:
            # Go from tuple to chess notation
            p1= x_inv[p[0]]+str(p[1])
            return p1

    def generate_moves(p, forbidden, piece):
        """
        Defines every possible move for specified chess piece
         on chess board at position p, given constraints in forbidden positions.

        Input:
            p (tuple): knights starting position on chess board

            forbidden (set): positions that are either occupied by another piece or that have been previously traversed.

            piece (str): define which chess piece is being moved.
            
        Output:

            moves (list): tuples of all possible moves from current position
        """

        # TODO: Write rules for other chess pieces: queen, king, bishop, rook, pawn.
        #         Note: special moves not currently configured without additional parameters (e.g. en passant).

        x, y = p[0], p[1]

        if piece=='knight':

            moves=[(x+(2**k)*(-1)**i, y+(2**abs(k-1))*(-1)**j) for i in range(2) for j in range(2) for k in range(2) \
                    if x+(2**k)*(-1)**i > 0 and x+(2**k)*(-1)**i <= 8 and y+(2**abs(k-1))*(-1)**j <= 8 \
                    and y+(2**abs(k-1))*(-1)**j > 0 and (x+(2**k)*(-1)**i, y+(2**abs(k-1))*(-1)**j) not in forbidden]
             
            moves.sort()
            return moves
        
    error0=' Error: Invalid input! Please input start and stop points in chess notation, separated by space. (e.g.\'A1 B2\')'
    error1=' Error: Specified position(s) out of bounds!'
    error2=' Critical Error: End point not found!'

    # Initialize warning string    
    warning=""

    # If positions occupied due to other black pieces, work around those pieces   
    # TODO: Input black/white demarcation and rules
    occupied_spaces_t=set()
    if occupied_spaces:
        occupied_spaces_ls=occupied_spaces.upper().strip().split(' ')
        for p in occupied_spaces_ls:
            occupied_spaces_t=occupied_spaces_t.union([chess_to_tup(p)])

    # Starting position for black pieces.
    if occupied_spaces=='start':
        occupied_spaces_start={(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),\
                               (1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8)}
        occupied_spaces_t=occupied_spaces_start.copy()

    # Possible chess pieces.
    pieces = {'queen', 'king', 'bishop', 'knight', 'rook' 'pawn'}
   
    # Clean user input & raise error if invalid input.
    if type(piece)==str:
        piece=piece.lower().strip()
        if piece not in pieces \
           or piece != 'knight': # Currently only configured for knight
        # If piece entered not chess piece, return user input error.
            return error0
    else:
        return error0
    
    if type(positions)==str:    
        positions=positions.upper().strip()
    else:
        # If string not entered, return user input error.
        return error0

    # Clean chess notation input and convert into tuple.
    p = tuple(filter(None,re.split('\s|\W|_',positions)))
    if len(p)==2:
        p0, p1 = p
        t_i = chess_to_tup(p0)
        t_f = chess_to_tup(p1)
    else:
        # Raise user input error if ambiguous start and endpoint.
        return error0
        
    if t_i==0 or t_f==0:
        # Out of bounds error
        return error1

    elif type(t_i)!=tuple or type(t_f)!=tuple:
        # User input error
        return error0

    if t_i in occupied_spaces_t:
        # Remove current piece from occupied_spaces
        occupied_spaces_t = occupied_spaces_t - set([t_i])
    
    if t_f in occupied_spaces_t:
        # Raise warning if target location is occupied.
        #  Note: this assumes pieces are same color/side
    
        occupied_spaces_t = occupied_spaces_t - set([t_f])

        # Return warning
        warning=' Warning: End point occupied by other piece.'

    Grph=Graph(t_i,occupied_spaces_t)
    Grph.set_target(t_f)
    Grph.generate_children(0)
    Graph_df=Grph.generate_recur()
    mindist_t=Grph.traceback(Graph_df)
    
    mindist_p=[]



    for t in mindist_t:
        # Tuples to chess allocations
        if type(t)==tuple:
            mindist_p.append(chess_to_tup(t,inverse=True))
        else:
            # Formatting for error message
            mindist_p=[mindist_t]
    if warning:
        mindist_p.append(warning)
    return ' '.join(mindist_p)
