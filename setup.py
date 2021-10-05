import os
os.system("python -m venv .venv")
os.system(".venv/bin/python -m pip install discord.py")
os.system(".venv/bin/python -m pip install dislash.py")
os.system(".venv/bin/python -m pip install aiofiles")
os.system("clear")
print("Finish seting up required files for the bot to run!")
print(f"run {os.path.dirname(__file__)}/.venv/bin/python bot.py to run the bot")  # noqa
