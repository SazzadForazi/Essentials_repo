## Basic Commands

### Start a New Session
To start a new screen session:
```bash
screen
```
Or with a custom name:
```bash
screen -S session_name
```

### Detach from a Session
To detach from the screen session and return to the terminal:
```bash
Ctrl + A, then D
```

### List Sessions
To list all active screen sessions:
```bash
screen -ls
```

### Reattach to a Session
To reattach to a session:
```bash
screen -r session_name
```
Or simply:
```bash
screen -r
```
To reattach to a session and detach it from another terminal:
```bash
screen -rd session_name
```

### Kill a Session
To terminate the screen session:
```bash
exit
```
Or directly kill a session from another terminal:
```bash
screen -X -S session_name quit
```

## Useful Features

### Split Screen
To split the screen into two regions:
```bash
Ctrl + A, then S
```
To switch between regions:
```bash
Ctrl + A, then Tab
```
To close a region:
```bash
Ctrl + A, then X
```

### Scrollback Mode
To enter scrollback mode:
```bash
Ctrl + A, then [
```
Use the arrow keys to scroll. Exit with:
```bash
Ctrl + C
```

### Switch Between Windows
To create a new window:
```bash
Ctrl + A, then C
```
Switch between windows:
```bash
Ctrl + A, then N (next)
Ctrl + A, then P (previous)
```
