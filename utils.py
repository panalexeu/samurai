from os import walk

import pygame


def import_sprites(sprites_path, animation_states: dict):
    for animation in animation_states.keys():
        full_path = sprites_path + '/' + animation + '/'
        animation_states[animation] = load_animation(full_path)

    return animation_states


def load_animation(path):
    surface_list = []

    for _, _, img_files in walk(path):
        for img in img_files:
            full_path = path + img
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
