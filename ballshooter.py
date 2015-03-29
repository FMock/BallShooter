from tkinter import *
import random
import time

# Object of game: Score points by shooting the red ball.
# Shoot any other shape and the game ends
# Up-Arrow shoots bullets
# Left-Arrow - move shooter left
# Right-Arrow - move shooter right
# Down-Arrow - stop shooter from moving
# Any-Key - start game over


#The first bullet object must have the highest id so that the id of other
#objects does not conflict with the collision detection of any bullet.
#Each time a bullet is fired its id increases by one
class Bullet:
	def __init__(self, canvas, paddle, color):
		self.canvas = canvas
		self.paddle = paddle
		paddle_pos = self.canvas.coords(self.paddle.id)
		self.id = 5 #the first bullet has an id of 5
		self.canvas.bind_all('<KeyPress-Up>', self.shoot)
		self.pos = self.canvas.coords(self.id)
		self.y = 0
		self.yPosition = 0
		self.shot = False
		self.color = color
		self.canvas_height = self.canvas.winfo_height()
	
	def draw(self):
		self.canvas.move(self.id, 0, self.y)
		pos = self.canvas.coords(self.id)
		self.yPosition = pos[1]
		if pos[1] <= 0: #if the bullet lower than the top of window
			self.shot = False
				
	def shoot(self, evt):
		self.shot = True
		self.canvas = canvas
		self.paddle = paddle
		paddle_pos = self.canvas.coords(self.paddle.id)
		canvas.create_oval(paddle_pos[0] + 20, paddle_pos[1], paddle_pos[0] + 30, paddle_pos[1] + 10, fill=self.color)
		self.y = -5
		self.id += 1
		self.pos = self.canvas.coords(self.id)

class Ball:
	def __init__(self, canvas, paddle, bullet, color):
		self.canvas = canvas
		self.paddle = paddle
		self.bullet = bullet
		self.id = canvas.create_oval(10, 10, 40, 40, fill=color)
		self.canvas.move(self.id, 245, 100)
		starts = [-4, -3, -2, -1, 1, 2, 3, 4]
		random.shuffle(starts)
		self.x = starts[0]
		self.y = -3
		self.count = 0
		self.canvas_height = self.canvas.winfo_height()
		self.canvas_width = self.canvas.winfo_width()
		
	def newBall(self):
		#make the ball re-appear at a random location in the game window
		self.canvas.move(self.id, random.randint(-200, 400), random.randint(-200, 400))
		self.increaseCount()
		
	#Checks if the ball has hit the paddle shooter
	def hit_paddle(self, pos):
		paddle_pos = self.canvas.coords(self.paddle.id)
		if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
			if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
				return True
		return False
		
	#Checks if the ball has hit the bullet
	def hit_bullet(self, pos):
		bullet_pos = self.canvas.coords(self.bullet.id)
		if pos[2] >= bullet_pos[0] and pos[0] <= bullet_pos[2]:
			if pos[3] >= bullet_pos[1] and pos[3] <= bullet_pos[3]:
				return True
		return False

	def increaseCount(self):
		self.count += 1
		print(self.count)
		
	def draw(self):
		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		if pos[1] <= 0:
			self.y = 3
		if pos[3] >= self.canvas_height:
			self.y = -3
		if self.hit_paddle(pos) == True:
			self.y = -3
		if self.bullet.shot == True:
			if self.hit_bullet(pos) == True:
				self.canvas.move(self.bullet.id, 0, -400)#make bullet disappear from game window
				self.newBall()
		if pos[0] <= 0:
			self.x = 3
		if pos[2] >= self.canvas_width:
			self.x = -3

#The paddle can move left or right.			
class Paddle:
	def __init__(self, canvas, color):
		self.canvas = canvas
		self.id = canvas.create_rectangle(0, 0, 50, 10, fill=color)
		self.canvas.move(self.id, 200, 300)
		self.x = 0
		self.canvas_width = self.canvas.winfo_width()
		self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
		self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
		self.canvas.bind_all('<KeyPress-Down>', self.stop)
		
	def draw(self):
		self.canvas.move(self.id, self.x, 0)
		pos = self.canvas.coords(self.id)
		if pos[0] <= 0:
			self.x = 0
		elif pos[2] >= self.canvas_width:
			self.x = 0
			
	def stop(self, evt):
		self.x = 0
	
	def turn_left(self, evt):
		self.x = -3
		
	def turn_right(self, evt):
		self.x = 3

