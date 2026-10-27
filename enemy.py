from pgzero.builtins import Actor


class Enemy(Actor):
    def __init__(
        self,
        enemy_type,
        image,
        patrol_range=140,
        num_frames=2,
        has_left_sprite=True,
        **kwargs,
    ):
        super().__init__(image, **kwargs)
        self.anchor = ("center", "bottom")

        self.enemy_type = enemy_type
        self.speed = 2
        self.direction = 1

        self.start_x = None
        self.patrol_range = patrol_range

        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.15

        self.can_be_squished = "ghost" not in enemy_type

        self.is_dead = False
        self.dead_timer = 0
        self.should_remove = False

        if num_frames == 1:
            left_img = (
                f"enemies/{enemy_type}_left"
                if has_left_sprite
                else f"enemies/{enemy_type}"
            )
            self.animations = {
                "right": [f"enemies/{enemy_type}"],
                "left": [left_img],
            }
        else:
            self.animations = {
                "right": [
                    f"enemies/{enemy_type}1",
                    f"enemies/{enemy_type}2",
                ],
                "left": [
                    f"enemies/{enemy_type}1_left",
                    f"enemies/{enemy_type}2_left",
                ],
            }

    def squish(self):
        self.is_dead = True
        self.speed = 0

        side = "_dead_left" if self.direction == -1 else "_dead"
        self.image = f"enemies/{self.enemy_type}{side}"

    def update_enemy(self, dt):
        if self.is_dead:
            self.dead_timer += dt
            if self.dead_timer >= 0.3:
                self.should_remove = True
            return

        if self.start_x is None:
            self.start_x = self.x

        self.x += self.speed * self.direction

        if self.x >= self.start_x + self.patrol_range:
            self.direction = -1
        elif self.x <= self.start_x - self.patrol_range:
            self.direction = 1

        side = "right" if self.direction == 1 else "left"
        frames = self.animations.get(side, self.animations["right"])

        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
