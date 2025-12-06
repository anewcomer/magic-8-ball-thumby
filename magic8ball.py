import thumby
import time
import random

# Display dimensions
SCREEN_WIDTH = 72
SCREEN_HEIGHT = 40

# The 20 authentic Magic 8 Ball phrases
MAGIC_8_BALL_PHRASES = [
    # Affirmative (10)
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes definitely",
    "You may rely on it",
    "As I see it yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    # Non-committal (5)
    "Reply hazy try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    # Negative (5)
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful"
]

# 8-ball sprite (top view) - 24x24 pixels circle
# Represents the black 8-ball with white circle and "8" marking
BALL_WIDTH = 24
BALL_HEIGHT = 24
BALL_SPRITE = bytearray([
    # Row 0-7
    0x00, 0x00, 0xC0, 0xF0, 0xF8, 0xFC, 0xFE, 0xFE, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0xFE, 0xFC, 0xF8, 0xF0, 0xC0, 0x00, 0x00,
    # Row 8-15
    0x00, 0x1F, 0x7F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F, 0x1F, 0x00,
    # Row 16-23
    0x00, 0x00, 0x00, 0x01, 0x03, 0x07, 0x0F, 0x0F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x0F, 0x0F, 0x07, 0x03, 0x01, 0x00, 0x00, 0x00,
])

_ball_sprite_obj = None
_drawsprite_extended_signature = None

def draw_ball_sprite(x, y):
    """Compatibility wrapper for different drawSprite signatures."""
    global _ball_sprite_obj, _drawsprite_extended_signature

    if _drawsprite_extended_signature is None:
        try:
            thumby.display.drawSprite(BALL_SPRITE, x, y, BALL_WIDTH, BALL_HEIGHT)
        except TypeError:
            _drawsprite_extended_signature = False
        else:
            _drawsprite_extended_signature = True
            return

    if _drawsprite_extended_signature:
        thumby.display.drawSprite(BALL_SPRITE, x, y, BALL_WIDTH, BALL_HEIGHT)
        return

    sprite_cls = getattr(thumby, "Sprite", None)
    if sprite_cls is None:
        return

    if _ball_sprite_obj is None:
        _ball_sprite_obj = sprite_cls(BALL_WIDTH, BALL_HEIGHT, BALL_SPRITE)

    _ball_sprite_obj.x = x
    _ball_sprite_obj.y = y
    thumby.display.drawSprite(_ball_sprite_obj)

# Display constants
CHAR_WIDTH = 6  # Approximate pixel width per character

# Game states
STATE_IDLE = 0
STATE_SHAKING = 1
STATE_SHOWING_ANSWER = 2

def update_input_state():
    """Call thumby.inputUpdate when available for compatibility."""
    input_update = getattr(thumby, "inputUpdate", None)
    if callable(input_update):
        input_update()

