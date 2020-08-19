# [Knights](#knights)

Write a program to solve logic puzzles.

<a data-id="" id="when-to-do-it" style="top: 0px;"></a>

## [When to Do It](#when-to-do-it)

By <span data-local="2020-12-31T23:59:00-05:00" data-boundary="window" data-toggle="tooltip" data-trigger="focus" title="" data-original-title="Thursday, December 31, 2020, 11:59 PM Eastern Standard Time" class="text-nowrap" tabindex="0">Thu, Dec 31, 2020, 11:59 PM EST</span>.

<a data-id="" id="how-to-get-help" style="top: 0px;"></a>

## [How to Get Help](#how-to-get-help)

1.  Ask questions on Ed!
2.  Ask questions on CS50’s various online fora!

<a data-id="" id="background" style="top: 0px;"></a>

## [Background](#background)

In 1978, logician Raymond Smullyan published “What is the name of this book?”, a book of logical puzzles. Among the puzzles in the book were a class of puzzles that Smullyan called “Knights and Knaves” puzzles.

In a Knights and Knaves puzzle, the following information is given: Each character is either a knight or a knave. A knight will always tell the truth: if knight states a sentence, then that sentence is true. Conversely, a knave will always lie: if a knave states a sentence, then that sentence is false.

The objective of the puzzle is, given a set of sentences spoken by each of the characters, determine, for each character, whether that character is a knight or a knave.

For example, consider a simple puzzle with just a single character named A. A says “I am both a knight and a knave.”

Logically, we might reason that if A were a knight, then that sentence would have to be true. But we know that the sentence cannot possibly be true, because A cannot be both a knight and a knave – we know that each character is either a knight or a knave, but not both. So, we could conclude, A must be a knave.

That puzzle was on the simpler side. With more characters and more sentences, the puzzles can get trickier! Your task in this problem is to determine how to represent these puzzles using propositional logic, such that an AI running a model-checking algorithm could solve these puzzles for us.

<a data-id="" id="getting-started" style="top: 0px;"></a>

## [Getting Started](#getting-started)

