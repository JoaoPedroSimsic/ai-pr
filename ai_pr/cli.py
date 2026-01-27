from .git import get_git_diff, create_pull_request
from .models import get_ai_review, parse_ai_response

import sys


def main():
    if len(sys.argv) < 2:
        print("💡 Usage: ai-pr <target-branch>")
        print("Example: ai-pr main")
        return

    target_branch = sys.argv[1]

    print(f"🔍 Fetching git diff against {target_branch}...")
    diff = get_git_diff(target_branch)

    if not diff:
        return

    print("🤖 Sending to Claude...")

    response = get_ai_review(diff)

    if not response:
        print("❌ Claude didn't return a response.")
        return

    title, body = parse_ai_response(response)

    if not title or not body:
        print("⚠️ Parsing error: Check Claude's response format.")
        return

    print(f"\n--- Draft PR ---\nTITLE: {title}\nBODY: {body}\n----------------\n")

    if input(f"Create PR into '{target_branch}'? (y/n): ").lower() == "y":
        if create_pull_request(title, body, target_branch):
            print("🚀 PR successfully created!")
        else:
            print("❌ Failed to create PR.")
