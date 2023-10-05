import random

x = random.random()
print(f"{x:.2f}")

print(random.choice([-1, 1]))       


# Coin behavior test
"""if arcade.check_for_collision_with_lists(self.coin_sprite, self.enemy_collision_list):
            
            for enemy1 in self.enemy_sprite_list1:

                if self.coin_sprite.center_y >= enemy1.bottom:
                    self.coin_sprite.change_y = -self.coin_sprite.change_y + 1
                elif self.coin_sprite.center_y <= enemy1.top:
                    self.coin_sprite.change_y = -self.coin_sprite.change_y + 1
                
                if self.coin_sprite.center_x <= enemy1.right:
                    self.coin_sprite.change_x = -self.coin_sprite.change_x + 1
                elif self.coin_sprite.center_x >= enemy1.left:
                    self.coin_sprite.change_x = -self.coin_sprite.change_x + 1
            
            for enemy2 in self.enemy_sprite_list2:

                if self.coin_sprite.center_y >= enemy2.bottom:
                    self.coin_sprite.change_y = -self.coin_sprite.change_y + 1
                elif self.coin_sprite.center_y <= enemy2.top:
                    self.coin_sprite.change_y = -self.coin_sprite.change_y + 1
                
                if self.coin_sprite.center_x >= enemy2.right:
                    self.coin_sprite.change_x = -self.coin_sprite.change_x + 1
                elif self.coin_sprite.center_x <= enemy2.left:
                    self.coin_sprite.change_x = -self.coin_sprite.change_x + 1"""