# Magic 8 Ball for Thumby

A classic Magic 8 Ball fortune teller app for the [Thumby](https://thumby.us/) handheld gaming device.

## Description

This app recreates the iconic Magic 8 Ball experience on your Thumby. Ask a yes/no question in your mind, press any button, and receive one of the 20 authentic Magic 8 Ball answers!

## Features

- **Authentic Answers**: All 20 original Magic 8 Ball phrases
  - 10 Affirmative answers
  - 5 Non-committal answers  
  - 5 Negative answers
- **Responsive Animation**: quick shake when activated, then an immediate text reveal
- **Classic Visuals**: 8-ball sprite displayed at the center of the screen with dithering for low-brightness effects
- **Text Wrapping**: Phrases are automatically wrapped to fit the small screen (max 10 characters per line)
- **Firmware Friendly**: Sprite drawing works on both legacy and current Thumby firmware APIs

## How to Use

1. **Upload the app**: Use the [Thumby Code Editor](https://thumby.us/Code-Editor/) to upload `magic8ball.py` to your Thumby device
2. **Ask a question**: Think of a yes/no question in your mind
3. **Activate**: Press any button or D-pad direction
4. **View answer**: The ball will shake briefly, then the answer text appears instantly
5. **Repeat**: Press any button again to return to the 8-ball and ask another question

## Game Flow

```
┌─────────────────┐
│   8-Ball View   │ <─┐
│  (Press button) │   │
└────────┬────────┘   │
         │            │
         v            │
┌─────────────────┐   │
│ Shake Animation │   │
│   (20 frames)   │   │
└────────┬────────┘   │
         │            │
         v            │
┌─────────────────┐
│ Show Answer     │   │
│ (wait press)    │───┘
└─────────────────┘
```

## Technical Details

- **Platform**: Thumby (RP2040, 72×40 monochrome OLED)
- **Language**: MicroPython
- **Display**: 72×40 pixels monochrome
- **Controls**: All 6 buttons supported (D-pad: Up/Down/Left/Right, Action: A/B)
- **Frame Rate**: ~20 FPS target (throttled by `time.sleep(0.05)`)

## The 20 Authentic Magic 8 Ball Answers

### Affirmative (10)
1. It is certain
2. It is decidedly so
3. Without a doubt
4. Yes definitely
5. You may rely on it
6. As I see it yes
7. Most likely
8. Outlook good
9. Yes
10. Signs point to yes

### Non-Committal (5)
11. Reply hazy try again
12. Ask again later
13. Better not tell you now
14. Cannot predict now
15. Concentrate and ask again

### Negative (5)
16. Don't count on it
17. My reply is no
18. My sources say no
19. Outlook not so good
20. Very doubtful

## License

See LICENSE file for details.
