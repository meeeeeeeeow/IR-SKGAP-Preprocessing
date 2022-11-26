import argparse

def foo():
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    print(args.filename)
    return 

if __name__ == "__main__":
    main()