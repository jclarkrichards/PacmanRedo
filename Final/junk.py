    def render(self, screen):
        if self.visible:
            if self.image is not None:
                #newtext::adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
                #newtext::p = self.position - adjust
                #newtext::screen.blit(self.image, p.asTuple())
                #strikeout::screen.blit(self.image, self.position.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)