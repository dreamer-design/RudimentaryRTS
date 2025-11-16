import pygame

class Button:
    def __init__(self, x, y, w=64, h=64,
                 color_idle=(60,60,60),
                 color_hover=(90,90,90)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_idle = color_idle
        self.color_hover = color_hover
        self.hover = False

    # check if within the box
    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        color = self.color_hover if self.hover else self.color_idle
        pygame.draw.rect(screen, color, self.rect)

    def handle_event(self, event):
        """Returns:
            'left'  if left click on button
            'right' if right click on button
            None    otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover:
                if event.button == 1:
                    return 'left'
                elif event.button == 3:
                    return 'right'
        return None
