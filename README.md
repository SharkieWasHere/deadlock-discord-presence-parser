# Deadlock RPC Bridge

Lightweight Python tool that monitors console.log for the game deadlock. Reads any update from the console and parses information to discord.

# Prerequisites

Before running this script, ensure you have the following installed: 
* **[Python3.9 or Higher](https://www.python.org/downloads/)**
* **Of course Deadlock**

# Setup

1. Clone or download this repository.
2. Install the required Python dependencies. You can run one of the following:
### If you cloned the repository run this:__
```bash
pip install -r requirements.txt
```
### If you are manually installing, run this in Command Prompt:
```bash
pip install pypresence
```

3.Extract the contents fully in the deadlock local files. You can go to steam - browse local files.

## Example
<img width="628" height="175" alt="image" src="https://github.com/user-attachments/assets/c8f0f5ce-027b-4b7f-b5f7-a0eb1e7841d9" />


4. Lastly make sure this is in your steam properties launch options:
```bash
StartDeadlockStatus.bat %command% -condebug
```
## Example
<img width="628" height="141" alt="image" src="https://github.com/user-attachments/assets/8a11d33f-7809-4deb-8afc-fbe5214cea30" />

# Running

Now with this setup whenever you open the game, it will automatically open the python script. This will close when Deadlock is not detected.
Enjoy!
And please feel free to edit or remove anything from this file!
This was just made for my self as a non flashy status for discord.
