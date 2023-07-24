import sprite


class Projectile(sprite.Sprite):
    def __init__(self, pos, image_path, speed, direction):
        super().__init__(
            pos,
            image_path=image_path
        )

        self.speed = speed
        self.direction = direction

    def movement(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def update(self):
        self.movement()
