import os

def remove_and_log(file_path):
    """Remove a file and log the action."""
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed file: {file_path}")
        return True
    return False

# Remove all txt files in variants_out/games
"""
games_dir = 'variants_out/games'
for file_name in os.listdir(games_dir):
    if file_name.endswith('.txt'):
        file_path = os.path.join(games_dir, file_name)
        remove_and_log(file_path)
"""

for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
    for file_name in files:
        # All nohup.out files
        if file_name == 'nohup.out':
            file_path = os.path.join(root, file_name)
            remove_and_log(file_path)
        # All .log files
        elif file_name.endswith('.log'):
            file_path = os.path.join(root, file_name)
            remove_and_log(file_path)
        # All pickle files
        elif file_name.endswith('.pickle'):
            file_path = os.path.join(root, file_name)
            remove_and_log(file_path)