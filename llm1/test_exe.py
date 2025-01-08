import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from code_execution.main import run_command

command = "mysql -uuser1 -pRajneesh#2024 -e 'show databases;'"
# command = "ls -la"
result = run_command(command)
print(result)
