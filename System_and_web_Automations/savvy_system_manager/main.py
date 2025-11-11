import argparse
import sys


def run_gui():
    from gui_app import launch_gui

    launch_gui()


def run_cli(extra_args):
    from cli_app import run_cli

    run_cli(extra_args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SavvySystem Manager — System Control Automation Tool"
    )
    parser.add_argument("--cli", action="store_true", help="Run the CLI version")
    parser.add_argument("--gui", action="store_true", help="Run the GUI version")

    # ✅ Use parse_known_args to ignore extra CLI args (e.g., restart, --rename)
    args, extra = parser.parse_known_args()

    if args.cli:
        run_cli(extra)  # ✅ Pass remaining args to Click
    elif args.gui:
        run_gui()
    else:
        print("Usage: python main.py --cli | --gui")
