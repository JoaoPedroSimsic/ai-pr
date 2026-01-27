import subprocess
import sys
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running {' '.join(command)}: {e.stderr}")
        sys.exit(1)

def get_git_diff():
    return run_command(["git", "diff", "main...HEAD", ":!*.lock", ":!*-lock.json"])

def get_ai_pr_details(diff):
    system_prompt = (
        "You are a helpful assistant that writes GitHub Pull Request descriptions. "
        "Use Conventional Commits for the title (e.g., feat: ..., fix: ...). "
        "The body should be clear, using Markdown bullets for changes."
    )

    user_prompt = f"Write a PR title and description for this diff:\n\n{diff}"

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )

    content = message.content[0].text
    lines = content.split('\n')
    title = lines[0].replace("Title: ", "").strip()
    body = "\n".join(lines[1:]).strip()
    return title, body

def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found in environment.")
        sys.exit(1)
    
        print("Reading git diff...")
        diff = get_git_diff()

        if not diff:
            print("No changes detected between main and HEAD")
            return
        
    print("Asking cluade to draft the PR...")
    title, body = get_ai_pr_details(diff)

    print(f"\n--- Proposed PR ---\nTitle: {title}\n\n\{body}\n------------------\n")

    confirm = input("Submit this Pull Request? (y/N): ")

    if confirm.lower() == 'y':
        run_command(["gh", "pr", "create", "--title", title, "--body", body])
        print("PR create successfully!")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()














