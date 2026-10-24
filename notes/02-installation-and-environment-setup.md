# Chapter 02 — Installation and Environment Setup

> Part 1 — Python Fundamentals · Video: 14:22–29:18 · Previous: [01 Introduction to Programming and Python](01-introduction-to-programming-and-python.md) · Next: [03 Built-in Functions, print() and Modules](03-builtin-functions-print-and-modules.md)

**In this chapter:** how to install Python on Windows, macOS and Linux, how to check that the installation works, three ways to run code (the interactive terminal, script files, and IDLE), what Anaconda and Jupyter Notebook are and when to choose them, and a first look at virtual environments, which keep each project's packages separate.

**Before you start:** you only need the ideas from [Chapter 01](01-introduction-to-programming-and-python.md#what-is-python-and-where-is-it-used): Python is an interpreted language, so a program called the interpreter reads your code and runs it. A terminal (also called a command prompt or shell) is a text window where you type commands. Commands in this chapter are shown in `bash` blocks. Windows users can use the same commands in PowerShell or Command Prompt unless the text says otherwise. Examples were run with Python 3.13 on Linux. Installer screens, menu names and download pages change over time, so this chapter describes what to achieve and which commands to use, and it links to the official instructions rather than describing every screen.

---

## Installing Python

**Timestamp:** [14:22](https://www.youtube.com/watch?v=J9BI0jGOds8&t=862s)

**Learning objectives:**

- Explain what you are installing (the interpreter and the standard library) and what Python 2 versus Python 3 means today.
- Install Python 3 on your operating system and verify the installation from a terminal.
- Explain what `PATH` is and why a wrong `PATH` causes "command not found" errors.

**1. Intuition**

Writing Python code is like writing a recipe in a language the kitchen understands. The interpreter is the cook who reads the recipe and performs each step. If no cook is installed on your computer, your recipe is only text. Installing Python means putting the cook, plus a standard pantry of ready-made tools (the standard library), on your machine.

**2. Why does it exist?**

Operating systems do not run Python source code on their own. You need a program that understands the language. Several versions exist side by side, and your operating system may already contain one for its own tools. A deliberate installation gives you a known, current version that you control.

**3. Technical explanation**

An installation of Python contains:

- the interpreter, an executable named `python` or `python3`, which reads source code and runs it;
- the standard library, a large collection of modules such as `math`, `os` and `json` (you will meet `math` in [Python Modules: math and import](03-builtin-functions-print-and-modules.md#python-modules-math-and-import));
- `pip`, the tool that downloads and installs extra packages;
- often `venv`, a module for creating virtual environments (covered later in this chapter), and IDLE, a small editor (see [Running Python in the Terminal and IDLE](#running-python-in-the-terminal-and-idle)).

Python 2 and Python 3 are different, partly incompatible versions of the language. Python 2 reached its official end of life on 1 January 2020. This handbook uses Python 3 only. When you see old tutorials that use `print "text"` without brackets, they were written for Python 2.

Python 3 releases are numbered `3.minor.patch`, for example `3.13.1`. A new minor version (3.12, 3.13, ...) is released about once a year and adds features. If a feature in this handbook needs a particular minor version, the text says so. The official download page is [python.org/downloads](https://www.python.org/downloads/), and the official setup guide is in the [Python documentation](https://docs.python.org/3/using/index.html).

The `PATH` is a list of folders that your terminal searches when you type a command. When you type `python`, the terminal looks through the folders in `PATH` for an executable with that name. If the folder that contains Python is not on the `PATH`, you get an error such as "command not found" even though Python is installed.

**4. Syntax**

There is no Python syntax here yet; the "syntax" is the set of terminal commands that check your installation.

```bash
python --version     # Windows and some systems
python3 --version    # macOS and most Linux systems
py --version         # Windows "py launcher"
```

- `python`, `python3` or `py` is the command that starts the interpreter.
- `--version` is an option (a flag) that asks the program to print its version and exit.
- Text after `#` is a comment for the reader; the terminal ignores it.

**5. Example 1 — Basic**

Installing, step by step. These are the usual routes. Follow the official page for the current details.

*Windows.* Download the installer from [python.org/downloads](https://www.python.org/downloads/) and run it. The installer offers an option to add Python to `PATH`; tick it. After installing, open a new terminal window and run:

```bash
python --version
```

On Windows the installer usually also installs the `py` launcher, a small program that finds installed Pythons for you. `py --version` and `py -3.13 --version` (to ask for a specific minor version) are common.

*macOS.* Download the macOS installer from the same page and run it, or use a package manager such as Homebrew if you already use one. Then run:

```bash
python3 --version
```

*Linux.* Most distributions include Python 3 already. Check first:

```bash
python3 --version
```

If it is missing or too old, install it with your distribution's package manager (for example `sudo apt install python3 python3-venv python3-pip` on Debian or Ubuntu). On some distributions IDLE and `venv` are separate packages, so they may need their own install command.

Expected output (the numbers depend on what you installed):

```text
Python 3.13.16
```

If you see a version that starts with `Python 3.`, the installation works. A version that starts with `Python 2.` means the command you typed points to the old interpreter; try `python3` instead.

**6. Example 2 — Practical**

Checking exactly which interpreter you are using matters when several are installed. Ask Python itself:

```python
import sys

print(sys.version_info[:2])
```

Line by line:

- `import sys` loads the standard-library module `sys`, which exposes details about the running interpreter.
- `sys.version_info` is a named tuple with the version numbers. Slicing with `[:2]` keeps the first two items: major and minor. (Tuples and slicing are covered in [Tuples](21-tuples.md#tuples) and [String Slicing](07-string-slicing.md#string-slicing).)

Output with Python 3.13:

```text
(3, 13)
```

You can also print the path of the running interpreter with `print(sys.executable)`. The path is different on every machine, so no output is shown here. If it points to a folder you did not expect, you have more than one Python installed.

**7. Example 3 — Edge case or common mistake**

The most common installation problem is a `PATH` error. On Windows it looks like this (the exact wording differs between Command Prompt and PowerShell):

```text
'python' is not recognized as an internal or external command,
operable program or batch file.
```

On macOS and Linux the message is usually `command not found: python`.

There are two different causes and two different fixes:

1. Python is installed but its folder is not on `PATH`. Fix: re-run the installer and tick the option that adds Python to `PATH`, or add the folder to `PATH` by hand. Open a new terminal afterwards, because an already open terminal keeps the old `PATH`.
2. The command name is different on your system. On macOS and many Linux systems the command is `python3`, and plain `python` may not exist. Fix: use `python3`. On Windows try `py`.

**8. Common mistakes**

- Installing but never opening a new terminal. An open terminal does not see a changed `PATH`. Close it and open another.
- Typing `python` and getting Python 2 on an old machine. Always check with `--version` and use `python3` where needed.
- Confusing the terminal with the Python prompt. If your prompt shows `>>>`, you are inside Python and typing `python --version` there is an error. You type that at the terminal prompt instead (see the next section).
- Downloading Python from an unofficial site. Use python.org or your operating system's package manager.
- Installing packages for the wrong Python. If `pip install` seems to work but `import` fails, `pip` and `python` may belong to different installations. Use `python -m pip install ...` (shown later) to be sure they match.

**9. Real-world and AI applications**

Professional projects state which Python version they need, because libraries are tested against specific versions. Teams pin the version in a project file or in a Docker image so everyone runs the same interpreter. AI libraries are particularly sensitive to this: deep-learning packages publish builds only for certain Python versions, and a mismatch is a common cause of "no matching distribution found" errors when installing them. Checking `python --version` first saves time.

**10. Practice**

1. Open a terminal and print your Python version. Which minor version do you have?
2. Write a two-line Python program that prints the major and minor version using `sys.version_info`. Run it from a file.
3. A teammate says `python --version` prints `Python 2.7.18` while `python3 --version` prints `Python 3.12.3`. Explain what is happening and what command they should use for this course.
4. After installing Python on Windows, `python --version` still says the command is not recognized, but the installer reported success. List two things to try, in order.

**11. Interview questions**

- *What is the difference between Python 2 and Python 3, and which should new code use?* Python 3. Python 2 reached end of life on 1 January 2020 and is not maintained.
- *What does `PATH` do?* It is a list of folders the shell searches to find an executable when you type a command name.
- *What is `pip`?* The standard tool for installing Python packages from the Python Package Index (PyPI).

**12. Quick revision**

- Installing Python installs the interpreter, standard library and `pip`.
- This handbook uses Python 3.
- Check with `python --version`, `python3 --version` or `py --version`.
- "Command not found" usually means a `PATH` or command-name problem, not a broken install.
- Open a new terminal after changing the `PATH`.

---

## Running Python in the Terminal and IDLE

**Timestamp:** [16:18](https://www.youtube.com/watch?v=J9BI0jGOds8&t=978s)

**Learning objectives:**

- Start the interactive prompt (the REPL), run expressions, and leave it correctly.
- Save code in a `.py` file and run it from the terminal, including a one-line command with `-c`.
- Describe when to use the REPL, script files and IDLE.

**1. Intuition**

There are two basic ways to talk to Python. The first is a conversation: you type one line, Python answers at once. The second is a letter: you write many lines in a file, hand the file over, and Python carries out all of it. The conversation is great for trying ideas. The letter is how real programs are saved and shared.

**2. Why does it exist?**

Beginners need quick feedback ("what does this do?") and programmers need repeatable programs ("run the same steps tomorrow"). Python supports both with the same interpreter.

**3. Technical explanation**

The interactive mode is called a REPL, short for Read-Eval-Print Loop. It reads a line you type, evaluates it, prints the result, and loops to wait for the next line. The default prompt is `>>>`. If you start a block that continues on more lines (such as an `if` statement), the prompt changes to `...` until the block ends.

In the REPL, if you type an expression, Python prints its value automatically. In a script file nothing is printed unless you call `print()`. This difference surprises many beginners: the line `2 + 3` shows `5` in the REPL but shows nothing when it is a line in a file.

A script is a plain text file, by convention ending in `.py`. Running `python hello.py` starts the interpreter, which reads the whole file from top to bottom and executes each statement in order, then exits.

IDLE (Integrated Development and Learning Environment) is a simple editor and REPL window that comes with many Python installs. It highlights syntax, lets you type a file and run it with a keystroke, and shows output in a separate window. It is small and useful for learning; most professionals later move to a full editor such as VS Code or PyCharm, but nothing in this handbook requires a specific editor.

**4. Syntax**

```bash
python                 # start the REPL (use python3 or py on some systems)
python script.py       # run a file
python -c "code"       # run a short piece of code given on the command line
python -m module       # run a module as a program (for example: python -m venv .venv)
```

- `script.py` is the path to a file. If the file is in another folder, give the folder path too.
- `-c` takes the next argument as Python source text.
- `-m` runs a module by name, searching the places Python normally imports from.

To leave the REPL, call `exit()` or press Ctrl+D on macOS and Linux, or Ctrl+Z and then Enter on Windows.

**5. Example 1 — Basic**

An interactive session. Lines starting with `>>>` are what you type; the other lines are Python's answers. (This is an interactive transcript, so it shows how the REPL behaves; it is not a script.)

```text
>>> 2 + 3
5
>>> name = "Asha"
>>> name.upper()
'ASHA'
>>> print("hi")
hi
>>> len(name)
4
>>> exit()
```

Notice the difference between `name.upper()` and `print("hi")`. The first is an expression, so the REPL shows its value, with quotes, because it displays the value's representation (called `repr`). The second calls `print()`, which writes the text without quotes and returns nothing to display.

A related convenience: in the REPL, the variable `_` holds the value of the last expression that was displayed, so after `2 + 3` you can type `_ * 10` to get `50`. This works only in the interactive REPL, not in script files.

**6. Example 2 — Practical**

Save this text in a file named `hello.py`:

```python
name = "Asha"
print("Hello,", name)
print(2 + 3)
```

Run it from the terminal, in the folder that contains the file:

```bash
python hello.py
```

Output:

```text
Hello, Asha
5
```

Line by line:

- `name = "Asha"` creates a variable called `name` that refers to the string `"Asha"`.
- `print("Hello,", name)` prints the two items separated by a space (you will study `print()` in [Built-in Functions and print()](03-builtin-functions-print-and-modules.md#built-in-functions-and-print)).
- `print(2 + 3)` prints `5`. Without `print`, the expression `2 + 3` would compute a value and discard it silently.

For a very short test you can skip the file:

```bash
python -c "print('inline', 6 * 7)"
```

```text
inline 42
```

To use IDLE, start it from your applications menu, or from a terminal with `python -m idlelib` (on Linux it may need a separate package such as `python3-idle`). Choose File, then New File, type the code, save with a `.py` name, and choose Run, then Run Module (the shortcut is F5). Output appears in the shell window.

**7. Example 3 — Edge case or common mistake**

Typing a shell command inside the REPL, or Python code in the terminal, produces confusing errors. The line below is a terminal command. Python can read it as an arithmetic expression (the name `python`, minus the negated name `version`), so it is valid syntax, but it fails when run because no such names exist:

```python
python --version
```

Inside the Python REPL, or as a line in a script, it gives:

```text
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    python --version
NameError: name 'python' is not defined
```

Python found nothing called `python` to subtract from. The lesson: terminal commands go at the terminal prompt, and Python code goes at the `>>>` prompt or in a file.

Three situations look similar. If the first character of the prompt is `>>>`, you are in Python; type Python code. If you see your folder name and a `$` or `>`, you are at the terminal; type terminal commands such as `python hello.py`. If you run `python hello.py` and the terminal says it cannot find the file, you are in a different folder than the file; check with `ls` (macOS and Linux) or `dir` (Windows), and use `cd folder_name` to move.

**8. Common mistakes**

- Expecting a bare expression in a file to display a value. Use `print()` in scripts.
- Saving the file as `hello.py.txt` because the operating system hides extensions. Turn on "show file extensions" and check the name.
- Naming your own file after a standard module (for example `math.py` or `random.py`). Python may import your file instead of the real module and cause strange errors. Pick a different name.
- Running the script from the wrong folder, so the file is not found.
- Indenting code inconsistently when pasting into the REPL. Blocks must be indented the same way everywhere.

**9. Real-world and AI applications**

Developers use the REPL to test a function or inspect an object in seconds. Data and AI work often starts in a REPL-like environment (the next section) because you can load data once and keep experimenting. Production programs and training scripts are files: they are run with `python train.py` or `python -m package.module`, often from automated systems, so they must produce the same results every time without a person typing.

**10. Practice**

1. In the REPL, compute `7 * 8` and then use `_` to double the result. Note which key sequence you used to exit.
2. Write a file `greet.py` that stores your name in a variable and prints a greeting with `print()`. Run it.
3. Use `python -c` to print the result of `10 / 4`. What does the output tell you about the `/` operator?
4. A file contains the single line `3 * 3`. You run it with `python file.py` and see nothing. Explain why and fix it.

**11. Interview questions**

- *What does REPL stand for, and how does it differ from running a script?* Read-Eval-Print Loop. It evaluates one statement at a time and echoes expression values, while a script is run as a whole and prints only what you ask it to.
- *What does `python -m` do?* It runs a module as a program by name instead of by file path.
- *Why might `import random` break after you create a file `random.py` in your project?* Your file shadows the standard module because the current folder is searched first.

**12. Quick revision**

- REPL: type a line, see the answer; good for experiments; prompt `>>>`.
- Script: a `.py` file run with `python file.py`; needs `print()` to show values.
- `python -c` runs a short snippet; `python -m` runs a module.
- IDLE is a simple bundled editor; any editor works.
- Do not name your files after standard modules.

---

## Anaconda and Jupyter Notebook Setup

**Timestamp:** [20:31](https://www.youtube.com/watch?v=J9BI0jGOds8&t=1231s)

**Learning objectives:**

- Explain what Anaconda, conda, and Jupyter Notebook are and how each differs from plain Python with `pip`.
- Start a notebook and run code cells.
- Create and activate an isolated environment with `venv` (and know the `conda` equivalent).

**1. Intuition**

Plain Python is like a kitchen with basic tools. Anaconda is a ready-made catering kit: the kitchen plus many pre-packed data-science tools, delivered together with a manager that can set up separate workstations. Jupyter Notebook is a lab notebook: you write a bit of code in a box (a cell), run it, and see the result right below, mixed with your written notes.

**2. Why does it exist?**

Two real problems led to these tools.

1. Data and AI work needs many scientific packages whose installation was once painful. Anaconda bundles and manages them.
2. Exploratory work is a back-and-forth: load data, look at it, change a step, look again. Re-running a whole script each time is slow. A notebook keeps state in memory between cells and displays tables and charts inline.

A third problem is shared by all Python work: different projects need different versions of packages, and installing everything into one place makes projects interfere with each other. That is solved by virtual environments.

**3. Technical explanation**

- **Anaconda** is a distribution: Python plus a large set of preinstalled data-science packages plus the `conda` package and environment manager. Miniconda is a smaller installer with only `conda` and Python. The Anaconda distribution has its own licensing terms for some commercial uses, so check the current terms on the Anaconda website if you use it at work.
- **conda** installs packages and creates environments, and it can manage non-Python dependencies as well. `pip` installs Python packages from PyPI. Many people use both; the safest habit is to use only one tool per environment where possible.
- **Jupyter Notebook** is a web-based application that runs in your browser while a Python process (the kernel) runs in the background. A notebook file has the extension `.ipynb` and stores both your cells and their last outputs. It is a separate package. It is not part of the plain Python installation; you install it with `pip install notebook` (or get it with Anaconda). JupyterLab is a newer interface from the same project.
- A cell is either code or Markdown text. Running a code cell sends its code to the kernel. The kernel keeps variables alive between cells, so the order in which you run cells matters, not only the order they appear on the page.
- A **virtual environment** is a folder that contains its own copy of (or link to) the interpreter and its own place for installed packages. Activating it makes `python` and `pip` in your terminal use that folder. The standard-library module for this is `venv`.

**4. Syntax**

Create, activate, use and leave a virtual environment:

```bash
python -m venv .venv                 # create an environment in the folder .venv
source .venv/bin/activate            # activate (macOS and Linux)
.venv\Scripts\activate               # activate (Windows Command Prompt or PowerShell)
python -m pip install notebook       # install a package into this environment
jupyter notebook                     # start Jupyter Notebook
deactivate                           # leave the environment
```

Components:

- `python -m venv .venv` runs the `venv` module and names the new folder `.venv`. The leading dot is only a convention that keeps the folder tidy.
- Activation changes your terminal so that `python` and `pip` refer to the environment. Your prompt usually shows the environment name in brackets.
- `python -m pip install ...` runs `pip` as a module of the interpreter you named, which guarantees that the package lands in the same environment as that `python`.
- `deactivate` restores your normal terminal settings.

The `conda` equivalents:

```bash
conda create -n handbook python=3.13   # create an environment named handbook
conda activate handbook                # activate it
conda install notebook                 # install a package
conda deactivate                       # leave it
```

**5. Example 1 — Basic**

Start Jupyter and run two cells.

1. Activate an environment that has Jupyter installed and run `jupyter notebook` in a terminal. Your browser opens a page that lists the files in your current folder. If the browser does not open, the terminal prints a local address (it starts with `http://localhost`) that you can paste into a browser.
2. Create a new notebook and choose a Python kernel.
3. In the first cell, type:

```python
message = "notebook works"
print(message)
```

4. Press Shift+Enter to run the cell. Below it you see:

```text
notebook works
```

5. In a second cell type just `len(message)` and run it. A notebook shows the value of the last expression in a cell, as the REPL does, so the output is:

```text
14
```

**6. Example 2 — Practical**

Creating an environment for this handbook, and proving that it is isolated. This runs the same commands you would type. The check uses `sys.prefix`, which is the folder where the active environment lives, and `sys.base_prefix`, which is the folder of the base installation; they differ inside a virtual environment.

```bash
python3 -m venv demo-env
demo-env/bin/python -c "import sys; print(sys.prefix != sys.base_prefix)"
python3 -c "import sys; print(sys.prefix != sys.base_prefix)"
```

Output (verified with Python 3.13 on Linux):

```text
True
False
```

Line by line:

- The first command creates the environment folder `demo-env`.
- The second calls the environment's own interpreter directly, without activating anything. It prints `True` because its `sys.prefix` is different from the base installation.
- The third uses the normal interpreter and prints `False`, because it is not inside a virtual environment.

On Windows the environment's interpreter is at `demo-env\Scripts\python.exe` instead of `demo-env/bin/python`. Inside the folder you will find a configuration file named `pyvenv.cfg` and scripts named `activate`; you never edit these.

A good project habit: create one environment per project, put a `.venv` folder in it, and add `.venv/` to `.gitignore` so that it is never committed to Git. This repository's `.gitignore` already does that.

**7. Example 3 — Edge case or common mistake**

A frequent confusion: installing a package into one Python and then importing it from another. Suppose you installed Jupyter in an environment but ran the notebook from a terminal where it was not activated. The result is typically:

```text
jupyter: command not found
```

or, inside a notebook, an import that works in one place and fails in another:

```text
ModuleNotFoundError: No module named 'something'
```

The fix is to check which interpreter you are really using and install into that one:

```python
import sys

print(sys.executable)
```

The printed path tells you which interpreter is running (it differs on every machine, so no output is shown). In a notebook cell, run this to see which environment the kernel uses. Then, in a terminal where the right environment is active, run `python -m pip install <package>`.

Another subtle trap is cell order. If you run cell 3 before cell 2 and cell 3 uses a variable defined in cell 2, you get a `NameError`. Restarting the kernel and running all cells from top to bottom is the reliable way to check that a notebook works from scratch.

**8. Common mistakes**

- Using `pip` instead of `python -m pip`, then installing into a different Python than you expected.
- Mixing `conda install` and `pip install` carelessly in the same environment, which can leave it inconsistent.
- Forgetting to activate the environment before running `pip` or `jupyter`.
- Committing the `.venv` folder or large notebooks with outputs to Git. Ignore the folder and clear outputs when sharing.
- Trusting a notebook that was run out of order. Restart and run all before relying on results.
- Assuming Jupyter is installed with Python. It is a separate install.

**9. Real-world and AI applications**

Notebooks are the standard place for exploring data, prototyping models, plotting training curves and explaining results to others. Many cloud services offer hosted notebooks. Once an idea works, the code is usually moved into `.py` files, tested and run as scripts or services. Virtual environments appear in almost every professional Python project: each AI project pins the exact package versions it was developed with, so that results can be reproduced and one project's upgrade does not break another.

**10. Practice**

1. Create a virtual environment named `.venv`, activate it, run `python -c "import sys; print(sys.prefix)"`, deactivate it, and run the same command again. Compare the two outputs.
2. Install Jupyter (`python -m pip install notebook`) in your environment, start it, create a notebook, and run a cell that prints your Python version using `sys.version_info`.
3. In a notebook, define `x = 5` in cell 1, then delete that cell and run `print(x)` in another cell. Does it still work? Explain why, and how restarting the kernel changes the result.
4. Write down, for each of these, whether it is part of plain Python, part of Anaconda, or a separate install: `venv`, `pip`, `conda`, Jupyter Notebook.

**11. Interview questions**

- *What problem do virtual environments solve?* They isolate each project's installed packages and versions so projects do not conflict.
- *How is conda different from pip?* `pip` installs Python packages from PyPI. `conda` is a package and environment manager that can also install non-Python dependencies and manages whole environments.
- *Why can a notebook give different results from the same code in a script?* Notebook cells keep shared state and can be run out of order, so hidden state from earlier cells can change results.

**12. Quick revision**

- Anaconda = Python + many packages + `conda`; Jupyter is a separate package (also bundled with Anaconda).
- Notebooks run code in cells against a live kernel; order of execution matters.
- Use `python -m venv .venv`, activate, then `python -m pip install ...`.
- One environment per project; never commit `.venv`.
- Restart and run all to verify a notebook.

---

## Answers to Practice Exercises

### Answers: Installing Python

1. Run `python --version`, `python3 --version` or `py --version`, and read the number after the second dot. For example `Python 3.13.16` means minor version 13. Any current Python 3 is fine for this handbook.
2. File `version.py`:

```python
import sys

major, minor = sys.version_info[:2]
print("Python", major, minor)
```

Running `python version.py` prints, for example, `Python 3 13`. The line `major, minor = ...` unpacks the two-item slice into two names (unpacking is explained in [Tuples](21-tuples.md)).
3. `python` points to an old Python 2.7 installation, and `python3` points to Python 3.12. For this course use `python3` (and `python3 -m pip`).
4. First, close the terminal and open a new one, because an open terminal keeps the old `PATH`. If it still fails, try `py --version`, and if that works use `py` or re-run the installer and enable the option that adds Python to `PATH`.

### Answers: Running Python in the Terminal and IDLE

1. Type `7 * 8` and the REPL shows `56`; then `_ * 2` shows `112`. Exit with `exit()`, Ctrl+D (macOS and Linux) or Ctrl+Z then Enter (Windows).
2. For example:

```python
name = "Diya"
print("Hello,", name)
```

Save as `greet.py` and run `python greet.py`.
3. `python -c "print(10 / 4)"` prints `2.5`. So `/` always gives a float result with the fractional part, even when the division is exact (you will study this in [Arithmetic Operators](11-arithmetic-operators.md)).
4. In a script, a bare expression computes a value and throws it away. Change the line to `print(3 * 3)`.

### Answers: Anaconda and Jupyter Notebook Setup

1. The first command (inside the active environment) prints a path that includes `.venv`. After `deactivate`, the same command prints the base installation's path. The two differ.
2. In a notebook cell:

```python
import sys

print(sys.version_info[:2])
```

3. It still works, because deleting a cell does not remove the variable from the kernel's memory. The kernel remembers `x = 5` until you restart it. After restarting the kernel and running only the `print(x)` cell, you get `NameError: name 'x' is not defined`.
4. `venv` is part of the standard library (part of plain Python, though a few Linux distributions package it separately). `pip` is bundled with most Python installations. `conda` comes with Anaconda or Miniconda, which are separate installs. Jupyter Notebook is a separate package; Anaconda includes it, and with plain Python you install it with `pip`.

---

## Chapter Summary and Key Takeaways

- Install Python 3 from python.org or your system's package manager, and verify with `python --version` (or `python3`, or `py`).
- Command-not-found errors usually come from `PATH` or from using the wrong command name.
- Use the REPL (`>>>`) to experiment, `python script.py` to run saved programs, and IDLE or any editor to write them.
- Anaconda bundles Python, data packages and `conda`; Jupyter Notebook is a separate cell-based tool that keeps state between cells.
- Create one virtual environment per project with `python -m venv .venv`, activate it, and install packages with `python -m pip install`.
- Never commit `.venv` or secrets; this repository's `.gitignore` already excludes them.

Next: [Chapter 03 — Built-in Functions, print() and Modules](03-builtin-functions-print-and-modules.md) starts writing real Python with `print()`, other built-in functions and the `math` module.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