class Magic8Ball:
    def __init__(self):
        self.state = STATE_IDLE
        self.current_phrase = ""
        self.frame_count = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        self.ball_x = (SCREEN_WIDTH - BALL_WIDTH) // 2
        self.ball_y = (SCREEN_HEIGHT - BALL_HEIGHT) // 2
        
    def check_any_button(self):
        """Check if any button or D-pad is pressed"""
        return (thumby.buttonU.justPressed() or 
                thumby.buttonD.justPressed() or 
                thumby.buttonL.justPressed() or 
                thumby.buttonR.justPressed() or 
                thumby.buttonA.justPressed() or 
                thumby.buttonB.justPressed())
    
    def draw_ball(self, offset_x=0, offset_y=0, brightness=255):
        """Draw the 8-ball with optional offset and brightness"""
        if brightness <= 0:
            return
            
        x = self.ball_x + offset_x
        y = self.ball_y + offset_y
        
        # Draw the main ball sprite using fast drawSprite method
        if brightness >= 255:
            # Full brightness - draw normally using optimized drawSprite
            draw_ball_sprite(x, y)
        else:
            # Reduced brightness - still use drawSprite but with dithering pattern
            # Create a dithered version by drawing at reduced opacity
            # Use 128 as threshold (brightness range 0-255): above this, sprite is visible enough
            # to draw normally; at or below, use heavy dithering to simulate fade effect
            if brightness > 128:
                draw_ball_sprite(x, y)
            else:
                # For very low brightness, use sparse checkerboard dithering
                # Draw every other pixel in a checkerboard pattern to simulate fading
                for sprite_y in range(BALL_HEIGHT):
                    for sprite_x in range(BALL_WIDTH):
                        # Checkerboard pattern: only draw if (x + y) is even
                        if (sprite_x + sprite_y) % 2 == 0:
                            byte_index = (sprite_y // 8) * BALL_WIDTH + sprite_x
                            bit_index = sprite_y % 8
                            if byte_index < len(BALL_SPRITE):
                                if BALL_SPRITE[byte_index] & (1 << bit_index):
                                    px = x + sprite_x
                                    py = y + sprite_y
                                    if 0 <= px < SCREEN_WIDTH and 0 <= py < SCREEN_HEIGHT:
                                        thumby.display.setPixel(px, py, 1)
        
        # Draw the white circle with "8" in the center
        center_x = x + BALL_WIDTH // 2
        center_y = y + BALL_HEIGHT // 2
        circle_radius = 6
        
        # Draw white circle using optimized approach
        for dy in range(-circle_radius, circle_radius + 1):
            # Calculate the width of the circle at this y position (once per dy)
            # Protect against domain errors when dy is at circle boundary
            dx_squared = circle_radius * circle_radius - dy * dy
            if dx_squared < 0:
                continue
            # Use max() for additional floating-point precision safety
            dx = int(max(0, dx_squared) ** 0.5)
            
            if brightness > 128:
                # Use filled circle approach - draw horizontal lines
                for x_offset in range(-dx, dx + 1):
                    px = center_x + x_offset
                    py = center_y + dy
                    if 0 <= px < SCREEN_WIDTH and 0 <= py < SCREEN_HEIGHT:
                        thumby.display.setPixel(px, py, 0)
            elif brightness > 0:
                # Dither white circle for low brightness using checkerboard pattern
                for x_offset in range(-dx, dx + 1):
                    # Use checkerboard pattern to maintain circle shape while reducing brightness
                    if (x_offset + dy) % 2 == 0:
                        px = center_x + x_offset
                        py = center_y + dy
                        if 0 <= px < SCREEN_WIDTH and 0 <= py < SCREEN_HEIGHT:
                            thumby.display.setPixel(px, py, 0)
        
        # Draw "8" in the circle
        if brightness >= 128:  # Only draw 8 if reasonably visible
            # Simple "8" using pixels - two stacked circles
            thumby.display.drawText("8", center_x - 2, center_y - 3, 1)
    
    def shake_animation(self):
        """Perform subtle shake animation"""
        # Simple shake pattern
        shake_patterns = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1),
            (0, 0)
        ]
        self.shake_offset_x, self.shake_offset_y = shake_patterns[self.frame_count % len(shake_patterns)]
    
    def wrap_text(self, text, max_width=12):
        """Wrap text to fit within max_width characters per line"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= max_width:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    lines.append(current_line)
                # Handle words that are too long - split recursively
                while len(word) > max_width:
                    lines.append(word[:max_width])
                    word = word[max_width:]
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def draw_text_centered(self, lines, brightness=255):
        """Draw text centered on screen with optional brightness"""
        if brightness <= 0:
            return
            
        line_height = 8
        total_height = len(lines) * line_height
        start_y = (SCREEN_HEIGHT - total_height) // 2
        
        for i, line in enumerate(lines):
            text_width = len(line) * CHAR_WIDTH
            x = (SCREEN_WIDTH - text_width) // 2
            y = start_y + i * line_height
            
            if brightness >= 255:
                thumby.display.drawText(line, x, y, 1)
            else:
                # Draw with reduced brightness using dithering
                for char_idx, char in enumerate(line):
                    char_x = x + char_idx * 6
                    # Simple dithering - skip some pixels based on brightness
                    if brightness > 128 or (char_idx + i) % 2 == 0:
                        thumby.display.drawText(char, char_x, y, 1)
    
    def update(self):
        """Update game state"""
        # Update input state to ensure button presses are detected when supported
        update_input_state()
        
        if self.state == STATE_IDLE:
            if self.check_any_button():
                # Start shaking
                self.state = STATE_SHAKING
                self.frame_count = 0
                # Pick a random phrase
                self.current_phrase = random.choice(MAGIC_8_BALL_PHRASES)
        
        elif self.state == STATE_SHAKING:
            self.frame_count += 1
            if self.frame_count >= 20:  # Shake for about 20 frames
                self.state = STATE_SHOWING_ANSWER
                self.frame_count = 0
        
        elif self.state == STATE_SHOWING_ANSWER:
            if self.check_any_button():
                # Return to idle
                self.state = STATE_IDLE
                self.shake_offset_x = 0
                self.shake_offset_y = 0
    
    def draw(self):
        """Draw current game state"""
        thumby.display.fill(0)
        
        if self.state == STATE_IDLE:
            self.draw_ball()
        
        elif self.state == STATE_SHAKING:
            self.shake_animation()
            self.draw_ball(self.shake_offset_x, self.shake_offset_y)
        
        elif self.state == STATE_SHOWING_ANSWER:
            lines = self.wrap_text(self.current_phrase)
            self.draw_text_centered(lines, 255)
        
        thumby.display.update()

# Main game loop
def main():
    game = Magic8Ball()
    
    while True:
        game.update()
        game.draw()
        time.sleep(0.05)  # ~20 FPS

if __name__ == "__main__":
    main()
