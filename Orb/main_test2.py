import arcade
import arcade.gui
import json
from arcade import SpriteSolidColor
import random
from pathlib import Path

working_directory = Path(__file__).absolute().parent


WINDOW_WIDTH = 1000        # Set our game's window properties.
WINDOW_HEIGHT = 1000
WINDOW_TITLE = "Reflex"

player_radius = 15         # Player character properties.     
player_speed = 3

enemy_radius = 26          # Enemy properties.




class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.texture = arcade.make_circle_texture(player_radius, arcade.color.ORANGE_PEEL)

    def update(self):      # Updates the state of the player sprite.

        self.center_x += self.change_x           # Player movement. 
        self.center_y += self.change_y

        if self.left < 0:                        # The player can t go outside the screen.
            self.left = 0
        elif self.right >= WINDOW_WIDTH: 
            self.right = WINDOW_WIDTH - 1
        if self.bottom < 0: 
            self.bottom = 0
        elif self.top >= WINDOW_HEIGHT: 
            self.top = WINDOW_HEIGHT - 1



class Enemies(arcade.Sprite):
    def __init__(self, enemy_speed):
        super().__init__()
        
        self.texture = arcade.make_soft_square_texture(enemy_radius, 
                                                       arcade.color.BLUEBERRY, 
                                                       outer_alpha=255)
        self.enemy_speed = enemy_speed

        
    def update(self):

        self.center_y -= self.enemy_speed   # Updates the player movement by the enemy speed.



