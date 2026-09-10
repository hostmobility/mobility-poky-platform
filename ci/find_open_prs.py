import json
import urllib.request
from datetime import datetime, timedelta, timezone


GITHUB_REPOSITORY = "hostmobility/mobility-poky-platform"
GITHUB_API_URL = (
    f"https://api.github.com/repos/"
    f"{GITHUB_REPOSITORY}/pulls?state=open&per_page=100"
)


def github_request(url):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "jenkins-mobility-poky-platform",
        },
    )

    with urllib.request.urlopen(request) as response:
        return json.load(response)


def main():
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)

    print(f"Repository: {GITHUB_REPOSITORY}")
    print(f"Looking for open PRs updated since: {cutoff.isoformat()}")
    print()

    pull_requests = github_request(GITHUB_API_URL)

    recent_prs = []

    for pr in pull_requests:
        updated_at = datetime.fromisoformat(
            pr["updated_at"].replace("Z", "+00:00")
        )

        if updated_at >= cutoff:
            recent_prs.append(pr)

    if not recent_prs:
        print("No open PRs updated within the last 30 days.")
        return

    print(f"Found {len(recent_prs)} PR(s):")
    print()

    for pr in recent_prs:
        print(f"PR #{pr['number']}: {pr['title']}")
        print(f"  Updated:  {pr['updated_at']}")
        print(f"  Branch:   {pr['head']['ref']}")
        print(f"  Head SHA: {pr['head']['sha']}")
        print()


if __name__ == "__main__":
    main()