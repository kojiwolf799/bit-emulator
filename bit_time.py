import pygame


_last_tick = pygame.time.get_ticks()


def sleep_ms(ms):

    global _last_tick

    now = pygame.time.get_ticks()

    elapsed = now - _last_tick

    remaining = ms - elapsed

    if remaining > 0:
        pygame.time.wait(remaining)

    _last_tick = pygame.time.get_ticks()
