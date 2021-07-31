import tkinter as tk
import math
from tkinter import messagebox
import threading
from tkinter.constants import W

canvas = None

SQUARE_LENGTH = 60
RADIUS = SQUARE_LENGTH / 2 - 5
POSITION = {"x": 8, "y": 8}
BORDER_WIDTH = 3
NUMBER = 8
LENGTH = SQUARE_LENGTH * NUMBER + BORDER_WIDTH * NUMBER
cells = []
BLACK = 1
WHITE = 2
turn = 1

def set_field():
  global cells
  canvas.create_rectangle(POSITION["x"], POSITION["y"], LENGTH + POSITION["x"], LENGTH + POSITION["y"], fill='darkgreen', width=BORDER_WIDTH)

  for i in range(NUMBER - 1):
    x = POSITION["x"] + SQUARE_LENGTH * (i + 1) + BORDER_WIDTH * i + BORDER_WIDTH
    y = POSITION["y"] + SQUARE_LENGTH * (i + 1) + BORDER_WIDTH * i + BORDER_WIDTH
    canvas.create_line(x, POSITION["y"], x, LENGTH + POSITION["y"], width=BORDER_WIDTH)
    canvas.create_line(POSITION["x"], y, LENGTH + POSITION["x"], y, width=BORDER_WIDTH)
  cells = [[0]* NUMBER for i in range(NUMBER)]

def set_item(kind, x, y):
  center_x = POSITION["x"] + BORDER_WIDTH * x + BORDER_WIDTH / 2 + SQUARE_LENGTH * x + SQUARE_LENGTH / 2
  center_y = POSITION["y"] + BORDER_WIDTH * y + BORDER_WIDTH / 2 + SQUARE_LENGTH * y + SQUARE_LENGTH / 2

  canvas.create_rectangle(center_x - SQUARE_LENGTH / 2, center_y - SQUARE_LENGTH / 2, center_x + SQUARE_LENGTH / 2, center_y + SQUARE_LENGTH / 2, fill="darkgreen", width=0)

  if kind != None:

    if kind == BLACK:
      canvas.create_oval(center_x - RADIUS, center_y - RADIUS, center_x + RADIUS, center_y + RADIUS, fill="black", width=0)
      cells[x][y] = BLACK
    elif kind == WHITE:
      canvas.create_oval(center_x - RADIUS, center_y - RADIUS, center_x + RADIUS, center_y + RADIUS, fill="white", width=0)
      cells[x][y] = WHITE

def point_to_numbers(event_x, event_y):
    x = math.floor((event_x - POSITION["x"]) / (SQUARE_LENGTH + BORDER_WIDTH))
    y = math.floor((event_y - POSITION["y"]) / (SQUARE_LENGTH + BORDER_WIDTH))
    return x, y

def create_canvas():
  root = tk.Tk()
  root.geometry(f"""{LENGTH + POSITION["x"] * 2}x{LENGTH + POSITION["y"] * 2}""")
  root.title("オセロ")
  canvas = tk.Canvas(root, width=(LENGTH + POSITION["x"]), height=(LENGTH + POSITION["y"]))
  canvas.place(x=0, y=0)

  return root, canvas

def click(event):
  global turn
  x, y = point_to_numbers(event.x, event.y)
  my_turn = 2 if turn % 2 == 0 else 1
  if check_adjacent(x, y, my_turn) == False:
    return
  set_item(my_turn, x, y)
  next_turn = 3 - my_turn# 次は白
  check_adjacent(x, y, 3 - next_turn, True)
  black_count, white_count = count_stones() # (b, w)
  if black_count + white_count == 64:
    show_result(black_count, white_count)
  turn += 1
  if should_pass(next_turn):
    pass_message()
    turn += 1
  """""
  #パスが必要かどうか　　　一方向でも置けるところがあれば要らない
  should_pass = True
  stone_count = 0
  for i in range(NUMBER):
    for j in range(NUMBER):
      if cells[i][j] == 1 or cells[i][j] == 2:
        stone_count += 1
        if stone_count == 64:
          should_pass = False
      if check_adjacent(i, j, next_turn) == True: # 次の色が置ける条件の時
      # if is_set_stones(i, j, next_turn) == True: # 次の色が置ける条件の時
        should_pass = False
  if should_pass == True:
    pass_message()
    turn += 1
  """""

def should_pass(next_turn):
  stone_count = 0
  for i in range(NUMBER):
    for j in range(NUMBER):
      if cells[i][j] == 1 or cells[i][j] == 2:
        stone_count += 1
        if stone_count == 64:
          return False
      elif check_adjacent(i, j, next_turn) == True: # 次の色が置ける条件の時
        return False
  return True
      
      



def pass_message():
  messagebox.showinfo('Title','パス')

