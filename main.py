# ==============================================================================
# SCRIPT PRINCIPAL DE SIMULACIÓN MONTE CARLO
# ==============================================================================

import time
from src.deck import Deck
from src.engine import GameEngine


def run_monte_carlo(iterations=100000):
    print("=" * 65)
    print("🚀 ZIRDABILITIES: MONTE CARLO COMBO SIMULATOR")
    print("=" * 65)

    deck = Deck("decklist.txt")
    print(f"Loaded Deck: {len(deck)} cards.")
    print(f"Running {iterations:,} simulated games...\n")

    wins = 0
    mulligan_counts = {0: 0, 1: 0, 2: 0}
    mulligan_wins = {0: 0, 1: 0, 2: 0}

    winning_samples = []
    losing_samples = []

    start_time = time.time()

    for i in range(iterations):
        record = i < 5 or (iterations - i) <= 5
        engine = GameEngine(deck, debug=record)
        mulls = engine.mulligans
        mulligan_counts[mulls] = mulligan_counts.get(mulls, 0) + 1

        success, reason = engine.run_simulation(max_turns=2)

        if success:
            wins += 1
            mulligan_wins[mulls] = mulligan_wins.get(mulls, 0) + 1
            if len(winning_samples) < 5:
                winning_samples.append((engine, i + 1, reason))
        else:
            if len(losing_samples) < 5:
                losing_samples.append((engine, i + 1, reason))

    elapsed_time = time.time() - start_time

    # Imprimir Resumen de Resultados
    print("=" * 65)
    print("📊 SIMULATION RESULTS SUMMARY")
    print("=" * 65)
    print(f"Total Iterations: {iterations:,}")
    print(f"Execution Time  : {elapsed_time:.2f} seconds")
    print("-" * 65)

    win_rate = (wins / iterations) * 100
    print(f"Overall T2 Win Rate: {win_rate:.2f}%\n")

    print("Breakdown by Mulligan Level:")
    for m in range(3):
        total_m = mulligan_counts.get(m, 0)
        wins_m = mulligan_wins.get(m, 0)
        rate_m = (wins_m / total_m * 100) if total_m > 0 else 0.0
        label = "No Mulligan" if m == 0 else f"{m} Mulligan(s)"
        print(f"  • Hand of {7 - m} ({label}) : {rate_m:.2f}% ({wins_m}/{total_m})")

    print("=" * 65)

    # Muestras de Ganadoras
    print("\n🟢 5 SAMPLE WINNING HANDS 🟢\n")
    for engine, idx, reason in winning_samples:
        hand_names = [getattr(c, "name", str(c)) for c in engine.state.hand]
        board_names = [getattr(c, "name", str(c)) for c in engine.state.battlefield]
        print(f"--- [WINNING GAME #{idx}] ---")
        print(f"  Mulligans: {engine.mulligans}")
        print(f"  Mano Restante: {hand_names}")
        print(f"  Board State Final: {board_names}")
        print(f"  ✅ RESULTADO: {reason}\n")

    # Muestras de Perdedoras
    print("\n🔴 5 SAMPLE LOSING HANDS 🔴\n")
    for engine, idx, reason in losing_samples:
        hand_names = [getattr(c, "name", str(c)) for c in engine.state.hand]
        board_names = [getattr(c, "name", str(c)) for c in engine.state.battlefield]
        print(f"--- [LOSING GAME #{idx}] ---")
        print(f"  Mulligans: {engine.mulligans}")
        print(f"  Mano Restante: {hand_names}")
        print(f"  Board State Final: {board_names}")
        print(f"  ❌ RESULTADO: {reason}\n")


if __name__ == "__main__":
    run_monte_carlo(100000)
