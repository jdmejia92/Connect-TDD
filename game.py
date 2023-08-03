import pyfiglet

class Game:
  
  def start(self):
    # print the game's name or logo
    self.print_logo()

    # Set up the game
    # run the main loop
    
  def print_logo(self):
    logo = pyfiglet.Figlet(font='stop')
    print(logo.renderText('Connecta'))