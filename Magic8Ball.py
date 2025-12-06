import thumby
import random
import time

# --- Configuration and Constants ---

# Screen size: 72x40 pixels
SCREEN_W = thumby.display.width
SCREEN_H = thumby.display.height

# Frame rate configuration (~20 FPS)
FRAME_DELAY = 0.05
SHAKE_DURATION_FRAMES = 40  # 2 seconds at 20 FPS

# Game States
STATE_IDLE = "IDLE"
STATE_SHAKE = "SHAKE"
STATE_ANSWER = "ANSWER"



# --- Magic 8 Ball Answers ---

ANSWERS = [
    # Affirmative (10)
    "It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", 
    "You may rely on it", "As I see it yes", "Most likely", "Outlook good", 
    "Yes", "Signs point to yes",
    # Non-Committal (5)
    "Reply hazy try again", "Ask again later", "Better not tell you now", 
    "Cannot predict now", "Concentrate and ask again",
    # Negative (5)
    "Don't count on it", "My reply is no", "My sources say no", 
    "Outlook not so good", "Very doubtful"
]


# --- Utility Functions ---

def wrap_text(text, max_chars=10):
    """Splits a string into lines, ensuring no line exceeds max_chars."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        # Check if adding the word (and a space) exceeds the limit
        if len(current_line) + len(word) + (1 if current_line else 0) <= max_chars:
            if current_line:
                current_line += " "
            current_line += word
        else:
            # Word won't fit, start a new line
            if current_line:
                lines.append(current_line)
            current_line = word
            
    if current_line:
        lines.append(current_line)
    return lines

def any_button_pressed():
    """Checks if any Thumby button has been newly pressed."""
    # We rely on the button objects handling their own state update when checked
    return (thumby.buttonA.justPressed() or thumby.buttonB.justPressed() or
            thumby.buttonU.justPressed() or thumby.buttonD.justPressed() or
            thumby.buttonL.justPressed() or thumby.buttonR.justPressed())

# --- Draw Functions ---

def draw_idle():
    """Draws the initial '8' waiting screen."""
    thumby.display.fill(0) # Black screen
    x = (SCREEN_W - 6) // 2
    y = (SCREEN_H - 8) // 2
    thumby.display.drawText("8", x, y, 1)


def draw_shake(frame):
    """Draws the shake animation for the text-based '8'."""
    thumby.display.fill(0) # Black screen
    
    # Calculate offset for a quick, jittery shake
    offset_x = (frame % 5) - 2 # Range -2 to 2
    offset_y = (frame % 3) - 1 # Range -1 to 1
    
    x = (SCREEN_W - 6) // 2 + offset_x
    y = (SCREEN_H - 8) // 2 + offset_y
    thumby.display.drawText("8", x, y, 1)


def draw_answer(answer_text):
    """Draws the answer text centered on the screen."""
    thumby.display.fill(0) # Black screen

    CENTER_X, CENTER_Y = SCREEN_W // 2, SCREEN_H // 2

    # Draw wrapped text in white (color 1)
    lines = wrap_text(answer_text, max_chars=10)
    
    # Calculate starting Y to center the block of text
    total_text_height = len(lines) * 8
    y_start = CENTER_Y - (total_text_height // 2)

    for i, line in enumerate(lines):
        # Center X based on text length
        x = CENTER_X - (len(line) * 6 // 2) + 1
        thumby.display.drawText(line, x, y_start + (i * 8), 1)


# --- Game Logic ---

# Global State Variables
game_state = STATE_IDLE
current_answer = ""
shake_counter = 0

thumby.display.setFPS(1 / FRAME_DELAY) # Set theoretical max FPS for consistency

def game_loop():
    global game_state, current_answer, shake_counter

    # State IDLE: Waiting for a question/button press
    if game_state == STATE_IDLE:
        if any_button_pressed():
            current_answer = random.choice(ANSWERS)
            game_state = STATE_SHAKE
            shake_counter = 0
        draw_idle()

    # State SHAKE: Running the shake animation
    elif game_state == STATE_SHAKE:
        shake_counter += 1
        if shake_counter >= SHAKE_DURATION_FRAMES:
            game_state = STATE_ANSWER
            shake_counter = 0
        draw_shake(shake_counter)

    # State ANSWER: Displaying the result
    elif game_state == STATE_ANSWER:
        if any_button_pressed():
            game_state = STATE_IDLE
        draw_answer(current_answer)


# --- Main Loop ---

while(1):
    game_loop()
    thumby.display.update()
    time.sleep(FRAME_DELAY)
    