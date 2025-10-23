Using Shared Modules from the Libraries Folder

All tasks (Task 1, Task 2, Task 3, Task 4) in this project share common Python modules stored in the Libraries folder.
To ensure these modules can be imported correctly from any task, follow the setup below.

⚙️ Setup Instructions

Add the following code at the very top of every Task_X.py file:

"import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
libraries_path = os.path.join(base_dir, "Libraries")

sys.path.insert(0, libraries_path)"

This code automatically detects your project structure and locates the shared Libraries directory — no matter which task folder the code is running from.

#Run this commands after you update your code
git add . #Run this command after updating your code
git commit -m "Type what you changed" #Then run this command
git push #Run this command to update your code to GitHub

If you want to use the Underground Data in your code
I used this line of code

file_path = os.path.join(base_dir, "data.csv")  # ← This works!
df = pd.read_csv(file_path)  # ← This reads the file successfully

It will work when you combine the code I provided above and this.
