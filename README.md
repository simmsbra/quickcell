# QuickCell
QuickCell is an implementation of the single-player card game FreeCell. It places the focus on the actual strategy of the game by automating tedious moves, requiring minimal input, and providing a highlighting system.

![Screenshot](https://raw.githubusercontent.com/simmsbra/quickcell/master/screenshot.png)

## Features
- *Smart Highlighting*: Cards that are needed to advance will be highlit so one doesn't have to search for them.
- *Minimal Keystrokes*: Moves are 2 to 3 strokes on the numpad, do not require the enter key, and are natural to string together.
- *Extended Automoving*: A more aggressive but still safe-for-play system will automatically move cards to the foundations.
- *Distilled Display*: The game state is represented as simply as possible so as not to interfere with quick play.

## Running
- Linux
  1. Install python3, which comes with curses.
  2. Download the source files.
  3. Run the program.
     - `python3 quickcell.py` to play a random deal
     - `python3 quickcell.py 399677` to play, for example, game 399677 (this can be used to replay deals)
- Windows
  - curses is not supported. One could always use a Linux virtual machine or LiveCD/USB, however.

## Author
This project was created by Brandon Simmons.

## Thanks
Thank you Michael Keller for creating the FreeCell FAQ at:
<http://solitairelaboratory.com/fcfaq.html>
The last question of section 2, about cards automatically moving home, was particularly helpful.
