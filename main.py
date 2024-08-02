import pygame, sys
from pygame.locals import QUIT
import os
import math
from english_words import get_english_words_set
import secrets

list_words = list(get_english_words_set(["web2"], False, True))

#Set up display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hangman Game')

#fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

#Load images
images = []
for i in range(7):
  image = pygame.image.load("hangman"+str(i) + ".png")
  images.append(image)
  #pixels called surface

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)



#button vaiables
RADIUS = 20
GAP = 15
letters = []
starx = round((WIDTH - (RADIUS * 2 + GAP) * 13)/2)
starty = 400
A = 65
for i in range(26):
  x = starx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
  y = starty + ((i // 13) * (GAP + RADIUS * 2))
  letters.append([x,y,chr(A+i), True])



#game variables
hangman_status = 0
word = secrets.choice(list_words)
word = word.upper()
guessed = []
run = True




def display_message(message):
  win.fill(WHITE)
  text = WORD_FONT.render(message, 1, BLACK)
  win.blit(text,(WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
  pygame.display.update()
  

def final_draw():
  #Text
  message = "Would you like to play again?"
  win.fill(WHITE)
  text = WORD_FONT.render(message, 1, BLACK)
  win.blit(text,(WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
  
  #YES
  pygame.draw.circle(win, BLACK, (WIDTH//2 - 35 - 100, HEIGHT//2 + 100), 35, 3)
  text = LETTER_FONT.render("YES", 1, BLACK)
  win.blit(text, (WIDTH//2 - 35 - 100 - text.get_width()/2, HEIGHT//2 + 100 - text.get_height()/2))
  #NO
  pygame.draw.circle(win, BLACK, ( WIDTH//2 + 35 + 100, HEIGHT//2 + 100), 35, 3)
  text = LETTER_FONT.render("NO", 1, BLACK)
  win.blit(text, (WIDTH//2 + 35 + 100 - text.get_width()/2, HEIGHT//2 + 100 - text.get_height()/2))
  pygame.display.update()
  

def draw():
  global display_word
  win.fill(WHITE)
  text = TITLE_FONT.render("HANGMAN", 1, BLACK)
  win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

  #draw word
  display_word = ""
  for letter in word:
    if letter in guessed:
      display_word += letter + " "
    else:
      display_word += "_ "
  text = WORD_FONT.render(display_word, 1, BLACK)
  win.blit(text, (500-text.get_width()/2,200))
  

  for letter in letters:
    x,y, ltr, vis = letter
    if vis:
      pygame.draw.circle(win, BLACK, (x,y), RADIUS, 3)
      text = LETTER_FONT.render(ltr, 1, BLACK)
      win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
      
  #blit to load surfaces (image)
  win.blit(images[hangman_status], (50,100))
  pygame.display.update()

def main():
  
  global run
  global hangman_status
  #Setup game loop
  FPS = 60
  clock = pygame.time.Clock()

  while run:
    clock.tick(FPS)
  
    draw()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        m_x,m_y = pygame.mouse.get_pos()
        for letter in letters:
          x,y,ltr, vis = letter
          if vis:
            dis = math.sqrt((x-m_x)**2 + (y-m_y)**2)
            if dis < RADIUS:
              letter[3] = False
              guessed.append(ltr)
              if ltr not in word:
                hangman_status += 1
                
    won = True
    for letter in word:
      if letter not in guessed:
        won = False
        break
    if won:
      draw()
      pygame.time.delay(2000)
      display_message("You Won!")
      pygame.time.delay(3000)
      run = False
      break
  
    if hangman_status == 6:
      win.blit(images[hangman_status], (50,100))
      text = WORD_FONT.render(word, 1, BLACK)
      win.blit(text,(500-text.get_width()/2,300))
      pygame.display.update()
      pygame.time.delay(2000)
      display_message("You Lost!")
      pygame.time.delay(3000)
      run = False
      break

      
main()

while run == False:

  final_draw()

  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      m_x, m_y = pygame.mouse.get_pos()
      print(m_x, m_y)
      dis_yes = math.sqrt(((WIDTH//2 - 35 - 100)-m_x)**2 + ((HEIGHT//2 + 100)-m_y)**2)
      dis_no = math.sqrt(((WIDTH//2 + 35 + 100)-m_x)**2 + ((HEIGHT//2 + 100)-m_y)**2)
      if dis_yes < 35:
        print("Yes")
        #reset variables
        hangman_status = 0
        word = secrets.choice(list_words)
        word = word.upper()
        guessed = []
        run = True

        #reset the letters : 
        letters = []
        starx = round((WIDTH - (RADIUS * 2 + GAP) * 13)/2)
        starty = 400
        A = 65
        for i in range(26):
          x = starx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
          y = starty + ((i // 13) * (GAP + RADIUS * 2))
          letters.append([x,y,chr(A+i), True])
          
        main()
      if dis_no < 35:
        print("No")
        pygame.quit()
  
  
 



