Using Shared Modules from the Libraries Folder

All tasks (Task 1, Task 2, Task 3, Task 4) in this project share common Python modules stored in the Libraries folder.
To ensure these modules can be imported correctly from any task, follow the setup below.

⚙️ Setup Instructions

Add the following code at the very top of every Task_X.py file:

"import os
import sys

# Dynamically find the path to the Libraries folder
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")

# Add Libraries folder to Python import path
sys.path.insert(0, libraries_path)"

This code automatically detects your project structure and locates the shared Libraries directory — no matter which task folder the code is running from.
