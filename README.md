# Tetris

Tetris was created with Pygame

## Quick Start

```bash
git clone https://github.com/Veter-ok/pygame-tetris.git
```

``` bash
cd pygame-tetris
```

```bash
pip install -r requirements.txt
```

```bash
python3 main.py
```

## Description

First of all you`ll see main screen, where you need enter your name to remember score

<img width="600" alt="screenshot-1" src="https://user-images.githubusercontent.com/61391385/222982362-8259c242-4e45-415e-8e94-75d70ca0c7c1.png">


Then tap to space and start to play

<img width="699" alt="screenshot-2" src="https://user-images.githubusercontent.com/61391385/222982885-61c5f162-a4e2-4281-94c8-585bad97ec01.png">

## Create .app file

```bash
pip install py2app
```

```bash
touch setup.py
```

Put this code to setup.py

```python
from setuptools import setup

APP = ['main.py']
DATA_FILES = [('imgs', ['./imgs/logo.jpg'])]
OPTIONS = {
	'packages': ['pygame'],
	'argv_emulation': True	
}
PY_MODULE = ['blocks.py', 'board.py', 'tools.py', 'constants.py']

setup(
	app=APP,
    data_files=DATA_FILES,
	py_modules=PY_MODULE,
	name="Tetris",
	options={'py2app': OPTIONS}
)
```

And run build

```bash
python setup.py py2app
```

Tetris.app will be in `./dist`

## Thank you for attention
