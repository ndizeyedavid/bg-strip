from typing import Tuple

PREDEFINED_COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "transparent": None,
    "light_gray": (200, 200, 200),
    "dark_gray": (50, 50, 50),
    "custom": "custom"
}

def parse_color(color_input: str) -> Tuple[int, int, int] | None:
    """Parse color input (hex, rgb, or predefined name)"""
    color_input = color_input.strip().lower()
    
    if color_input in PREDEFINED_COLORS and color_input != "custom":
        return PREDEFINED_COLORS[color_input]
    
    if color_input.startswith("#"):
        hex_color = color_input.lstrip("#")
        if len(hex_color) == 6:
            try:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                    return (r, g, b)
            except ValueError:
                pass
    
    if "rgb" in color_input:
        try:
            numbers = [int(x) for x in color_input.replace("rgb", "").replace("(", "").replace(")", "").split(",")]
            if len(numbers) == 3 and all(0 <= n <= 255 for n in numbers):
                return (numbers[0], numbers[1], numbers[2])
        except ValueError:
            pass
    
    try:
        numbers = [int(x) for x in color_input.replace(" ", "").split(",")]
        if len(numbers) == 3 and all(0 <= n <= 255 for n in numbers):
            return (numbers[0], numbers[1], numbers[2])
    except ValueError:
        pass
    
    return PREDEFINED_COLORS["white"]
