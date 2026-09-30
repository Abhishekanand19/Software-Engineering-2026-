import argparse
from game import WordleGame


def main():
    parser = argparse.ArgumentParser(description="Play terminal Wordle.")
    parser.add_argument("length", nargs="?", type=int, choices=(4, 5, 6), default=5,
                        help="word length (default: 5)")
    args = parser.parse_args()
    WordleGame(length=args.length).run()


if __name__ == "__main__":
    main()