#A square obstacle that continually moves left and right. If a bullet hits
#the square obstacle the game is over		
class SquareObstacle:
	def __init__(self, canvas, ball, bullet, color):
		self.ball = ball
		self.bullet = bullet
		self.canvas = canvas
		self.canvas_width = self.canvas.winfo_width()
		self.id = canvas.create_rectangle(0, 0, 40, 40, fill=color)
		self.canvas.move(self.id, -40, 0)
		self.x = 2
		self.gameOver = False
	
	#Checks if the square obstacle was hit by a bullet
	def obstacle_hit(self, pos):
		bullet_pos = self.canvas.coords(self.bullet.id)
		if pos[2] >= bullet_pos[0] and pos[0] <= bullet_pos[2]:
			if pos[3] >= bullet_pos[1] and pos[3] <= bullet_pos[3]:
				return True
		return False
		
	def draw(self):
		pos = self.canvas.coords(self.id)
		self.canvas.move(self.id, self.x, 0)
		if self.bullet.shot == True:
			if self.obstacle_hit(pos) == True:
				self.x = 0
				ball.x = 0
				ball.y = 0
				self.gameOver = True
		if pos[0] > self.canvas_width:
			self.x = -2
		if pos[2] == 0:
			self.x = 2
			
class TriangleObstacle:
	def __init__(self, canvas, ball, bullet, square_obstacle, color):
		self.ball = ball
		self.bullet = bullet
		self.canvas = canvas
		self.square_obstacle = square_obstacle
		self.canvas_width = self.canvas.winfo_width()
		self.id = canvas.create_polygon(300, 100, 350, 100, 350, 160, fill=color)
		self.canvas.move(self.id, -40, 0)
		self.x = -2
		self.gameOver = False
	
	#Checks if the triangle obstacle was hit by a bullet
	def obstacle_hit(self, pos):
		bullet_pos = self.canvas.coords(self.bullet.id)
		if pos[2] >= bullet_pos[0] and pos[0] <= bullet_pos[2]:
			if pos[3] >= bullet_pos[1] and pos[3] <= bullet_pos[3]:
				return True
		return False
		
	def draw(self):
		pos = self.canvas.coords(self.id)
		self.canvas.move(self.id, self.x, 0)
		if self.bullet.shot == True:
			if self.obstacle_hit(pos) == True:
				ball.x = 0
				ball.y = 0
				self.square_obstacle.x = 0
				self.gameOver = True
		if pos[0] > self.canvas_width:
			self.x = -2
		if pos[2] == 0:
			self.x = 2

#Displays the score, displays game over message and prompts the user to play again			
class Game_Info:
	def __init__(self, canvas, ball, square_obstacle, triangle_obstacle, color):
		self.canvas = canvas
		self.width = self.canvas.winfo_width()
		self.height = self.canvas.winfo_height()
		self.color = color
		self.ball = ball
		self.obstacle = square_obstacle
		self.triangle_obstacle = triangle_obstacle
		self.id = canvas.create_text(self.width/6, self.height/10, text = 'SCORE %d' % self.ball.count, font=('Courier', 12))
		self.canvas.bind_all('<Any-KeyPress>', self.replay)
	
	def draw(self):
		self.canvas.move(self.id, 0, 0)
		if self.obstacle.gameOver == False and self.triangle_obstacle.gameOver == False:
			canvas.itemconfig(self.id, text='SCORE %d' % self.ball.count, font=('Courier', 12))
		else:
			canvas.itemconfig(self.id, text='\nSCORE %d\nGAME OVER\nPLAY AGAIN?\n(press any key)' % self.ball.count, font=('Courier',12))
			self.triangle_obstacle.x = 0
	
	def replay(self, evt):
		self.ball.count = 0
		self.triangle_obstacle.gameOver = False
		self.triangle_obstacle.x = -2
		self.obstacle.gameOver = False
		self.obstacle.x = 2
		self.ball.x = 2
		self.ball.y = -3
	
tk = Tk()
tk.title("Ball Shooter")
endGame = False
tk.resizable(0,0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0, bg='#CBF7EB')
canvas.pack()
tk.update()

paddle = Paddle(canvas, 'blue')
bullet = Bullet(canvas, paddle, 'black')
ball = Ball(canvas, paddle, bullet, 'red')
square_obstacle = SquareObstacle(canvas, ball, bullet,'blue')
triangle_obstacle = TriangleObstacle(canvas, ball, bullet, square_obstacle, 'yellow')
game_info = Game_Info(canvas, ball, square_obstacle, triangle_obstacle, 'green')

#infinite game loop
while 1:
	game_info.draw() #id = 0
	square_obstacle.draw() #id = 1
	triangle_obstacle.draw() #id = 2
	ball.draw() #id = 3
	paddle.draw() #id = 4
	bullet.draw() #id = 5 The bullet must have the highest id
	tk.update_idletasks()
	tk.update()
	time.sleep(0.01)