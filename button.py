import time

import pygame

from src.utils import blit_centered, ninepatch, text
from src.data import BACKGROUND


class Button:
    MULTIPLE_CLICK_INTERVAL = 0.3
    BACKGROUND = BACKGROUND

    def __init__(
        self,
        rect,
        round_rect=False,
        circular=False,
        color=None,
        outcolor=None,
        images=None,
        resize=False,
        icon=None,
        label=None,
        sound=None,
        on_click=None,
        arguments=(),
    ):
        self.rect = pygame.Rect(rect)
        self.round_rect = round_rect
        self.circular = circular
        self.color = pygame.Color(color) if color else None
        self.outcolor = (
            outcolor
            if outcolor
            else self.color + pygame.Color(15, 15, 15)
            if color
            else None
        )
        self.images = (
            [ninepatch(image, tuple(self.rect)) for image in images]
            if resize
            else images
        )
        self.icon = icon
        self.label = label
        self.sound = sound
        self.on_click = on_click
        self.arguments = arguments

        self.last_clicked = 0
        self.click_count = 0

    def handle_event(self, event: pygame.event.Event):
        if self.mouseover and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if time.time() - self.last_clicked < self.MULTIPLE_CLICK_INTERVAL:
                    self.click_count += 1
                else:
                    self.click_count = 1
                self.last_clicked = time.time()
                if self.on_click:
                    for i, function in enumerate(self.on_click):
                        function(
                            self, *self.arguments[i] if len(self.arguments) > i else ()
                        )

    def draw(self, screen: pygame.Surface):
        if self.color:
            pygame.draw.rect(
                screen,
                self.outcolor if self.mouseover else self.color,
                self.rect,
                border_radius=min(self.rect.size) // 2
                if self.circular
                else min(self.rect.size) // 4
                if self.round_rect
                else 0,
            )
        if self.images:
            blit_centered(
                screen,
                self.images[1]
                if self.mouseclicking and len(self.images) > 1
                else self.images[0],
                self.rect,
            )
        if (self.icon and not self.label) or (
            self.icon and self.label and not self.mouseover
        ):
            blit_centered(screen, self.icon, self.rect)
        if (self.label and not self.icon) or (
            self.icon and self.label and self.mouseover
        ):
            blit_centered(
                screen,
                text(
                    self.label,
                    tuple(pygame.Color(255, 255, 255) - self.color)
                    if self.color
                    else tuple(
                        pygame.Color(255, 255, 255) - pygame.Color(self.BACKGROUND)
                    ),
                ),
                self.rect,
            )

    @property
    def mouseover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    @property
    def mouseclicking(self):
        return self.mouseover and pygame.mouse.get_pressed(num_buttons=3)[0]

    def play_sound(self):
        self.sound.play()

    def update_text(self, new_text=""):
        if new_text:
            self.label = new_text
        else:
            times = (
                "once"
                if self.click_count == 1
                else "twice"
                if self.click_count == 2
                else "many times"
            )
            self.label = "I've been clicked " + times

    def put_exit(self, exit_routine=None):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        if exit_routine:
            exit_routine()
