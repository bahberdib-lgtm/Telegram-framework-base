import os
import shutil
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Telegram Bot Generator")
    parser.add_argument("name", help="Name of the bot project")
    parser.add_argument("--base", default="basic_bot", help="Base template to use (e.g., basic_bot, sqlite_bot)")
    args = parser.parse_args()

    # Find template
    # This is a simplified search for the template
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    template_path = None
    for root, dirs, files in os.walk(templates_dir):
        if args.base in dirs:
            template_path = os.path.join(root, args.base)
            break
            
    if not template_path:
        print(f"Error: Template '{args.base}' not found.")
        sys.exit(1)

    project_dir = os.path.join(os.getcwd(), args.name)
    if os.path.exists(project_dir):
        print(f"Error: Directory '{args.name}' already exists.")
        sys.exit(1)

    shutil.copytree(template_path, project_dir)
    print(f"Success! Bot project '{args.name}' created based on '{args.base}'.")
    print(f"cd {args.name}")

if __name__ == "__main__":
    main()
