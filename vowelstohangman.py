#dependencies
import pygame as P # accesses pygame files
import sys  # to communicate with windows


# pygame setup - only runs once
P.init()  # starts the game engine
clock = P.time.Clock()  # creates clock to limit frames per second
loopRate = 60  # sets max speed of main loop

SCREENSIZE = SCREENWIDTH, SCREENHEIGHT = 1024, 768  # sets size of screen/window
screen = P.display.set_mode(SCREENSIZE)  # creates window and game screen

DEFAULT_TEXT_SIZE = 48 #a default for any rendered text
P.display.set_caption('Hangman!')
#defaultFont = P.font.Font(None,80) #create a font for the letters, default font
#selectedFont = P.font.Font(None,40) #a smaller font for after the letters have been selected

# set variables for some colours RGB (0-255)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (200, 0, 235) #(128, 0, 128)
lightBlue = (185, 125, 255)#(125, 125, 255)

#clear and fill the screen
screen.fill(purple)

#define necessary classes
class renderedLetter(object):
    """letters rendered for display on screen
    
    to be displayer in pygame text has to be 'rendered'
    to be selectable with a mouse also need to define a rectangle
    for each letter
    """
    def __init__(self, letter):
        """ inits the letter"""
        self.text = letter
        self.size = DEFAULT_TEXT_SIZE
        self.color = blue #text color
        self.backColor = black #text background color
        self.x = 10 #where across the screen it is drawn
        self.y = 100 #where down the screen letter is rendered
        self.font = P.font.SysFont("Lucida Console", self.size) #rendered best with monospace font
        self.renderedText = self.font.render(self.text,1,self.color,self.backColor) #actually create the rendered text
        self.rectangle = self.renderedText.get_rect().move(self.x,self.y) #need to know the rectangle of text to interact
        
    def update(self):
        '''  update the rendered text and rectangle after changes
        '''
        self.font = P.font.SysFont("Lucida Console", self.size) #rendered best with monospace font
        self.renderedText = self.font.render(self.text,1,self.color,self.backColor) #actually create the rendered text
        self.rectangle = self.renderedText.get_rect().move(self.x,self.y) #need to know the rectangle of text to interact
        
#define other setup variables
alphabet = "abcdefghijklmnopqrstuvwxyz"
wordlist = "hummingbird" #kiwi, chicken, crow, stork, pigeon, swan, duck, peacock, parrot, sparrow, toucan, penguin, owl, hummingbird, seagull, ibis, emu, kingfisher, kookaburra, dove, conary, puffin, albatross, eagle.
lose = "You lose!!"

#create arrays to display the rendered letters
alphabetArray = [] #an initially empty array
for letter in alphabet:
    rLetter = renderedLetter(letter) #create an instance of the class renderedLetter
    alphabetArray.append(rLetter)
    
wordlistArray = [] #an initially empty array
for letter in wordlist:
    rLetter = renderedLetter(letter)
    wordlistArray.append(rLetter)

loseArray = [] #an initially empty array
for letter in lose:
    rLetter = renderedLetter(letter)
    loseArray.append(rLetter)

#draw alphabet letters on the screen
xPosition = 10 #across
yPosition = 400 #down
for l in alphabetArray:
    l.x = xPosition #set the x position of the rendered letter
    l.y = yPosition #set the y position of the rendered letter
    l.color = blue #start with letters blue
    l.backColor = purple
    l.update() #changed the properties so need to update
    screen.blit(l.renderedText,l.rectangle) #tell pygame where to draw next screen is flipped
    xPosition += (l.rectangle.width + 10) #move the x position to the right so letters not drawn on top of each other

xPosition = 10
yPosition = 200
for l in wordlistArray:
    l.x = xPosition
    l.y = yPosition
    l.color = lightBlue
    l.backColor = lightBlue
    l.size = DEFAULT_TEXT_SIZE #make the words twice as big
    l.update()
    screen.blit(l.renderedText,l.rectangle)
    xPosition += (l.rectangle.width + 20)


#everytihng up to here was setting up - now lets play

play = True  # controls whether to keep playing
guessesRemaining = 10
# game loop - runs 'loopRate' times a second!
while play:  # game loop - note:  everything in this loop is indented one tab

    for event in P.event.get():  # get user interaction events
        if event.type == P.QUIT:  # tests if window's X (close) has been clicked
            play = False  # causes exit of game loop
    # your code starts here ##############################
        elif event.type == P.MOUSEBUTTONDOWN:
            mousePosition = P.mouse.get_pos() #find out where they clicked
            
            #need to check all letters to see if they clicked on that letter
            for a in alphabetArray:
                if a.rectangle.collidepoint(mousePosition): #is the mouse click inside the letters rectangle
                    a.color = red
                    #a.update()
                    for v in wordlistArray: #check whether that letter is in the wordlist
                        if a.text == v.text: #compare text of clicked letter to the word's text
                            a.color = green
                            v.backColor = purple
                            v.update() #made changes so we need to update
                            screen.blit(v.renderedText, v.rectangle) #need to re-blit
                            guessCorrect = True #so it doesn't count as a loss of a guess
                    a.update() #made changes so we need to update
                    screen.blit(a.renderedText, a.rectangle) #need to re-blit
                
                    if guessCorrect == False: #to allow a guessing system
                        #update image
                        guessesRemaining -= 1
                        pass
                                                            
        if guessesRemaining == 0: #allows guessing system to end the game once all guesses are used up
            screen.fill(purple)
            for o in loseArray:
                o.x = xPosition
                o.y = yPosition
                o.color = blue
                o.backColor = purple
                o.update()
                screen.blit(o.renderedText,o.rectangle)
                xPosition += (o.rectangle.width + 10)
                #flash you lose
                P.quit()
                pass
            

      

    # your code ends here ###############################
    P.display.flip()  # makes any changes visible on the screen
    clock.tick(loopRate)  # limits game to frame per second, FPS value

# out of game loop ###############
P.quit()   # stops the game engine
sys.exit()  # close operating system window