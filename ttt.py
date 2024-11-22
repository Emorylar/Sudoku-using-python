import pygame
pygame.font.init()

def main():
    win=pygame.display.set_mode((350,400))
    pygame.display.set_caption("Tic Tac Toe")
    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT():
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
    win.fill(255,255,255)      
          