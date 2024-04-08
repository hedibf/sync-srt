# sync-srt
Python to sync a .str subtitle file

Usage: **python3 sync-srt.py input_file time_difference**

 **input_file:** Must be .srt file
 **time_difference:** HH:MM:SS,000 or -HH:MM:SS,000

Output:
1. Backup the original .srt appending "-backup" at the end of filename.
2. Rewrite the .str file given using the "time_difference" setting
