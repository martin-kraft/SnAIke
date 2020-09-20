 #!/bin/bash
 
 pyinstaller --add-data "/home/martin/Dropbox/SnAIke/assets:assets" snake.py --hidden-import=packaging.requirements --hidden-import="PIL._tkinter_finder" --onefile
