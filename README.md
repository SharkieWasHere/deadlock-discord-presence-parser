# Deadlock RPC Bridge

Lightweight Python tool that monitors console.log for the game deadlock. Reads any update from the console and parses information to discord.

# Prerequisites

Before running this script, ensure you have the following installed: 
* **Python3.9 or Higher**
* **Of course Deadlock**

# Setup

1. Clone or download this repository.
2. Install the required Python dependencies. You can run the following:
```bash
pip install -r requirements.txt
```
3. Lastly make sure this is in your steam properties launch options:
```bash
StartDeadlockStatus.bat %command% -condebug
```
# Example
<img width="628" height="141" alt="image" src="https://github.com/user-attachments/assets/8a11d33f-7809-4deb-8afc-fbe5214cea30" />

# Running

Now with this setup whenever you open the game, it will automatically open the python script. This will close when Deadlock is not detected.
Enjoy!
