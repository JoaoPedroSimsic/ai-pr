import subprocess


def branch_exists(branch_name):
    result = subprocess.run(
        ["git", "ls-remote", "--exit-code", "--heads", "origin", branch_name],
        capture_output=True,
        text=True,
    )

    return result.returncode == 0


def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_git_diff(base_branch=None):
    if not branch_exists(base_branch):
        print(f"❌ Error: The branch '{base_branch}' does not exist on origin.")
        return None

    diff = run_command(
        ["git", "diff", "--merge-base", base_branch, ":!*.lock", ":!*-lock.json"]
    )

    if diff:
        return diff

    return None


def create_pull_request(title, body, base):
    run_command(["git", "push", "-u", "origin", "HEAD"])

    return run_command(
        ["gh", "pr", "create", "--title", title, "--body", body, "--base", base]
    )
