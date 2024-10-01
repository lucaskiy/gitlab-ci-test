import os
import subprocess
import re

def run():
    # Get the list of modified files in /project/models/
    modified_files = get_modified_files_in_models()
    # modified_files = ['project/models/orders/orders_test.sql']
    if len(modified_files) > 0:
        # Search for the word in the modified files
        tags = search_for_word_in_files(modified_files)
        for tag in tags:
            command = [
                "docker", "exec", "-t", "gitlab_ci-dbt-1", "dbt", "run", "-s", f"tag:{tag}", 
            ]
            subprocess.run(command, check=True, stdout=None, stderr=subprocess.PIPE, text=True)


def get_modified_files_in_models():
    # Use git to get the list of modified files between current branch and the default branch
    try:
        subprocess.run(['git', 'fetch', 'origin', 'master'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = subprocess.run(['git', 'diff', '--name-only', 'origin/master'], 
                                stdout=subprocess.PIPE, text=True, check=True)
        # Get the list of files
        modified_files = result.stdout.splitlines()
        # Filter to only include files in the /project/models/ directory
        models_files = [f for f in modified_files if f.startswith('project/models/')]
        print(models_files)
        return models_files

    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e}")
        return []   
    

def search_for_word_in_files(files):
    unit_tests = []
    # Search the word in each file
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "tags='unit_test'" or 'tags="unit_test"' in content:
                    config_blocks = re.findall(r'\{\{\s*config.*?\}\}', content, re.DOTALL)
                    for block in config_blocks:
                        matches = re.findall(r'unit_test_\w+', block)
                        unit_tests.extend(matches)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    return unit_tests

run()