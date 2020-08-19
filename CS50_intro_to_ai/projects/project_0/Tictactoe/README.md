# [Tic-Tac-Toe](#tic-tac-toe)

Using Minimax, implement an AI to play Tic-Tac-Toe optimally.

![Tic-Tac-Toe Game](./images/game.png)

<a data-id="" id="when-to-do-it" style="top: 0px;"></a>

## [When to Do It](#when-to-do-it)

By <span data-local="2020-12-31T23:59:00-05:00" data-boundary="window" data-toggle="tooltip" data-trigger="focus" title="" data-original-title="Thursday, December 31, 2020, 11:59 PM Eastern Standard Time" class="text-nowrap" tabindex="0">Thu, Dec 31, 2020, 11:59 PM EST</span>.

<a data-id="" id="how-to-get-help" style="top: 0px;"></a>

## [How to Get Help](#how-to-get-help)

1.  Ask questions on Ed!
2.  Ask questions on CS50’s various online fora!

<a data-id="" id="getting-started" style="top: 0px;"></a>

## [Getting Started](#getting-started)

- <span class="fa-li"></span>Download the distribution code from [https://cdn.cs50.net/ai/2020/x/projects/0/tictactoe.zip](https://cdn.cs50.net/ai/2020/x/projects/0/tictactoe.zip) and unzip it.
- <span class="fa-li"></span>Once in the directory for the project, run `pip3 install -r requirements.txt` to install the required Python package (`pygame`) for this project.

<a data-id="" id="understanding" style="top: 0px;"></a>

## [Understanding](#understanding)

There are two main files in this project: `runner.py` and `tictactoe.py`. `tictactoe.py` contains all of the logic for playing the game, and for making optimal moves. `runner.py` has been implemented for you, and contains all of the code to run the graphical interface for the game. Once you’ve completed all the required functions in `tictactoe.py`, you should be able to run `python runner.py` to play against your AI!

Let’s open up `tictactoe.py` to get an understanding for what’s provided. First, we define three variables: `X`, `O`, and `EMPTY`, to represent possible moves of the board.

The function `initial_state` returns the starting state of the board. For this problem, we’ve chosen to represent the board as a list of three lists (representing the three rows of the board), where each internal list contains three values that are either `X`, `O`, or `EMPTY`. What follows are functions that we’ve left up to you to implement!

<a data-id="" id="specification" style="top: 0px;"></a>

## [Specification](#specification)

<div class="alert alert-warning" data-alert="warning" role="alert">

Beginning **1 July 2020**, an automated tool will begin assisting the staff in enforcing the constraints in the below specification. Your submission will fail if any of these are not handled properly or if you modify functions other than as permitted.

</div>

Complete the implementations of `player`, `actions`, `result`, `winner`, `terminal`, `utility`, and `minimax`.

- <span class="fa-li"></span>The `player` function should take a `board` state as input, and return which player’s turn it is (either `X` or `O`).
  - <span class="fa-li"></span>In the initial game state, `X` gets the first move. Subsequently, the player alternates with each additional move.
  - <span class="fa-li"></span>Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
- <span class="fa-li"></span>The `actions` function should return a `set` of all of the possible actions that can be taken on a given board.
  - <span class="fa-li"></span>Each action should be represented as a tuple `(i, j)` where `i` corresponds to the row of the move (`0`, `1`, or `2`) and `j` corresponds to which cell in the row corresponds to the move (also `0`, `1`, or `2`).
  - <span class="fa-li"></span>Possible moves are any cells on the board that do not already have an `X` or an `O` in them.
  - <span class="fa-li"></span>Any return value is acceptable if a terminal board is provided as input.
- <span class="fa-li"></span>The `result` function takes a `board` and an `action` as input, and should return a new board state, without modifying the original board.
  - <span class="fa-li"></span>If `action` is not a valid action for the board, your program should [raise an exception](https://docs.python.org/3/tutorial/errors.html#raising-exceptions).
  - <span class="fa-li"></span>The returned board state should be the board that would result from taking the original input board, and letting the player whose turn it is make their move at the cell indicated by the input action.
  - <span class="fa-li"></span>Importantly, the original board should be left unmodified: since Minimax will ultimately require considering many different board states during its computation. This means that simply updating a cell in `board` itself is not a correct implementation of the `result` function. You’ll likely want to make a [deep copy](https://docs.python.org/3/library/copy.html#copy.deepcopy) of the board first before making any changes.
- <span class="fa-li"></span>The `winner` function should accept a `board` as input, and return the winner of the board if there is one.
  - <span class="fa-li"></span>If the X player has won the game, your function should return `X`. If the O player has won the game, your function should return `O`.
  - <span class="fa-li"></span>One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
  - <span class="fa-li"></span>You may assume that there will be at most one winner (that is, no board will ever have both players with three-in-a-row, since that would be an invalid board state).
  - <span class="fa-li"></span>If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the function should return `None`.
- <span class="fa-li"></span>The `terminal` function should accept a `board` as input, and return a boolean value indicating whether the game is over.
  - <span class="fa-li"></span>If the game is over, either because someone has won the game or because all cells have been filled without anyone winning, the function should return `True`.
  - <span class="fa-li"></span>Otherwise, the function should return `False` if the game is still in progress.
- <span class="fa-li"></span>The `utility` function should accept a terminal `board` as input and output the utility of the board.
  - <span class="fa-li"></span>If X has won the game, the utility is `1`. If O has won the game, the utility is `-1`. If the game has ended in a tie, the utility is `0`.
  - <span class="fa-li"></span>You may assume `utility` will only be called on a `board` if `terminal(board)` is `True`.
- <span class="fa-li"></span>The `minimax` function should take a `board` as input, and return the optimal move for the player to move on that board.
  - <span class="fa-li"></span>The move returned should be the optimal action `(i, j)` that is one of the allowable actions on the board. If multiple moves are equally optimal, any of those moves is acceptable.
  - <span class="fa-li"></span>If the `board` is a terminal board, the `minimax` function should return `None`.

For all functions that accept a `board` as input, you may assume that it is a valid board (namely, that it is a list that contains three rows, each with three values of either `X`, `O`, or `EMPTY`). You should not modify the function declarations (the order or number of arguments to each function) provided.

Once all functions are implemented correctly, you should be able to run `python runner.py` and play against your AI. And, since Tic-Tac-Toe is a tie given optimal play by both sides, you should never be able to beat the AI (though if you don’t play optimally as well, it may beat you!)

<a data-id="" id="hints" style="top: 0px;"></a>

## [Hints](#hints)

- <span class="fa-li"></span>If you’d like to test your functions in a different Python file, you can import them with lines like `from tictactoe import initial_state`.
- <span class="fa-li"></span>You’re welcome to add additional helper functions to `tictactoe.py`, provided that their names do not collide with function or variable names already in the module.
- <span class="fa-li"></span>Alpha-beta pruning is optional, but may make your AI run more efficiently!

<a data-id="" id="how-to-submit" style="top: 0px;"></a>

## [How to Submit](#how-to-submit)

<div class="alert alert-warning" data-alert="warning" role="alert">

Effective **1 July 2020**, your submission must be structured exactly as follows:

You may not have your code in your `ai50/projects/2020/x/tictactoe` branch nested within any further subdirectories (such as a subdirectory called `tictactoe` or `project0b`). That is to say, if the staff attempts to access `https://github.com/me50/USERNAME/blob/ai50/projects/2020/x/tictactoe/tictactoe.py`, where `USERNAME` is your GitHub username, that is exactly where your file should live. If your file is not at that location when the staff attempts to grade, your submission will fail.

</div>

1.  Visit [this link](https://submit.cs50.io/invites/8f7fa48876984cda98a73ba53bcf01fd), log in with your GitHub account, and click **Authorize cs50**. Then, check the box indicating that you’d like to grant course staff access to your submissions, and click **Join course**.
2.  [Install Git](https://git-scm.com/downloads) and, optionally, [install `submit50`](https://cs50.readthedocs.io/submit50/).
3.  If you’ve installed `submit50`, execute

    <div class="highlighter-rouge">

    <div class="highlight">

        submit50 ai50/projects/2020/x/tictactoe

    </div>

    </div>

    Otherwise, using Git, push your work to `https://github.com/me50/USERNAME.git`, where `USERNAME` is your GitHub username, on a branch called `ai50/projects/2020/x/tictactoe`.

4.  [Record a 1- to 5-minute screencast](https://www.howtogeek.com/205742/how-to-record-your-windows-mac-linux-android-or-ios-screen/) in which you demonstrate your project’s functionality. Be certain that every element of the specification, above, is demonstrated in your video. There’s no need to show your code, just your application in action; we’ll review your code on GitHub. [Upload that video to YouTube](https://www.youtube.com/upload) (as unlisted or public, but not private) or somewhere else.
    - <span class="fa-li"></span>**VIDEO NOTE**: Your video should show at least one game where the AI plays X and at least one game where the AI plays O.
    - <span class="fa-li"></span>To aid in the staff’s review, in your video’s description on YouTube, you should timestamp where each of the following occurs. **THIS IS NOT OPTIONAL**. Failure to do this will result in your submission being rejected:
      - <span class="fa-li"></span>Game(s) where AI plays X (and you must state the result of those game(s))
      - <span class="fa-li"></span>Game(s) where AI plays O (and you must state the result of those game(s))
    - <span class="fa-li"></span>As an example, your timestamps should follow this format (two examples below):
      - <span class="fa-li"></span>0:08 - AI plays X (tie)
      - <span class="fa-li"></span>0:44 - AI plays O (AI wins)
5.  Submit [this form](https://forms.cs50.io/655c8eda-7148-4432-b22d-4090c71f7923).

You can then go to [https://cs50.me/cs50ai](https://cs50.me/cs50ai) to view your current progress!
