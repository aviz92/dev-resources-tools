# tree - structure project in a hierarchical format

### Purpose
The `tree` command is used to visualize the directory structure of a project in a hierarchical format. <br>
By redirecting the output with `>`, the structure is saved into a text file, commonly used for documentation or sharing the layout of a codebase. <br>

### What It Does
Lists all directories and files in the current folder recursively. <br>
Saves the output to project_structure.txt. <br>

### Use Case
This is useful for: <br>
 - Documenting the file structure of a repository.
 - Reviewing a project's layout during code reviews.
 - Sharing directory overviews in README or technical documentation.

###  How to Use
 - install `tree` command:
```bash
brew install tree
```

execute the command in the terminal of the project folder:
```bash
tree > project_structure.txt -L 5 -a -I '__pycache__|.venv|.git|.idea|.DS_Store'
```
