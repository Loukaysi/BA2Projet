import arcade

from gameview import GameView

INITIAL_COIN_COUNT = 5

DISTANCE_FROM_UPPER_CAM = 300
DISTANCE_FROM_LOWER_CAM = 200
DISTANCE_FROM_RIGHT_CAM = 550
DISTANCE_FROM_LEFT_CAM = 550

def test_collect_coins(window: arcade.Window) -> None:
    """view = GameView()
    window.show_view(view)

    # Make sure we have the amount of coins we expect at the start
    assert len(view.coin_sprite_list) == INITIAL_COIN_COUNT

    # Start moving right
    view.on_key_press(arcade.key.RIGHT, 0)

    # Let the game run for 1 second
    window.test(60)

    # We should have collected the first coin
    assert len(view.coin_sprite_list) == INITIAL_COIN_COUNT - 1

    # Jump to get past the first crate
    view.on_key_press(arcade.key.UP, 0)
    view.on_key_release(arcade.key.UP, 0)

    # Let the game run for 1 more second
    window.test(60)

    # We should have collected the second coin
    assert len(view.coin_sprite_list) == INITIAL_COIN_COUNT - 2"""
    pass

def test_camera_position(window: arcade.Window) -> None:
    """# Crée la fenêtre
    view = GameView()
    window.show_view(view)
    
    # Check for the valid camera position
    assert(camera_test(view.player_sprite,view.camera))

    # Start moving right
    view.on_key_press(arcade.key.RIGHT, 0)

    # Let the game run for 1 second
    window.test(60)

    # Check for the valid camera position
    assert(camera_test(view.player_sprite,view.camera))

    # Jump to get past the first crate
    view.on_key_press(arcade.key.UP, 0)
    view.on_key_release(arcade.key.UP, 0)

    # Let the game run for 1 more second
    window.test(60)

    # Check for the valid camera position
    assert(camera_test(view.player_sprite,view.camera))

    # Jump to get past the first crate
    view.on_key_press(arcade.key.UP, 0)
    view.on_key_release(arcade.key.UP, 0)

    # Let the game run for 1 more second
    window.test(60)

    # Jump to get past the first crate
    view.on_key_press(arcade.key.UP, 0)
    view.on_key_release(arcade.key.UP, 0)

    # Let the game run for 1 more second
    window.test(60)

    # Check for the valid camera position
    assert(camera_test(view.player_sprite,view.camera))"""
    pass


def camera_test(player: arcade.Sprite, camera:arcade.Camera2D) -> bool:
    """# Calcule la différence entre le joueur et la caméra
    x = player.position[0] - camera.position.x
    y = player.position[1] - camera.position.y
    # Vérifie que les distances sont dans les limites voulues
    return (x<= DISTANCE_FROM_RIGHT_CAM and x >= -DISTANCE_FROM_LEFT_CAM and
           y<= DISTANCE_FROM_UPPER_CAM and y>= -DISTANCE_FROM_LOWER_CAM)"""
    return False
    pass