from .git import run_command


def get_ai_review(diff):
    prompt = (
        f"Review this git diff and write a PR title and description. "
        f"Format your response exactly like this:\n"
        f"TITLE: [Your Title]\n"
        f"BODY: [Your Description]\n\n"
        f"Diff:\n{diff}"
    )
    return run_command(["claude", "-p", prompt])


def parse_ai_response(response):
    try:
        title = response.split("TITLE:")[1].split("BODY:")[0].strip()
        body = response.split("BODY:")[1].strip()

        if not title or not body:
            return None, None

        return title, body
    except IndexError, AttributeError:
        return None, None
