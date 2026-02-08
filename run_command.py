#!/usr/bin/env python3
"""
Simple command runner for lead generation
Usage: python3 run_command.py "your command here"
"""

import sys
from command_interface import run_command

if __name__ == "__main__":
    if len(sys.argv) < 2:
        command = input("Enter command: ")
    else:
        command = ' '.join(sys.argv[1:])
    
    result = run_command(command)
    print(result)