# check_adjacent(a, b) -> my_turn = None
# check_adjacent(a, b, 1) -> my_turn = 1

def check_adjacent(x, y, my_turn, flip=False):
  if not flip and (cells[x][y] == 1 or cells[x][y] == 2):#すでに置いてある所に置けないようにする
    return False
  ways = [(1, -1), (1, 1), (-1, -1), (-1, 1), (0, -1), (0, 1), (1, 0), (-1, 0)] #８方向分
  for way_x, way_y in ways:
    col = x + way_x
    row = y + way_y
    can_flip = False
    while 0 <= col <= 7 and 0 <= row <= 7:
      if cells[col][row] == 0:#空
        break
      if not flip and col == x + way_x and row == y + way_y and cells[col][row] == my_turn:
        break
      if cells[col][row] == my_turn:
        can_flip = True
        break
      col += way_x
      row += way_y
    # print(can_flip)
    if can_flip == True:
      if not flip:
        return True
      else:
        while col != x or row != y:
          if my_turn == WHITE:
              set_item(WHITE, col, row)
          elif my_turn == BLACK:
              set_item(BLACK, col, row)
          col -= way_x
          row -= way_y
  return False

"""""
def flip(x, y, my_turn):
  ways = [(1, -1), (1, 1), (-1, -1), (-1, 1), (0, -1), (0, 1), (1, 0), (-1, 0)] #８方向分
  for way_x, way_y in ways:
    col = x + way_x
    row = y + way_y
    can_flip = False
    while 0 <= col <= 7 and 0 <= row <= 7:
      if cells[col][row] == 0:#空
        break
      if cells[col][row] == my_turn:
        can_flip = True
        break
      col += way_x
      row += way_y
    if can_flip == True:
      while col != x or row != y:
        if my_turn == WHITE:
            set_item("white", col, row)
        elif my_turn == BLACK:
            set_item("black", col, row)
        col -= way_x
        row -= way_y

#8方位のうちでどこか一つでもおければ良い
#my_turn 黒か白の石のどちか       
def is_set_stones(x, y, my_turn):
  if cells[x][y] == 1 or cells[x][y] == 2:#すでに置いてある所に置けないようにする
    return False
  ways = [(1, -1), (1, 1), (-1, -1), (-1, 1), (0, -1), (0, 1), (1, 0), (-1, 0)]
  for way_x, way_y in ways:
    col = x + way_x
    row = y + way_y
    while 0 <= col <= 7 and 0 <= row <= 7:
      if cells[col][row] == 0:#空白x
        break
      #一つズレた８方向が同じ色x
      if col == x + way_x and row == y + way_y and cells[col][row] == my_turn:
        break
      if cells[col][row] == my_turn:#基準の色とcol,rowの色が同じ時flip
        return True
      col += way_x
      row += way_y
  return False
"""

# セルが全て埋まった時のみカウントして結果を出す埋まっていない場合はカウントすらしなくていい

# 黒と白の石をそれぞれカウントする         
def count_stones():
  black_count = 0
  white_count = 0
  for j in range(NUMBER):
    for i in range(NUMBER):  
        if cells[j][i] == BLACK:
          black_count += 1
        elif cells[j][i] == WHITE:
          white_count += 1 
        # print(black_count + white_count)
  return black_count, white_count

# 数を比較する
def show_result(black_count, white_count):
  if black_count > white_count:
        common_message('黒の勝ち白の負け')
  elif black_count < white_count:
        common_message('白の勝ち黒の負け')
  else:
        common_message('ドロー') # black_count == white_count:の時

          


""""

def result():
  black_count = 0
  white_count = 0
  for x in range(NUMBER):
    for y in range(NUMBER):  
        if cells[x][y] == BLACK:
          black_count += 1
        elif cells[x][y] == WHITE:
          white_count += 1

  if black_count + white_count != 64:
      return
  if black_count > white_count:
      black_win_message()
  elif black_count < white_count:
      black_lose_message()
  elif black_count == white_count:
    draw_message()

"""



def common_message(text):
  messagebox.showinfo('Title', text)

""""
def black_win_message():
  messagebox.showinfo('Title','黒の勝ち白の負け')

def black_lose_message():
  messagebox.showinfo('Title','白の勝ち黒の負け')

def draw_message():
  messagebox.showinfo('Title','ドロー')
"""

def set_first_field():
    set_item(BLACK,3,4)
    set_item(BLACK,4,3)
    set_item(WHITE,3,3)
    set_item(WHITE,4,4)

def callback(evt):
  th = threading.Thread(target=click, args=(evt,))
  th.start()


def play():
  global canvas
  root, canvas = create_canvas()
  set_field()
  set_first_field()
  canvas.bind("<Button-1>", lambda event: callback(event))
  root.mainloop()

play()
