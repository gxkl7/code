Sad Cafe Protocol
=================

This example is used to introduce the concept of an application protocol, 
along with key elements of server-side and client-side architecture, design
principles, and an introduction to automated unit testing.

In the `test/cafe_test` folder, you'll find several test cases and stubs
for test cases you can implement yourself for practice. The stub test
cases will fail (because they each `assert False`) but when you implement
them all correctly, you should be able to have all tests passing.

There are just a few steps that need to be completed to set up the
example so you can run the demo and run the unit tests.

1. Get the source code from the repository at code.vt.edu
2. Set up a Python "virtual environment", which is basically a project-local
   copy of the Python interpreter into which you can install packages needed
   for this example without making a mess for other projects/examples.
3. Install the `pytest` package needed to run the unit tests.
4. Activate the virtual environment and configure the path Python uses to
   find modules as it runs.
5. Set up the IDE to run the demo program in the `demo` package as a Python
   module.
6. Set up the IDE to run the test cases in the `test` folder using `pytest`.

Your IDE provides mechanisms to help you do all these steps, and there are
lots of helpful resources online that you can use for help. AI assistants can
also be very helpful for doing the setup.

What follows are instructions for how to do the setup in a plain old terminal,
in case all else fails.

### 0. Open a terminal

On MacOS and Linux, launch the standard Terminal app. On Windows, you probably
want to use the Start menu and search for "PowerShell" to run a PowerShell 
terminal.

### 1. Clone the Repository

Get the clone URL for HTTP or SSH from the Sad Cafe repository
at code.vt.edu. Use the HTTP URL if you're using a Personal Access
Token. Use the SSH URL if you're set up to use an SSH key. 

If you haven't done so already, create a folder/directory to hold all the examples
and projects for ECE4564. Students in past semesters have reported various difficulties
when trying to run Python programs from a folder that is stored in OneDrive -- best
to create a local folder.

Make your ECE4564 folder/directory the current directory for your shell.

The command to clone the repository is the same no matter which OS you're
using. This example uses the HTTP URL. Replace it with the SSH URL if you're
using an SSH key.

```
git clone https://code.vt.edu/ece4564/spring-2026/sad-cafe.git
```

### 2. Create a Python Virtual Environment

#### Windows Users
Depending on how you installed Python on your system, the command used
to run the Python interpreter is either `python` or `py`. The instructions
below assume the more common case (`python`), but if you get an error
indicating command not found, try `py` instead.

#### MacOS/Linux Users:
All distributions install the Python interpreter as `python3` to avoid
the potential for running the older Python 2 which is still included in
some distributions.

First **make the** `sad-cafe` **folder the current directory for your shell**.

Next, on Windows, create the virtual environment using this command:
```
python -m venv venv
```

On MacOS and Linux, create the virtual environment using this command:
```
python3 -m venv venv
```

### 3. Activate the Python Virtual Environment

On Windows, tell PowerShell to allow local script execution and then activate
the Python environment using the script provided with it.

```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

On MacOS abd Linux, activate the environment by sourcing it into your shell.
```
source venv/bin/activate
```

### 4. Install the Pytest package.

Make sure that you already activated the Python virtual environment as
specified in the previous step.

Windows users use this command to install Pytest into the virtual environment.
```
python -m pip install pytest
```

MacOS and Linux users do this instead.
```
python3 -m pip install pytest
```

### 5. Run the Demo

On Windows, set `PYTHONPATH` in your shell's enviroment, and then run the 
demo using Python.
```
$env:PYTHONPATH = ".\src"
python -m demo
```

On MacOS and Linux, specify the Python path on the command line when you 
run the demo:

```
PYTHONPATH=./src python3 -m demo
```

When the demo starts, it'll print "Waiting for request...". At that point you
can send a request string such as LIST MENU. See the Lecture 1 Slides for other
protocol request messages you can send and the expected responses.

#### 6. Run the Unit tests

Run this command to run all the test cases in the `test` folder (same command
for Windows, Mac OS, Linux):

```
pytest test
```
