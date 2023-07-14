import screen

import saves_db

# Saving system initialization 
saves_database = saves_db.SavesDatabase()
saves_database.initialize()

# The entry point of the whole game
if __name__ == '__main__':
    screen.MainScreen().run()
