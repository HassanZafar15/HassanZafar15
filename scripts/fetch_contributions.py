import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from urllib.request import Request, urlopen

USERNAME = "HassanZafar15"
TOKEN = os.environ["STATS_TOKEN"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }
  }
}
"""


def fetch_calendar():
    now = datetime.now(timezone.utc)
    payload = json.dumps({
        "query": QUERY,
        "variables": {
            "login": USERNAME,
        },
    }).encode("utf-8")

    req = Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": f"{USERNAME}-readme-cards",
        },
    )
    with urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    if "errors" in data:
        raise RuntimeError(data["errors"])

    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = []
    for week in cal["weeks"]:
        for d in week["contributionDays"]:
            days.append({
                "date": d["date"],
                "count": d["contributionCount"],
                "level": d["contributionLevel"],
            })

    days.sort(key=lambda x: x["date"])

    # Monthly totals
    monthly_map = defaultdict(int)
    for d in days:
        monthly_map[d["date"][:7]] += d["count"]
    monthly = [{"month": k, "count": v} for k, v in sorted(monthly_map.items())][-12:]

    # Active days & busiest day
    active_days = sum(1 for d in days if d["count"] > 0)
    busiest = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}

    # Longest streak
    longest_streak = 0
    run = 0
    for d in days:
        if d["count"] > 0:
            run += 1
            longest_streak = max(longest_streak, run)
        else:
            run = 0

    # Current streak (don't break streak if today simply has 0 commits so far)
    current_streak = 0
    check_days = days[:-1] if days and days[-1]["count"] == 0 else days
    for d in reversed(check_days):
        if d["count"] > 0:
            current_streak += 1
        else:
            break

    os.makedirs("data", exist_ok=True)
    output = {
        "updated_at": now.isoformat(),
        "total_contributions": cal["totalContributions"],
        "active_days": active_days,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "busiest_day": busiest,
        "monthly": monthly,
        "days": days,
    }
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    fetch_calendar()
