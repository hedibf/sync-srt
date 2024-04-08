import sys
import re
import shutil

def parse_time(time_str, neg=False):
    # Regular expression to match HH:MM:SS,ms format
    time_regex = r'(-?\d+):(\d+):(\d+),(\d+)'
    match = re.match(time_regex, time_str)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        milliseconds = int(match.group(4))
        total_milliseconds = hours * 3600 * 1000 + minutes * 60 * 1000 + seconds * 1000 + milliseconds
        if neg:
            total_milliseconds = -total_milliseconds
        return total_milliseconds
    else:
        print("Invalid time format. Please use HH:MM:SS,ms.")
        sys.exit(1)

def format_time(milliseconds):
    hours = int(milliseconds/1000 // 3600)
    minutes = int((milliseconds/1000 % 3600) // 60)
    seconds = int(milliseconds/1000 % 60)
    milliseconds = int((milliseconds) % 1000)
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(hours, minutes, seconds, milliseconds)

def resynchronize_srt(input_file, time_difference_str, neg):
    # Create backup of the original file
    backup_file = input_file[:-4] + "-backup.srt"
    shutil.copy(input_file, backup_file)

    # Parse time difference string to get the difference in seconds
    time_difference = parse_time(time_difference_str, neg)

    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(input_file, 'w') as f:
        for line in lines:
            if '-->' in line:
                start, end = line.strip().split(' --> ')
                start_time = parse_time(start)
                end_time = parse_time(end)
                start_time += time_difference
                end_time += time_difference
                new_start = format_time(start_time)
                new_end = format_time(end_time)
                f.write('{} --> {}\n'.format(new_start, new_end))
            else:
                f.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python sync-srt.py input_file time_difference")
        print(" input_file: Must be .srt file")
        print(" time_difference: HH:MM:SS,000 or -HH:MM:SS,000")
        sys.exit(1)

    input_file = sys.argv[1]
    time_difference_str = sys.argv[2]
    negative = sys.argv[2][0] == '-'

    resynchronize_srt(input_file, time_difference_str, negative)
    print("Subtitles resynchronized successfully!")
