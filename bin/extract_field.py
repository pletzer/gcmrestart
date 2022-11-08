import re
import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", type=str, help="regular expression pattern")
    parser.add_argument("--file", type=str, help="file from which the pattern value should be extracted")
    args = parser.parse_args()

    if not args.pattern:
        print('ERROR: must provide a pattern')
        sys.exit(1)

    if not args.file:
        print('ERROR: must provide a file')
        sys.exit(2)

    pat = re.compile(args.pattern)

    with open(args.file, 'r') as f:
        for line in f.readlines():
            m = re.match(pat, line)
            if m:
                print(m.group(1))
                break


if __name__ == '__main__':
    main()
