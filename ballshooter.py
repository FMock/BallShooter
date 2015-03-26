from tkinter import *
import random
import time

class Bullet:
	def __init__(self, canvas, paddle, color):
		self.canvas = canvas
		self.paddle = paddle
		paddle_pos = self.canvas.coords(self.paddle.id)
		self.id = 2 #the first bullet has an id of 2
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
		#print(self.yPosition)
		#print(self.canvas_height)
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
		starts = [-3, -2, -1, 1, 2, 3]
		random.shuffle(starts)
		self.x = starts[0]
		self.y = -3
		self.count = 0
		self.canvas_height = self.canvas.winfo_height()
		self.canvas_width = self.canvas.winfo_width()
		
	def newBall(self):
		self.canvas.move(self.id, random.randint(-200, 400), random.randint(-200, 400))
		self.increaseCount()
		
	def hit_paddle(self, pos):
		paddle_pos = self.canvas.coords(self.paddle.id)
		if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
			if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
				return True
		return False
		
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
				self.newBall()
		if pos[0] <= 0:
			self.x = 3
		if pos[2] >= self.canvas_width:
			self.x = -3
			
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
		

		
tk = Tk()
tk.title("Ball Shooter")
tk.resizable(0,0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

paddle = Paddle(canvas, 'blue')
bullet = Bullet(canvas, paddle, 'black')
ball = Ball(canvas, paddle, bullet, 'red')



while 1:
	ball.draw()
	paddle.draw()
	bullet.draw()
	tk.update_idletasks()
	tk.update()
	time.sleep(0.01)