- <span class="fa-li"></span>Download the distribution code from [https://cdn.cs50.net/ai/2020/x/projects/1/knights.zip](https://cdn.cs50.net/ai/2020/x/projects/1/knights.zip) and unzip it.

<a data-id="" id="understanding" style="top: 0px;"></a>

## [Understanding](#understanding)

Take a look at `logic.py`, which you may recall from Lecture 1\. No need to understand everything in this file, but notice that this file defines several classes for different types of logical connectives. These classes can be composed within each other, so an expression like `And(Not(A), Or(B, C))` represents the logical sentence stating that symbol `A` is not true, and that symbol `B` or symbol `C` is true (where “or” here refers to inclusive, not exclusive, or).

Recall that `logic.py` also contains a function `model_check`. `model_check` takes a knowledge base and a query. The knowledge base is a single logical sentence: if multiple logical sentences are known, they can be joined together in an `And` expression. `model_check` recursively considers all possible models, and returns `True` if the knowledge base entails the query, and returns `False` otherwise.

Now, take a look at `puzzle.py`. At the top, we’ve defined six propositional symbols. `AKnight`, for example, represents the sentence that “A is a knight,” while `AKnave` represents the sentence that “A is a knave.” We’ve similarly defined propositional symbols for characters B and C as well.

What follows are four different knowledge bases, `knowledge0`, `knowledge1`, `knowledge2`, and `knowledge3`, which will contain the knowledge needed to deduce the solutions to the upcoming Puzzles 0, 1, 2, and 3, respectively. Notice that, for now, each of these knowledge bases is empty. That’s where you come in!

The `main` function of this `puzzle.py` loops over all puzzles, and uses model checking to compute, given the knowledge for that puzzle, whether each character is a knight or a knave, printing out any conclusions that the model checking algorithm is able to make.

<a data-id="" id="specification" style="top: 0px;"></a>

## [Specification](#specification)

<div class="alert alert-warning" data-alert="warning" role="alert">

Beginning **1 July 2020**, an automated tool will begin assisting the staff in enforcing the constraints in the below specification. Your submission will fail if any of these are not handled properly or if you modify functions other than as permitted.

</div>

Add knowledge to knowledge bases `knowledge0`, `knowledge1`, `knowledge2`, and `knowledge3` to solve the following puzzles.

- <span class="fa-li"></span>Puzzle 0 is the puzzle from the Background. It contains a single character, A.
  - <span class="fa-li"></span>A says “I am both a knight and a knave.”
- <span class="fa-li"></span>Puzzle 1 has two characters: A and B.
  - <span class="fa-li"></span>A says “We are both knaves.”
  - <span class="fa-li"></span>B says nothing.
- <span class="fa-li"></span>Puzzle 2 has two characters: A and B.
  - <span class="fa-li"></span>A says “We are the same kind.”
  - <span class="fa-li"></span>B says “We are of different kinds.”
- <span class="fa-li"></span>Puzzle 3 has three characters: A, B, and C.
  - <span class="fa-li"></span>A says either “I am a knight.” or “I am a knave.”, but you don’t know which.
  - <span class="fa-li"></span>B says “A said ‘I am a knave.’”
  - <span class="fa-li"></span>B then says “C is a knave.”
  - <span class="fa-li"></span>C says “A is a knight.”

In each of the above puzzles, each character is either a knight or a knave. Every sentence spoken by a knight is true, and every sentence spoken by a knave is false.

Once you’ve completed the knowledge base for a problem, you should be able to run `python puzzle.py` to see the solution to the puzzle.

<a data-id="" id="hints" style="top: 0px;"></a>

## [Hints](#hints)

- <span class="fa-li"></span>For each knowledge base, you’ll likely want to encode two different types of information: (1) information about the structure of the problem itself (i.e., information given in the definition of a Knight and Knave puzzle), and (2) information about what the characters actually said.
- <span class="fa-li"></span>Consider what it means if a sentence is spoken by a character. Under what conditions is that sentence true? Under what conditions is that sentence false? How can you express that as a logical sentence?
- <span class="fa-li"></span>There are multiple possible knowledge bases for each puzzle that will compute the correct result. You should attempt to choose a knowledge base that offers the most direct translation of the information in the puzzle, rather than performing logical reasoning on your own. You should also consider what the most concise representation of the information in the puzzle would be.
  - <span class="fa-li"></span>For instance, for Puzzle 0, setting `knowledge0 = AKnave` would result in correct output, since through our own reasoning we know A must be a knave. But doing so would be against the spirit of this problem: the goal is to have your AI do the reasoning for you.
- <span class="fa-li"></span>You should not need to (nor should you) modify `logic.py` at all to complete this problem.

<a data-id="" id="how-to-submit" style="top: 0px;"></a>

## [How to Submit](#how-to-submit)

<div class="alert alert-warning" data-alert="warning" role="alert">

Effective **1 July 2020**, your submission must be structured exactly as follows:

You may not have your code in your `ai50/projects/2020/x/knights` branch nested within any further subdirectories (such as a subdirectory called `knights` or `project1a`). That is to say, if the staff attempts to access `https://github.com/me50/USERNAME/blob/ai50/projects/2020/x/knights/puzzle.py`, where `USERNAME` is your GitHub username, that is exactly where your file should live. If your file is not at that location when the staff attempts to grade, your submission will fail.

</div>

1.  Visit [this link](https://submit.cs50.io/invites/8f7fa48876984cda98a73ba53bcf01fd), log in with your GitHub account, and click **Authorize cs50**. Then, check the box indicating that you’d like to grant course staff access to your submissions, and click **Join course**.
2.  [Install Git](https://git-scm.com/downloads) and, optionally, [install `submit50`](https://cs50.readthedocs.io/submit50/).
3.  If you’ve installed `submit50`, execute

    <div class="highlighter-rouge">

    <div class="highlight">

        submit50 ai50/projects/2020/x/knights

    </div>

    </div>

    Otherwise, using Git, push your work to `https://github.com/me50/USERNAME.git`, where `USERNAME` is your GitHub username, on a branch called `ai50/projects/2020/x/knights`.

4.  [Record a 1- to 5-minute screencast](https://www.howtogeek.com/205742/how-to-record-your-windows-mac-linux-android-or-ios-screen/) in which you demonstrate your project’s functionality. Be certain that every element of the specification, above, is demonstrated in your video. There’s no need to show your code, just your application in action; we’ll review your code on GitHub. [Upload that video to YouTube](https://www.youtube.com/upload) (as unlisted or public, but not private) or somewhere else.
5.  Submit [this form](https://forms.cs50.io/8bf31a9b-0bfc-43a9-83d9-b8101b9b3855).

You can then go to [https://cs50.me/cs50ai](https://cs50.me/cs50ai) to view your current progress!