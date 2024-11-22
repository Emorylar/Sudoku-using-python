#GUI.py
import pygame
import time
pygame.font.init()
class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self,rows,cols,width,height,win):
        self.rows=rows
        self.cols=cols
        self.cubes=[[Cube(self.board[i][j] , i , j , width , height) for j in range(cols)]for i in range(rows)]  #list of list
        self.height=height
        self.width=width
        self.win=win
        self.model=None
        self.update_model()
        self.selected=None

    def update_model(self):    #Updates the list of elements
        self.model=[[self.cubes[i][j].value for j in range(self.cols)]for i in range(self.rows)]   #List of elements

    def place(self, val):
        row,col=self.selected
        if self.cubes[row][col] == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False
    
    def sketch(self,val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)    #temp value is set

    def draw(self):
        #Draw Grid lines:
        gap=self.width / 9
        for i in range (self.rows+1):   #0 to 10
            if i%3==0 and i!=0:
                thick=4
            else:
                thick=1
            
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)  #black horizontal lines
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)  #black vertical lines

            # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self,row,col):
        #Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected=False

        self.cubes[i][j].selected=True
        self.selected=(row,col)

    def clear(self):     #To clear the temporary value when DELETE is entered
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)
            
    def click(self,pos):
        if pos[0]<self.width and pos[1]<self.height:  #If mouse is clicked inside the displayed window then the position is returned
            gap=self.width/9
            x=pos[0]//gap
            y=pos[1]//gap
            return (int(y),int(x))
        else :
            return None
        
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True
    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False

class Cube:
    rows=9
    cols=9

    def __init__(self, value,row,col,width,height):
        self.value=value
        self.temp=0
        self.row=row
        self.col=col
        self.width=width
        self.height=height
        self.selected=False

    def draw(self,win):
        fnt = pygame.font.SysFont("comicsans",40) #comicsans is a font style and 40 is the font size
        gap = self.width / 9    # size of each cell in the grid
        x = self.col * gap
        y = self.row *gap

        if self.temp!=0 and self.value == 0:
            text=fnt.render(str(self.temp),1,(128,128,128))  #(128,128,128) is the (R,G,B) value of gray color. 1 means "True" to anti-aliasing i.e. smoothing edges using intermediate colors and temporary value is rendered into an image
            win.blit(text, (x+5,y+5))  #'blit' method is used to draw one surface on to another. We wrote +5 to differentiate actual value to temporary value by offsetting its visible position by 5 pixels
        
        elif not(self.value == 0):
            text=fnt.render(str(self.value),1,(0,0,0))  #render actual value in black
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))  # Center the value
        if self.selected:
            pygame.draw.rect(win,(255,0,0),(x,y,gap,gap),3)  #draws a red border . (surface,color,rect(x,y,width,height),width). Here x,y is the top left corner

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)  # Font for rendering text
        gap = self.width / 9  # Size of each cube
        x = self.col * gap  # X position of the cube
        y = self.row * gap  # Y position of the cube

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)  # Clear the previous value

        text = fnt.render(str(self.value), 1, (0, 0, 0))  # Render the current value in black
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))  # Center the value
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)  # Draw a green border for correct placement. 3 is the width of border
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)  # Draw a red border for incorrect placement 3 is the width of border
    def set(self, val):
        self.value = val  # Set the cube's value

    def set_temp(self, val):
        self.temp = val  # Set the cube's temporary value
    
def find_empty(bo):
        for i in range(len(bo)):   #len(bo)=no. of rows
            for j in range(len(bo[0])):  #len(bo[0])=no of columns in first row
                if bo[i][j]==0:
                    return (i,j)   #returns row and column
        return None
    
def valid(bo,num,pos):
        #Check row
        for i in range(len(bo[0])):
            if bo[pos[0]][i]==num and pos[1]!=i:
                return False
        #Check column
        for i in range(len(bo)):
            if bo[i][pos[1]]==num and pos[0]!=i:
                return False
        #Check box
        box_x=pos[1] //3
        box_y=pos[0] //3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if bo[i][j] == num and (i,j) != pos:
                    return False

        return True
    
def redraw_window(win,board,time,strikes):
        win.fill((255,255,255))                     #fills the entire display window blank
        #To draw time
        fnt=pygame.font.SysFont("comicsans",40)
        text=fnt.render("Time: " +format_time(time),1,(0,0,0))
        win.blit(text,(540-245,600-60))
        #To draw strikes
        text=fnt.render("X" *strikes, 1, (255,0,0))
        win.blit(text,(20,600-60))
        #To draw grid an board
        board.draw()

def format_time(secs):
        sec=secs % 60
        minute=secs // 60
        hour=minute // 60

        mat=" "+str(hour)+":"+str(minute)+":"+str(sec)
        return mat

      
def main():
    win=pygame.display.set_mode((540,600))  #Sets the dimension of display grid (540 wd,600 ht)
    pygame.display.set_caption("Sudoku")  #Sets the title of the display window
    board=Grid(9,9,540,540,win)          #creating an obj called board
    key=None
    run=True
    start=time.time()  #Retrieves current time in seconds
    strikes = 0
    while run:
        play_time=round(time.time()-start)  #Rounds the floating number to show in seconds

        for event in pygame.event.get(): #responds to user inputs(key presses, mouse movements, and window events) ensuring your game or application remains interactive and responsive.
            if event.type == pygame.QUIT:
                run=False              #The user clicked windows close button
            if event.type == pygame.KEYDOWN:  #checks if user prssed a key
                if event.key == pygame.K_1:   #To check for keys pressed for (1-9)
                    key=1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:  #checks for constant numeric keys
                    key = 9
                if event.key == pygame.K_KP1: #checks for numeric keys from keypad
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:  #Delete key
                    board.clear()                 #removes all elements from a list
                    key=None
                if event.key == pygame.K_SPACE:   #Space key
                    board.solve_gui()
                if event.key == pygame.K_RETURN:  #Enter key
                    i,j=board.selected            #i and j of selected cell gets noted
                    if board.cubes[i][j].temp!=0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")    #Console print
                        else:
                            print("Wrong")      #Console print
                            strikes+=1
                        key=None

                        if board.is_finished():
                            print("Game over")
            
            if event.type == pygame.MOUSEBUTTONDOWN: #detecting mouse clicks
                pos=pygame.mouse.get_pos()  #returns current position of mouse in the form (x,y)
                clicked=board.click(pos)    #Calls a method named click and passes pos as parameter. Boolean value is returned
                
                if clicked:
                    board.select(clicked[0],clicked[1])
                    key=None

        if board.selected and key !=None:
            board.sketch(key)

        redraw_window(win , board , play_time, strikes)  #redraws window
        pygame.display.update()                          #updates display
main()
pygame.quit()








    
