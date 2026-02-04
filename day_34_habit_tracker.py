import json
from pathlib import Path
import datetime
from typing import Dict, Any

try:
    import pandas as pd
    _HAS_PANDAS = True
except Exception:
    _HAS_PANDAS = False

DATA_FILE = Path(__file__).parent / "life_data.json"

LEVELS = ["Beginner", "Learner", "Builder", "Pro", "Legend"]
BADGES = {
    "7-day streak": "Maintain any habit for 7 days",
    "No-Spend Day": "0 expense in a day"
}


def load() -> Dict[str, Any]:
    if not DATA_FILE.exists():
        return {
            "habits": {},
            "expenses": [],
            "xp": 0,
            "coins": 0,
            "level": 0,
            "streaks": {},
            "badges": [],
            "goals": {}
        }
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {
            "habits": {},
            "expenses": [],
            "xp": 0,
            "coins": 0,
            "level": 0,
            "streaks": {},
            "badges": [],
            "goals": {}
        }


def save(data: Dict[str, Any]):
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


data = load()


# ---------- HELPERS ----------
def _today() -> datetime.date:
    return datetime.date.today()


def _yesterday() -> datetime.date:
    return _today() - datetime.timedelta(days=1)


def _ensure_habit(name: str) -> bool:
    return name in data["habits"]


# ---------- CORE ----------
def add_habit(name: str):
    name = name.strip()
    if not name:
        print("Invalid habit name.")
        return
    if name in data["habits"]:
        print("Habit already exists.")
        return
    data["habits"][name] = []
    data["streaks"][name] = 0
    save(data)
    print(f"Habit added: {name}")


def mark_habit(name: str):
    if not _ensure_habit(name):
        print("Habit not found. Use 'add' to create it first.")
        return
    today = _today().isoformat()
    dates = data["habits"].get(name, [])
    if dates and dates[-1] == today:
        print("Already marked today.")
        return

    # update streak: if last marked was yesterday -> +1 else reset to 1
    if dates:
        try:
            last = datetime.date.fromisoformat(dates[-1])
            if last == _yesterday():
                data["streaks"][name] = data["streaks"].get(name, 0) + 1
            else:
                data["streaks"][name] = 1
        except Exception:
            data["streaks"][name] = 1
    else:
        data["streaks"][name] = 1

    data["habits"][name].append(today)
    gain_xp(10)
    check_badges(name)
    save(data)
    print(f"🔥 Habit '{name}' done today!")


def remove_habit(name: str):
    if not _ensure_habit(name):
        print("Habit not found.")
        return
    data["habits"].pop(name, None)
    data["streaks"].pop(name, None)
    save(data)
    print(f"Removed habit: {name}")


def list_habits():
    if not data["habits"]:
        print("No habits yet.")
        return
    for i, (name, dates) in enumerate(data["habits"].items(), 1):
        streak = data["streaks"].get(name, 0)
        last = dates[-1] if dates else "-"
        print(f"{i}. {name} (streak: {streak}, last: {last})")


def add_expense(amount: float, category: str, note: str = ""):
    try:
        amount = float(amount)
    except Exception:
        print("Invalid amount.")
        return
    if amount <= 0:
        print("Amount must be positive.")
        return
    today = _today().isoformat()
    data["expenses"].append({
        "date": today,
        "amount": amount,
        "category": category.strip() or "uncategorized",
        "note": note.strip()
    })
    data["coins"] -= int(amount / 10)
    save(data)
    no_spend_today()


def monthly_summary():
    if not data["expenses"]:
        print("No expenses yet.")
        return
    if _HAS_PANDAS:
        df = pd.DataFrame(data["expenses"])
        df["date"] = pd.to_datetime(df["date"])
        month = datetime.datetime.now().month
        mdf = df[df["date"].dt.month == month]
        print(mdf.groupby("category")["amount"].sum())
        return
    # fallback simple summary
    month = datetime.datetime.now().month
    agg = {}
    for e in data["expenses"]:
        try:
            d = datetime.date.fromisoformat(e["date"])
        except Exception:
            continue
        if d.month != month:
            continue
        agg[e["category"]] = agg.get(e["category"], 0) + e["amount"]
    if not agg:
        print("No expenses this month.")
        return
    for k, v in agg.items():
        print(f"{k}: {v}")


