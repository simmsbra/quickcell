# QuickCell
QuickCell is an implementation of the single-player card game FreeCell. QuickCell places the focus on the actual strategy of the game by automating tedious moves, requiring minimal input, and providing a highlighting system.

![Demo](https://raw.githubusercontent.com/simmsbra/quickcell/master/demo.gif)

## Features
- *Smart Highlighting*: Cards that are needed to advance will be highlit for quick spotting.
- *Minimal Keystrokes*: Moves are made with 2 to 3 keystrokes, do not require the enter key, and are easy to string together on a numpad.
- *Extended Automoving*: A more aggressive but still safe-for-play system will automatically move cards to the foundations.
- *Distilled Display*: The game state is presented as simply as possible to keep the focus on quick, strategic play.

## Running
- Linux
  1. Install python3, which comes with the curses library.
  2. Download or clone this repository.
  3. Move to the src/ directory.
  4. Run the program.
     - `python3 quickcell.py` to play a random deal
     - `python3 quickcell.py 399677` to play, for example, game 399677 (this can be used to replay deals)
- Windows
  - curses, a required library, is not present.
  - To play, you can use a Linux LiveCD/USB or virtual machine.
  - (This project may be overhauled to become OS-independent in the future.)

## Author
This project was created by Brandon Simmons.

## Thanks
Thank you Michael Keller for creating the [FreeCell FAQ](http://solitairelaboratory.com/fcfaq.html).
The last question of section 2, about cards automatically moving home, was particularly helpful.

Thank you Dan Fletcher for writing the article [Freecell PowerMoves Explained](http://EzineArticles.com/104608).
The formula for determining the longest movable card sequence is implemented here.
