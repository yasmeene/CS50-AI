import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # if cells are equal to the amount of mines (self.count) and there exist mines, then return self.count. else return an empty set.
        if len(self.cells) == self.count and self.count != None:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if the count of mines is 0, then the cells are safe since there are no mines. else return an empty set
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # runs through all cells, if the possible cell isnt in cell then it adds it to the updated set. else, it removes it from the count and changes cells, to update
        update = set()
        for pcell in self.cells:
            if pcell != cell:
                update.add(pcell)
            else:
                self.count -= 1
        self.cells = update

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # checks to see if possible cell is in self.cells, if it isnt it adds the cell to the update set.
        update = set()
        for pcell in self.cells:
            if pcell != cell:
                update.add(pcell)
        self.cells = update


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # adds cell to the moves made, and the marked safe
        # 1
        self.moves_made.add(cell)

        # 2
        self.mark_safe(cell)

        # loops over neighbouring cells, and checks if the cells are already marked safe
        # 3
        neighbours = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if (i, j) in self.safes:
                    continue
                if (i, j) in self.mines:
                    count -= 1
                    continue

                # checks the absolute value of the cells and rows subtract existing cells to see if they are neighbours 
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbours.add((i, j))
                else:
                    continue

        new_inference = Sentence(neighbours, count)
        self.knowledge.append(new_inference)

        # 4
        for sentence in self.knowledge:
            mines = sentence.known_mines()
            safes = sentence.known_safes()

            # if there are safes or mines in self.knowledge, then we add them using union to make sure duplicates are not included
            if safes:
                self.safes = self.safes.union(safes)
            if mines:
                self.mines = self.mines.union(mines)

        # 5
        for sentenceA in self.knowledge:
            for sentenceB in self.knowledge:

                # if the cells of sentence a exist in the cells of sentence b, remove them and the counts of mines
                if sentenceA.cells.issubset(sentenceB.cells):
                    new_cells = sentenceB.cells - sentenceA.cells
                    new_count = sentenceB.count - sentenceA.count
                    new_sentence = Sentence(new_cells, new_count)
            
                if new_sentence not in self.knowledge:
                    self.knowledge.append(new_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # makes list out of safes subtracting moves made
        safe_moves = self.safes - self.moves_made
        if len(safe_moves) != 0:
            # makes random choice out of given list
            return random.choice(list(safe_moves))

        # returns none if no moves can be made
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        free_spaces = []

        # iterates through i, j. if i, j is not a move that has already been made and also not a mine, then add that cell to free_spaces
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    free_spaces.append(cell)
        
        # if there are no free spaces, we return none
        if len(free_spaces) ==  0:
            return None
        # we randomize a cell in free_spaces to choose from
        i = random.randrange(len(free_spaces))
        return free_spaces[i]