# ---------- GAMIFICATION ----------
def gain_xp(x: int):
    data["xp"] = data.get("xp", 0) + int(x)
    next_level_xp = (data.get("level", 0) + 1) * 100
    if data["xp"] >= next_level_xp:
        data["level"] = min(data.get("level", 0) + 1, len(LEVELS) - 1)
        print(f"🎉 Level Up! You are now {LEVELS[data['level']]}")
        save(data)


def check_badges(habit: str):
    if data["streaks"].get(habit, 0) >= 7 and "7-day streak" not in data["badges"]:
        data["badges"].append("7-day streak")
        print("🏅 Badge Unlocked: 7-day streak")
        save(data)


def no_spend_today():
    today = _today().isoformat()
    if not any(e["date"] == today for e in data["expenses"]):
        if "No-Spend Day" not in data["badges"]:
            data["badges"].append("No-Spend Day")
            print("🏅 Badge: No-Spend Day")
            save(data)


# ---------- AI INSIGHTS ----------
def ai_spending_insight():
    if not data["expenses"]:
        print("No expenses to analyze.")
        return
    if _HAS_PANDAS:
        df = pd.DataFrame(data["expenses"])
        total = df["amount"].sum()
        cat = df.groupby("category")["amount"].sum()
        top = cat.idxmax()
        perc = (cat.max() / total) * 100
        print(f"🤖 You spend {perc:.1f}% on {top}")
        return
    # fallback
    agg = {}
    total = 0
    for e in data["expenses"]:
        agg[e["category"]] = agg.get(e["category"], 0) + e["amount"]
        total += e["amount"]
    top = max(agg, key=agg.get)
    perc = (agg[top] / total) * 100 if total else 0
    print(f"🤖 You spend {perc:.1f}% on {top}")


def auto_budget():
    if not data["expenses"]:
        print("No expenses to suggest budget for.")
        return
    if _HAS_PANDAS:
        df = pd.DataFrame(data["expenses"])
        avg = df.groupby("category")["amount"].mean()
        print("💡 Suggested budget:")
        print(avg)
        return
    agg = {}
    counts = {}
    for e in data["expenses"]:
        agg[e["category"]] = agg.get(e["category"], 0) + e["amount"]
        counts[e["category"]] = counts.get(e["category"], 0) + 1
    print("💡 Suggested budget:")
    for k in agg:
        print(f"{k}: {agg[k] / counts[k]:.2f}")


def show_stats():
    print("XP:", data.get("xp", 0), "Level:", LEVELS[data.get("level", 0)])
    print("Coins:", data.get("coins", 0), "Badges:", data.get("badges", []))


def main():
    while True:
        print(
            "\n1.List Habits 2.Add Habit 3.Mark Habit 4.Remove Habit 5.Add Expense 6.Monthly Summary"
        )
        print("7.AI Insight 8.Show Stats 9.Auto Budget 0.Exit")
        ch = input("Choose: ").strip()

        if ch == "1":
            list_habits()
        elif ch == "2":
            add_habit(input("Habit name: "))
        elif ch == "3":
            mark_habit(input("Habit name: "))
        elif ch == "4":
            remove_habit(input("Habit name to remove: "))
        elif ch == "5":
            amt = input("Amount: ")
            cat = input("Category: ")
            note = input("Note: ")
            add_expense(amt, cat, note)
        elif ch == "6":
            monthly_summary()
        elif ch == "7":
            ai_spending_insight()
        elif ch == "8":
            show_stats()
        elif ch == "9":
            auto_budget()
        elif ch == "0":
            save(data)
            print("Saved. Bye!")
            break
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()
