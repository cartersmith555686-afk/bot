import os, importlib

def load_plugins(bot):
    if not os.path.exists("plugins"):
        return
    for file in os.listdir("plugins"):
        if file.endswith(".py"):
            importlib.import_module(f"plugins.{file[:-3]}").setup(bot)
