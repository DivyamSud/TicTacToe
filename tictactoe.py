import pygame 
import itertools

fps = 60
width, height = 600, 600
rows, cols = 3, 3
square_size = width//cols
red = (255,0,0)
blue = (0,0,255)
gray = (60,60,60)
white = (211,211,211)
dark_gray = (30,30,30)
black = (0,0,0)
yellow = (255,255,0)
x = "x"
o = "o"
color = "color"
 
Window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe")

class Board:
	def __init__(self):
		self.board = []
		self.no_of_x = self.no_of_o = 0
		self.create_board()

	def draw_board_squares(self, win):
		width = 10
		win.fill(dark_gray)
		pygame.draw.line(win, white, (200, 0), (200, 600), width)
		pygame.draw.line(win, white, (400, 0), (400, 600), width)
		pygame.draw.line(win, white, (0, 200), (600, 200), width)
		pygame.draw.line(win, white, (0, 400), (600, 400), width)

	def create_board(self):
		for row in range(rows):
			self.board.append([])
			for col in range(cols):
				self.board[row].append(0) 

	def draw(self, win):
		self.draw_board_squares(win)
		for row in range(rows):
			for col in range(cols):
				piece = self.board[row][col]
				if piece != 0:
					shape = piece.__repr__()
					if shape == x:
						piece.draw_x(win)
					else:
						piece.draw_o(win)

	def move(self, row, col, shape):
		if shape == x:
			self.board[row][col] = Piece(row, col, yellow, x)
		else:
			self.board[row][col] = Piece(row, col, red, o)

	def get_slot(self, row, col):
		return self.board[row][col]

	def get_valid_moves(self):
		valid_moves = []
		for row in range(rows):
			for col in range(cols):
				if self.board[row][col] == 0:
					valid_moves.append((row, col))
		return valid_moves

	def count(self, shape):
		self.no_of_o = self.no_of_x = 0
		for row in self.board:
			for piece in row:
				if piece != 0 and piece.__repr__() == shape:
					if shape == x:
						self.no_of_x += 1
					else:
						self.no_of_o += 1
		if shape == x:
			return self.no_of_x
		else:
			return self.no_of_o

	def evaluate(self):
		no_x = self.count(x)
		no_o = self.count(o)
		return no_o - no_x

class Piece:
	padding = 50
	width = 20
	outline = 15

	def __init__(self, row, col, color, shape):
		self.color = color
		self.shape = shape
		self.col = col
		self.row = row
		self.x = 0
		self.y = 0
		self.calc_pos()

	def calc_pos(self):
		self.x = square_size*self.col + square_size//2
		self.y = square_size*self.row + square_size//2

	def draw_o(self, win):
		radius = square_size//2 - self.padding
		pygame.draw.circle(win, self.color, (self.x, self.y), radius + self.outline)
		pygame.draw.circle(win, dark_gray, (self.x, self.y), radius)

	def draw_x(self, win):
		base = height = (square_size//2 - self.padding)*2
		pygame.draw.line(win, self.color, (self.x-base//2, self.y-height//2),(self.x+base//2, self.y+height//2), self.width) 
		pygame.draw.line(win, self.color, (self.x+base//2, self.y-height//2),(self.x-base//2, self.y+height//2), self.width)

	def move(self, row, col):
		self.row = row
		self.col = col
		self.calc_pos()

	def __repr__(self):
		return str(self.shape)

class Game:
	def __init__(self, win):
		self._init()
		self.win = win

	def _init(self):
		self.valid_selection = False
		self.turn = x
		self.board = Board()
		self.valid_moves = []

	def reset(self):
		self._init()

	def update(self):
		self.board.draw(self.win)
		pygame.display.update()

	def _check(self, row, col):
		slot = self.board.get_slot(row, col)
		if slot == 0:
			self.valid_selection = True
		else:
			self.valid_selection = False

	def move(self, row, col, run=True):
		slot = self.board.get_slot(row, col)
		self._check(row, col)
		if self.valid_selection:
			self.valid_moves = self.board.get_valid_moves()
			moved = False
			while not moved:
				if slot == 0 and (row, col) in self.valid_moves:
					self.board.move(row, col, self.turn)
					self.valid_moves = self.board.get_valid_moves()
					if self.valid_moves == []:
						print("Tie!!")
						run = False
					moved = True
		
			self.change_turn()
		else:
			moved = False
		return run

	def change_turn(self):
		if self.turn == x:
			self.turn = o
		else:
			self.turn = x

	def check_win(self):

		curr_game = self.__repr__()

		def all_same(original_list_name):
			list_name = []
			for element in original_list_name:
				new_element = str(element)
				list_name.append(new_element)
			if list_name.count(list_name[0]) == len(list_name) and list_name[0] != "0":
				return True
			else:
				return False

		for row in curr_game:
			if all_same(row):
				return True

		for col in range(len(curr_game)):
			check = []
			for row in curr_game:
				check.append(row[col])
			if all_same(check):
				return True
		
		diags = []
		for ind in range(len(curr_game)):
			diags.append(curr_game[ind][ind])
		if all_same(diags):
			return True

		diags = []
		for col, row in enumerate(reversed(range(len(curr_game)))):
			diags.append(curr_game[row][col])
		if all_same(diags):
			return True
		return False

	def __repr__(self):
		return list(self.board.board)


def get_pos_from_mouse(pos):
	x, y = pos
	row = y // square_size
	col = x // square_size
	return row, col

def main():
	run = True
	clock = pygame.time.Clock()
	game = Game(Window)

	while run:
		clock.tick(fps)

		if game.check_win():
			game.change_turn()
			print(f"{game.turn} is the winner!")
			run = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				row, col = get_pos_from_mouse(pos)
				run = game.move(row, col, run)

		game.update()

	pygame.time.wait(800)		
	pygame.quit()

main()		