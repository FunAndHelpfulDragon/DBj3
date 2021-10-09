import os
os.system("python -m venv .venv")
os.system(".venv/bin/python -m pip install discord.py")
os.system(".venv/bin/python -m pip install dislash.py")
os.system(".venv/bin/python -m pip install aiofiles")
os.system("clear")
print("Finish seting up required files for the bot to run!")
Token = input("Please enter the bot token: ")
os.system(f"echo '{Token}' > Token.txt")
print(f"run 'python start.py' to run the bot")  # noqa
