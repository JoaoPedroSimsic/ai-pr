import subprocess
import sys

def run_command(command):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def get_git_diff():
    """Returns the git diff of the current branch."""
    try:
        return run_command(["git", "diff", "--merge-base", "main", ":!*.lock", ":!*-lock.json"])
    except Exception:
        return run_command(["git", "diff", "--merge-base", "master", ":!*.lock", ":!*-lock.json"])

def main():
    print("🔍 Fetching git diff...")
    diff = get_git_diff()
    
    if not diff:
        print("✅ No changes to report.")
        return

    prompt = (
        f"Review this git diff and write a PR title and description. "
        f"Format your response exactly like this:\n"
        f"TITLE: [Your Title]\n"
        f"BODY: [Your Description]\n\n"
        f"Diff:\n{diff}"
    )

    print("🤖 Sending to Claude (via your Subscription)...")
    
    ai_response = run_command(["claude", "-p", prompt])

    if not ai_response:
        print("❌ Claude didn't return a response.")
        return

    print("\n--- Draft PR ---")
    print(ai_response)
    print("----------------\n")

    confirm = input("Would you like to create this PR now? (y/n): ")
    if confirm.lower() == 'y':
        try:
            title = ai_response.split("TITLE:")[1].split("BODY:")[0].strip()
            body = ai_response.split("BODY:")[1].strip()
            
            run_command(["gh", "pr", "create", "--title", title, "--body", body])
            print("🚀 PR successfully created!")
        except IndexError:
            print("⚠️ Parsing error: Claude's response wasn't in the expected format.")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()
