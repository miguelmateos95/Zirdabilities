import time
from src.deck import Deck
from src.engine import GameEngine


def run_monte_carlo(iterations: int = 100000):
    print("=" * 65)
    print("🚀 ZIRDABILITIES: MONTE CARLO COMBO SIMULATOR")
    print("=" * 65)

    # 1. Load Deck
    deck = Deck("decklist.txt")
    if len(deck) == 0:
        print("Error: Could not load decklist.txt. Please check the file.")
        return

    print(f"Loaded Deck: {len(deck)} cards.")
    print(f"Running {iterations:,} simulated games...\n")

    start_time = time.time()

    # Metrics Tracking
    wins_total = 0
    wins_by_mulligan = {0: 0, 1: 0, 2: 0}

    # Lists to capture sample trace logs
    winning_logs = []
    losing_logs = []

    # 2. Monte Carlo Execution Loop
    for _ in range(iterations):
        # We only record execution traces when we still need sample winning/losing logs
        need_win = len(winning_logs) < 5
        need_loss = len(losing_logs) < 5
        record = need_win or need_loss

        engine = GameEngine(deck, debug=record)
        success, reason = engine.run_simulation()

        if success:
            wins_total += 1
            if "Mulligan 0" in reason:
                wins_by_mulligan[0] += 1
            elif "Mulligan 1" in reason:
                wins_by_mulligan[1] += 1
            elif "Mulligan 2" in reason:
                wins_by_mulligan[2] += 1

            if need_win:
                winning_logs.append(engine.log)
        else:
            if need_loss:
                losing_logs.append(engine.log)

    elapsed = time.time() - start_time

    # 3. Calculation & Metrics Output
    win_rate_total = (wins_total / iterations) * 100
    m0_rate = (wins_by_mulligan[0] / iterations) * 100
    m1_rate = (wins_by_mulligan[1] / iterations) * 100
    m2_rate = (wins_by_mulligan[2] / iterations) * 100

    print("=" * 65)
    print("📊 SIMULATION RESULTS SUMMARY")
    print("=" * 65)
    print(f"Total Iterations: {iterations:,}")
    print(f"Execution Time  : {elapsed:.2f} seconds")
    print("-" * 65)
    print(f"Overall T2 Win Rate: {win_rate_total:.2f}%\n")
    print("Breakdown by Mulligan Level:")
    print(f"  • Hand of 7 (No Mulligan) : {m0_rate:.2f}%")
    print(f"  • Hand of 6 (1 Mulligan)   : {m1_rate:.2f}%")
    print(f"  • Hand of 5 (2 Mulligans)  : {m2_rate:.2f}%")
    print("=" * 65)

    # 4. Print 5 Sample Winning Games
    print("\n" + "🟢 " * 10 + " 5 SAMPLE WINNING HANDS " + "🟢 " * 10)
    for idx, log_trace in enumerate(winning_logs, 1):
        print(f"\n--- [WINNING GAME #{idx}] ---")
        for line in log_trace:
            print(f"  {line}")

    # 5. Print 5 Sample Losing Games
    print("\n" + "🔴 " * 10 + " 5 SAMPLE LOSING HANDS " + "🔴 " * 10)
    for idx, log_trace in enumerate(losing_logs, 1):
        print(f"\n--- [LOSING GAME #{idx}] ---")
        for line in log_trace:
            print(f"  {line}")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    run_monte_carlo(iterations=100000)
