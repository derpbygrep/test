import subprocess
import re

# Path to your tags file
tags_file = 'tags.txt'

# Command pattern to run (adapt as needed)
command_pattern = 'python3 best-caf* {}'

def extract_tags(filename):
    tags = []
    with open(filename, 'r') as f:
        for line in f:
            if '[new tag]' in line:
                parts = line.strip().split()
                tag = parts[-1]
                tags.append(tag)
    return tags

def get_lines_changed(tag):
    try:
        # Run your command for each tag
        result = subprocess.run(command_pattern.format(tag), shell=True, capture_output=True, text=True, timeout=300)
        output = result.stdout

        # Extract lines changed from the output
        match = re.search(r'Lines changed:\s+(\d+)', output)
        if match:
            return int(match.group(1))
        else:
            print(f"[WARNING] No match for tag: {tag}")
            return None
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Timeout expired for tag: {tag}")
        return None
    except Exception as e:
        print(f"[ERROR] Exception for tag {tag}: {e}")
        return None

def main():
    tags = extract_tags(tags_file)
    print(f"Total tags found: {len(tags)}")

    best_tag = None
    least_changes = None

    for tag in tags:
        print(f"Processing tag: {tag}")
        lines_changed = get_lines_changed(tag)

        if lines_changed is not None:
            print(f"Tag: {tag}, Lines changed: {lines_changed}")

            if least_changes is None or lines_changed < least_changes:
                least_changes = lines_changed
                best_tag = tag

    print("\nBest tag found:")
    print(f"TAG: {best_tag}")
    print(f"Lines changed: {least_changes}")

if __name__ == '__main__':
    main()
