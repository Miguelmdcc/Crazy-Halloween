from pgzero.builtins import Actor


class Zombie(Actor):
    def __init__(self, image, **kwargs):
        super().__init__(image, **kwargs)
        self.x_speed = 4
        self.anchor = ("center", "bottom")
        self.frame_index = 0
        self.anim_timer = 0
        self.direction = 1
        self.state = "idle"

        self.coins = 0
        self.life = 2

        self.anim_speeds = {
            "idle": 0.30,
            "walk": 0.12,
            "jump": 0.12,
        }

        self.animations = {
            "idle_right": [
                "zombie/idle/zombie_stand",
                "zombie/idle/zombie_idle",
                "zombie/idle/zombie_talk",
            ],
            "idle_left": [
                "zombie/idle/zombie_stand_left",
                "zombie/idle/zombie_idle_left",
                "zombie/idle/zombie_talk_left",
            ],
            "walk_right": [
                "zombie/walk/zombie_walk1",
                "zombie/walk/zombie_walk2",
            ],
            "walk_left": [
                "zombie/walk/zombie_walk1_left",
                "zombie/walk/zombie_walk2_left",
            ],
            "jump_right": ["zombie/jump/zombie_jump"],
            "jump_left": ["zombie/jump/zombie_jump_left"],
            "cheer_right": [
                "zombie/cheer/zombie_cheer1",
                "zombie/cheer/zombie_cheer2",
            ],
            "cheer_left": [
                "zombie/cheer/zombie_cheer1_left",
                "zombie/cheer/zombie_cheer2_left",
            ],
        }

        self.vel_y = 0
        self.gravity = 0.8
        self.jump_strength = -14
        self.on_ground = False

    def walking(self, direction, tiles):
        self.x += self.x_speed * direction
        if self.x >= 1280:
            self.x = 1280
        if self.x <= 0:
            self.x = 0
        if self.direction != direction:
            self.direction = direction
            self.frame_index = 0
            self.anim_timer = 0
            self.apply_current_frame()
        if self.on_ground == True:
            self.set_state("walk")
        for tile in tiles:
            platform = tile["actor"]
            if self.colliderect(platform) and direction == 1:
                self.right = platform.left
            if self.colliderect(platform) and direction == -1:
                self.left = platform.right

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False
            self.frame_index = 0
            self.anim_timer = 0
            self.apply_current_frame()
            self.set_state("jump")

    def cheer(self):
        self.set_state("cheer")
        self.apply_current_frame()

    def update_physics(self, tiles):
        self.vel_y += self.gravity
        self.y += self.vel_y
        self.on_ground = False

        for tile in tiles:
            platform = tile["actor"]
            if self.colliderect(platform):
                if self.vel_y > 0:
                    self.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.top = platform.bottom
                    self.vel_y = 0

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.frame_index = 0
            self.anim_timer = 0
            self.apply_current_frame()

    def apply_current_frame(self):
        """Força a atualização imediata do sprite na tela."""
        side = "right" if self.direction == 1 else "left"
        anim_key = f"{self.state}_{side}"
        frames = self.animations[anim_key]
        self.frame_index = self.frame_index % len(frames)
        self.image = frames[self.frame_index]

    def update_animation(self, dt):
        side = "right" if self.direction == 1 else "left"
        anim_key = f"{self.state}_{side}"
        frames = self.animations[anim_key]

        speed = self.anim_speeds.get(self.state, 0.15)

        self.anim_timer += dt
        if self.anim_timer >= speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