class MainMenuView(arcade.View):
    def __init__(self, level_mode_time=None, level_mode_obstacle=None, level_mode_score=None, enemy_speed=4):
        super().__init__() 

        self.level_mode_time = level_mode_time
        self.level_mode_obstacle = level_mode_obstacle
        self.level_mode_score = level_mode_score
        
    def setup(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
            
        self.v_box = arcade.gui.UIBoxLayout(150, 700, space_between=20) # Creates a vertical BoxGroup to align buttons.

        self.leveling_buttons_style = {"font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": (21, 19, 21),
            # Used if buttons are pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.WHITE,  # Also used when hovered
            "font_color_pressed": arcade.color.BLACK
            }
            
        self.button_time = arcade.gui.UIFlatButton(text="TIME", width=200, 
                                                   style=self.leveling_buttons_style)
        self.button_obstacles = arcade.gui.UIFlatButton(text="OBSTACLES", width=200, 
                                                        style=self.leveling_buttons_style)
        self.button_score = arcade.gui.UIFlatButton(text="SCORE", width=200, 
                                                    style=self.leveling_buttons_style)
            
        self.v_box.add(self.button_time)
        self.v_box.add(self.button_obstacles)
        self.v_box.add(self.button_score)

        self.manager.add(self.v_box) # Adds a widget to hold the v_box widget, that will center the buttons


    def on_draw(self):
            
            self.clear()

            self.texture = arcade.set_background_color(arcade.color.BATTLESHIP_GREY)

            arcade.draw_text("LEVELING SYSTEM", start_x=100, start_y=750, 
                            color=arcade.color.BARN_RED, font_size=24, bold=True)

            self.manager.draw()


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.button_time.on_click = self.go_play_time
            self.button_obstacles.on_click = self.go_play_obstacle
            self.button_score.on_click = self.go_play_score

    
    def go_play_time(self, event):

        self.level_mode_time = True
        
        game_view = GameView(self.level_mode_obstacle, None, None)
        game_view.setup()
        self.manager.disable()
        self.window.show_view(game_view)
        
    

    def go_play_obstacle(self, event):
        
        self.level_mode_obstacle = True

        game_view = GameView(None, self.level_mode_obstacle, None)
        game_view.setup()
        self.manager.disable()
        self.window.show_view(game_view)

    
    def go_play_score(self, event):
    
        self.level_mode_score = True

        game_view = GameView(None, None, self.level_mode_score)
        game_view.setup()
        self.manager.disable()
        self.window.show_view(game_view)
    


class PauseView(arcade.View):
    def __init__(self, gameview_reference):
        super().__init__()

        self.gameview_reference = gameview_reference

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.mainmenu_button_style = {"font_name": ("calibri", "arial"),
                    "font_size": 15,
                    "font_color": arcade.color.WHITE,
                    "border_width": 2,
                    "border_color": None,
                    "bg_color": (21, 19, 21),
                    # Used if buttons are pressed
                    "bg_color_pressed": arcade.color.BLUE_BELL,
                    "border_color_pressed": arcade.color.BLUE_BELL,  # Also used when hovered
                    "font_color_pressed": arcade.color.WHEAT
                    }

        self.button_mainmenu = arcade.gui.UIFlatButton(WINDOW_WIDTH/2, 50, 
                                                       width=200, text="MAIN MENU",
                                                       style=self.mainmenu_button_style)
        
        

        self.manager.add(self.button_mainmenu)

        self.leaderboard_list = list()         # Top scores leaderboard list holding the json file data.

        try:
            with open(working_directory / 'leaderboard.json', "r") as file:
                self.leaderboard_list = json.load(file)
                file.close()
        except:
            print("leaderboard.json load ERROR")

        self.leaderboard_multiline = '\n'.join([f"{name}:{score}" for placement in self.leaderboard_list    # Making the leaderboard list into a string and formatting it  
                                                                for name, score in placement.items()])      # with each pair name:score on a new line
        self.leaderboard_start_y = None


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.button_mainmenu.on_click = self.go_mainmenu


    def go_mainmenu(self, event):
        
        main_menu = MainMenuView()
        main_menu.setup()
        self.manager.disable()
        self.window.show_view(main_menu)


    def on_draw(self):
        
        arcade.start_render()
        
        self.texture = arcade.set_background_color(arcade.color.GREEN_YELLOW)

        self.manager.draw()

        self.leaderboard_backround = arcade.draw_rectangle_filled(200, 500,
                                                                  400, 500,
                                                                  arcade.color.WHITE_SMOKE)
        
        self.leaderboard_text = arcade.draw_text("TOP 10 LEADERBOARD", 
                                                 30, 725,
                                                 arcade.color.RED_DEVIL, font_size=22, width=150)
        
        self.leaderboard_start_y = 675

        for placement in self.leaderboard_list:
            name = list(placement.keys())[0]
            points = list(placement.values())[0]
            self.leaderboard = arcade.draw_text(f"{name}: {points}", 
                            40, self.leaderboard_start_y, 
                            arcade.color.BLACK, font_size=20)
            self.leaderboard_start_y -= 30
        

    def on_key_press(self, key, modifier):

        if key == arcade.key.ESCAPE:
            
            self.window.show_view(self.gameview_reference)



class GameOverView(arcade.View):
    def __init__(self, score, level_mode_time=None, level_mode_obstacles=None, level_mode_score=None, enemy_speed = 4):
        super().__init__()

        self.level_mode_time = level_mode_time
        self.level_mode_obstacles = level_mode_obstacles
        self.level_mode_score = level_mode_score

        self.enemy_speed = enemy_speed

        self.score = score

        self.leaderboard_list = list()         # Top scores leaderboard list holding the json file data.
        try:
            with open(working_directory / 'leaderboard.json', "r") as file:
                self.leaderboard_list = json.load(file)
                file.close()
        except:
            print("leaderboard.json load ERROR")

        self.manager = arcade.gui.UIManager()     # The UI Manager. The class to which all UI elemets must be added to.
        self.manager.enable()

        self.name_input = arcade.gui.UIInputText(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2,  # Ask for the name of the player.
                                                 200, 50, 
                                                 "name:", font_size=20, )
        
        self.manager.add(self.name_input)  # Add the widget to the Manager.
        
    
    def on_show_view(self):
        
        arcade.set_viewport(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

    def on_draw(self):

        self.clear()
        
        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        arcade.draw_lrtb_rectangle_filled(self.name_input.center_x - self.name_input.width/2, 
                                          self.name_input.center_x + self.name_input.width/2, 
                                          self.name_input.center_y + self.name_input.height/2, 
                                          self.name_input.center_y - self.name_input.height/4, 
                                          arcade.color.FLORAL_WHITE)

        self.manager.draw()

        arcade.draw_text("GAME OVER", 
                         WINDOW_WIDTH/2, WINDOW_HEIGHT - 250, 
                         arcade.color.BLACK, 60, 
                         anchor_x="center")
        arcade.draw_text(f"your score: {self.score}", WINDOW_WIDTH/2,
                          WINDOW_HEIGHT - 350, 
                          arcade.color.ALABAMA_CRIMSON, 40, 
                          anchor_x="center")
        arcade.draw_text("SPACE BAR to restart", 
                         WINDOW_WIDTH/2, WINDOW_HEIGHT - 800, 
                         arcade.color.BLACK, 40, 
                         anchor_x="center")
    
    def on_key_press(self, key, modifier):
        
        if key == arcade.key.ENTER and self.name_input.text:         # If you press enter and you ve written (name of the player) in the input box
            player_name = self.name_input.text 
            if len(self.leaderboard_list) < 10 or self.score > any([value for name, value in self.leaderboard_list]):
            
                self.leaderboard_list.append({player_name: self.score})
                self.leaderboard_list = sorted(self.leaderboard_list, key=lambda x: list(x.values()), reverse=True)
            
            with open(working_directory / 'leaderboard.json', "w") as file:
                json.dump(self.leaderboard_list, file, indent= 1)
                file.close()

        if key == arcade.key.SPACE:
            game_view = GameView(self.enemy_speed, self.level_mode_time, self.level_mode_obstacles, self.level_mode_score)
            game_view.setup()
            self.manager.disable()
            self.window.show_view(game_view)  # Go back to the game.
            

                  
class GameView(arcade.View):                   # Child class for the game of the parent class View.
    def __init__(self, level_mode_time=None, level_mode_obstacles=None, level_mode_score=None, enemy_speed = 4):    # Set the parameters for the new class. 
        super().__init__()   # With super we pair the parameters of the new class with the View class.
                                                            # Create sprites and sprite lists here.
        self.level_mode_time = level_mode_time
        self.level_mode_obstacles = level_mode_obstacles
        self.level_mode_score = level_mode_score

        self.enemy_speed = enemy_speed

        self.level = None
        self.obstacle_count = None

        self.player_sprite = None

        self.enemy_sprite = None                
        self.enemy_sprite_list1 = None
        self.enemy_sprite_list2 = None
        self.enemy_sprite_list3 = None
        self.enemy_collision_list = None


        self.score = None
        self.score_text = None
        self.score_updated1 = None
        self.score_updated2 = None              

        self.current_keys = None               # The list of key that are currently being pressed.

                 
    def setup(self):                            # Set up the game variables. Call to re-start the game.
                                                # Set you sprites and sprite lists properties here.
        self.player_sprite = Player()
        self.player_sprite.center_x = WINDOW_WIDTH/2 - player_radius/2  # To position the player sprite
        self.player_sprite.center_y = WINDOW_HEIGHT/2 - player_radius/2 # (in this case at the center of the screen).

        self.enemy_sprite_list1 = arcade.SpriteList()
        self.enemy_sprite_list2 = arcade.SpriteList()
        self.enemy_sprite_list3 = arcade.SpriteList()
        self.enemy_collision_list = [self.enemy_sprite_list1, self.enemy_sprite_list2, self.enemy_sprite_list3]

        self.enemy_speed = 4

        self.level = 1
        self.obstacle_count = 0

        self.score = 0
        self.score_updated1 = False              # Score shouldn t update untill the player passe the obstacle
        self.score_updated2 = False
        self.score_text = arcade.Text(f"SCORE: {self.score}", 
                                      5, WINDOW_HEIGHT - 15, 
                                      arcade.color.BROWN, 9, bold=True)
        self.current_keys = set()

        
    def on_update(self, delta_time):            # Event handler. Updates the state on the game objects.

            self.player_sprite.update()             # Calling the update function of the player class to update its state.

            
            self.leveling_mode()
            
            self.enemy_spawns()
            
            self.scoring()

            self.enemy_sprite_list1.update()
            self.enemy_sprite_list2.update()

            self.collisions()

        
    def on_draw(self):                          # Method responsible for rendering (drawing) on the screen.

        arcade.start_render()

        arcade.set_background_color(arcade.color.ARSENIC)

        self.player_sprite.draw()               # Draws the player sprite on the screen.
        self.enemy_sprite_list1.draw()
        self.enemy_sprite_list2.draw()
        self.score_text.draw()
    
  
    def on_key_press(self, key, modifier):                   # Reads key presses.

        
            self.current_keys.add(key)

            if key == arcade.key.ESCAPE:
                self.window.show_view(PauseView(self))
            
            if key == arcade.key.A:                              # Setting ASDW directional keys for player movement.
                self.player_sprite.change_x = -player_speed 
            if key == arcade.key.D:
                self.player_sprite.change_x = player_speed 
            if key == arcade.key.S:
                self.player_sprite.change_y = -player_speed 
            if key == arcade.key.W: 
                self.player_sprite.change_y = player_speed
    

    def on_key_release(self, key, modifier):                 # Reads key releases.
        
        
            if key in self.current_keys:
                self.current_keys.remove(key)

            if (key == arcade.key.A or key == arcade.key.D) \
                and (arcade.key.A not in self.current_keys and arcade.key.D not in self.current_keys):  # Handles realease and press of multiple keys at once
                self.player_sprite.change_x = 0                                                         # allowing the player to move after a key release if 
            elif key == arcade.key.A and arcade.key.D in self.current_keys:                             # another key is still being pressed.
                self.player_sprite.change_x = player_speed 
            elif key == arcade.key.D and arcade.key.A in self.current_keys:
                self.player_sprite.change_x = -player_speed 

            if (key == arcade.key.S or key == arcade.key.W) \
                and (arcade.key.S not in self.current_keys and arcade.key.W not in self.current_keys):
                self.player_sprite.change_y = 0
            elif key == arcade.key.S and arcade.key.W in self.current_keys:
                self.player_sprite.change_y = player_speed 
            elif key == arcade.key.W and arcade.key.S in self.current_keys:
                self.player_sprite.change_y = -player_speed 
    

    def enemy_spawns(self):

        if len(self.enemy_sprite_list1) == 0:
            enemy_count1 = random.randint(18,35)             # To set a random number of enemies to spawn (first row)
            self.obstacle_count += 1

            for _ in range(enemy_count1):                    # Populating the first row on enemies.
                self.enemy_sprite = Enemies(self.enemy_speed)
                self.enemy_sprite_list1.append(self.enemy_sprite)
            
            for enemy in self.enemy_sprite_list1:            # Setting the positions of the first row of enemies.
                enemy.center_x = random.randrange(0 + enemy_radius/2, WINDOW_WIDTH - enemy_radius/2, enemy_radius)
                enemy.center_y = WINDOW_HEIGHT + enemy_radius*2
                while arcade.check_for_collision_with_list(enemy, self.enemy_sprite_list1): # So that enemies don t spawn overlapped.
                    enemy.center_x = random.randrange(0 + enemy_radius/2, WINDOW_WIDTH - enemy_radius/2, enemy_radius)
        
        for enemy1 in self.enemy_sprite_list1:
            
            if enemy1.center_y <= WINDOW_HEIGHT/2 and len(self.enemy_sprite_list2) == 0: # When the first row of enemy is at half screen (500) we create and spawn the second row.
                enemy_count2 = random.randint(18,35)            # To set a random number of enemies to spawn (second row)
                self.obstacle_count += 1
                
                for _ in range(enemy_count2):                   # Populating the second row of enemies. 
                    self.enemy_sprite = Enemies(self.enemy_speed) 
                    self.enemy_sprite_list2.append(self.enemy_sprite)
               
                for enemy2 in self.enemy_sprite_list2:          # Setting the positions of the second row of enemies.
                    enemy2.center_x = random.randrange(0 + enemy_radius/2, WINDOW_WIDTH - enemy_radius/2, enemy_radius)
                    enemy2.center_y = WINDOW_HEIGHT + enemy_radius*2
                    while arcade.check_for_collision_with_list(enemy2, self.enemy_sprite_list2): # So that enemies don t spawn overlapped.
                        enemy2.center_x = random.randrange(0 + enemy_radius/2, WINDOW_WIDTH - enemy_radius/2, enemy_radius)
                    
            if enemy1.center_y < 0:              # When the obstacles's center is below the screen 
                self.enemy_sprite_list1.clear()  # clear the sprite list.
                self.score_updated1 = False       # Current row's score can be updated again. 
        
        for enemy2 in self.enemy_sprite_list2:

            if enemy2.center_y < 0:
                self.enemy_sprite_list2.clear()
                self.score_updated2 = False       # Current row's score can be updated again.


    def collisions(self):

        if arcade.check_for_collision_with_lists(self.player_sprite, self.enemy_collision_list): # Checking for collision between player and falling obstacles.
            self.window.show_view(GameOverView(self.score, self.level_mode_time, self.level_mode_obstacles, self.level_mode_score))
    

    def leveling_mode(self):

        if self.level_mode_score:
            if self.score >= self.level * 200:
                self.enemy_speed = self.enemy_speed + 0.5
                self.level += 1
        
        elif self.level_mode_obstacles:
            if self.obstacle_count >= self.level * 10:
                self.enemy_speed = self.enemy_speed + 0.5
                self.level += 1


    def scoring(self):
        
        for enemy1 in self.enemy_sprite_list1:

            if self.player_sprite.center_y > enemy1.center_y and self.score_updated1 == False: # Check if player has passed the obstacle
                self.score += len(self.enemy_sprite_list1)  # Adds the number of obstacles to the score
                self.score_updated1 = True                   # Don't update the score again untill obstacles's center is under the screen.
            
        for enemy2 in self.enemy_sprite_list2:

            if self.player_sprite.center_y > enemy2.center_y and self.score_updated2 == False:
                self.score += len(self.enemy_sprite_list2)
                self.score_updated2 = True
            
            
        self.score_text.text = f"SCORE: {self.score}"  # Updating the score widget on screenc   
        


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, center_window=True)
     
    main_menu = MainMenuView()
    main_menu.setup()
    window.show_view(main_menu)

    arcade.run()


if __name__ == "__main__":          # Checks if the program is being run deirectly from the file. Won t run if the file is imported
    main()