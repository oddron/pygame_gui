import os
import pytest
import pygame

from tests.shared_fixtures import _init_pygame, default_ui_manager, default_display_surface, \
    _display_surface_return_none

from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_screen_space_health_bar import UIScreenSpaceHealthBar
from pygame_gui.core.ui_container import UIContainer


class HealthySprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.health_capacity = 100
        self.current_health = 75
        self.rect = pygame.Rect(150, 150, 50, 75)


class HealthySpriteNoCapacity(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.current_health = 75
        self.rect = pygame.Rect(150, 150, 50, 75)


class HealthySpriteNoCurrentHealth(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.health_capacity = 100
        self.rect = pygame.Rect(150, 150, 50, 75)


class TestUIScreenSpaceHealthBar:

    def test_creation_with_sprite(self, _init_pygame, default_ui_manager):
        healthy_sprite = HealthySprite()
        UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                               sprite_to_monitor=healthy_sprite,
                               manager=default_ui_manager)

    def test_creation_no_sprite(self, _init_pygame, default_ui_manager):
        UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                               sprite_to_monitor=None,
                               manager=default_ui_manager)

    def test_creation_sprite_no_capacity(self, _init_pygame, default_ui_manager):
        healthy_sprite = HealthySpriteNoCapacity()
        with pytest.raises(AttributeError, match="Sprite does not have health_capacity attribute"):
            UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                                   sprite_to_monitor=healthy_sprite,
                                   manager=default_ui_manager)

    def test_creation_sprite_no_current_health(self, _init_pygame, default_ui_manager):
        healthy_sprite = HealthySpriteNoCurrentHealth()
        with pytest.raises(AttributeError, match="Sprite does not have current_health attribute"):
            UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                                   sprite_to_monitor=healthy_sprite,
                                   manager=default_ui_manager)

    def test_set_sprite_to_monitor(self, _init_pygame, default_ui_manager):
        healthy_sprite = HealthySprite()
        health_bar = UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                                            sprite_to_monitor=None,
                                            manager=default_ui_manager)

        health_bar.set_sprite_to_monitor(healthy_sprite)

    def test_set_sprite_to_monitor_no_capacity(self, _init_pygame, default_ui_manager):
        healthy_sprite = HealthySpriteNoCapacity()
        health_bar = UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                                            sprite_to_monitor=None,
                                            manager=default_ui_manager)
        with pytest.raises(AttributeError, match="Sprite does not have health_capacity attribute"):
            health_bar.set_sprite_to_monitor(healthy_sprite)

    def test_set_sprite_to_monitor_no_current_health(self, _init_pygame, default_ui_manager):
        healthy_sprite = HealthySpriteNoCurrentHealth()
        health_bar = UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                                            sprite_to_monitor=None,
                                            manager=default_ui_manager)
        with pytest.raises(AttributeError, match="Sprite does not have current_health attribute"):
            health_bar.set_sprite_to_monitor(healthy_sprite)

    def test_update(self, _init_pygame, default_ui_manager):
        healthy_sprite = HealthySprite()
        health_bar = UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                                            sprite_to_monitor=healthy_sprite,
                                            manager=default_ui_manager)
        healthy_sprite.current_health = 10
        health_bar.update(0.01)
        assert health_bar.image is not None

    def test_rebuild_from_theme_data_non_default(self, _init_pygame):
        manager = UIManager((800, 600), os.path.join("tests", "data", "themes",
                                                     "ui_screen_health_bar_non_default.json"))
        healthy_sprite = HealthySprite()
        health_bar = UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                                            sprite_to_monitor=healthy_sprite,
                                            manager=manager)
        assert health_bar.image is not None

    @pytest.mark.filterwarnings("ignore:Invalid value")
    @pytest.mark.filterwarnings("ignore:Colour hex code")
    def test_rebuild_from_theme_data_bad_values(self, _init_pygame):
        manager = UIManager((800, 600), os.path.join("tests", "data", "themes", "ui_screen_health_bar_bad_values.json"))
        healthy_sprite = HealthySprite()
        health_bar = UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                                            sprite_to_monitor=healthy_sprite,
                                            manager=manager)
        assert health_bar.image is not None

    def test_set_position(self, _init_pygame, default_ui_manager):
        healthy_sprite = HealthySprite()
        test_container = UIContainer(relative_rect=pygame.Rect(100, 100, 300, 60), manager=default_ui_manager)
        screen_space_health_bar = UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                                                         sprite_to_monitor=healthy_sprite,
                                                         container=test_container,
                                                         manager=default_ui_manager)

        screen_space_health_bar.set_position((150.0, 30.0))

        assert screen_space_health_bar.relative_rect.topleft == (50, -70)

    def test_set_relative_position(self, _init_pygame, default_ui_manager):
        healthy_sprite = HealthySprite()
        test_container = UIContainer(relative_rect=pygame.Rect(50, 50, 300, 250), manager=default_ui_manager)
        screen_space_health_bar = UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                                                         sprite_to_monitor=healthy_sprite,
                                                         container=test_container,
                                                         manager=default_ui_manager)

        screen_space_health_bar.set_relative_position((50.0, 30.0))

        assert screen_space_health_bar.rect.topleft == (100, 80)

    def test_set_dimensions(self, _init_pygame, default_ui_manager):
        healthy_sprite = HealthySprite()
        test_container = UIContainer(relative_rect=pygame.Rect(50, 50, 300, 250), manager=default_ui_manager)
        health_bar = UIScreenSpaceHealthBar(relative_rect=pygame.Rect(100, 100, 150, 30),
                                            sprite_to_monitor=healthy_sprite,
                                            container=test_container,
                                            manager=default_ui_manager)

        health_bar.set_dimensions((250.0, 60.0))

        assert health_bar.drawable_shape.containing_rect.size == (250, 60)
        assert health_bar.rect.size == (250, 60)
        assert health_bar.relative_rect.size == (250, 60)
