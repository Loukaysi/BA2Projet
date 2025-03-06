import arcade
from gameview import GameView
from gameview import Map

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

def main() -> None:
    """Main function."""

    # Test read map
    Mapp = Map()
    Mapp.ReadMap("map/map1.txt")
    Mapp.ShowMap()

    # Create the (unique) Window, setup our GameView, and launch
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game_view = GameView()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()