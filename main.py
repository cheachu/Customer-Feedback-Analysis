import subprocess
import sys
import os


def run_script(script_name):

    if not os.path.exists(script_name):
        print(f"Error: Could not find '{script_name}' in the current directory.")
        sys.exit(1)

    try:
        subprocess.run([sys.executable, script_name], check=True)
        print(f"Done: {script_name}\n")
    except subprocess.CalledProcessError as e:
        print(f"Failed: '{script_name}'  to execute.")
        sys.exit(1)


def main():
    run_script("synthetic_data.py")
    run_script("sentiment_topic_analysis.py")
    run_script("load_csv.py")

    print("Done")


if __name__ == "__main__":
    main()
