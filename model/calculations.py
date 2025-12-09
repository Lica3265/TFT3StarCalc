import math
import random
from .data import DROP_RATES, COPIES_PER_CHAMP, NUM_CHAMPS_PER_TIER,COST_TIERS
# 計算下一次抽到特定棋子的期望抽數
def expected_slots_to_next(remaining, tier_pool, p_tier):
    """計算下一次抽到特定棋子的期望抽數"""
    if remaining <= 0:
        return float('inf')
    p_specific = p_tier * (remaining / tier_pool)
    return 1 / p_specific if p_specific > 0 else float('inf')

# 計算期望金幣數（支援不同目標張數）
def calculate_expected_gold(level, cost, owned, outside, outside_other=0, target_copies=9):
    """計算到指定張數的期望金幣數，預設目標為 9 張（3 星）"""
    if owned >= target_copies:
        return 0
    initial_copies = COPIES_PER_CHAMP[cost]
    remaining = max(0, initial_copies - owned - outside)
    needed = target_copies - owned
    if remaining < needed:
        return float('inf')

    num_champs = NUM_CHAMPS_PER_TIER[cost]
    full_tier_pool = num_champs * initial_copies
    current_tier_pool = max(0, full_tier_pool - outside - outside_other - owned)

    p_tier = DROP_RATES.get(level, [0]*5)[cost-1]

    expected_slots = 0
    for _ in range(needed):
        if remaining <= 0:
            return float('inf')
        p_specific = p_tier * (remaining / current_tier_pool) if current_tier_pool > 0 else 0
        expected_slots += 1 / p_specific if p_specific > 0 else float('inf')
        remaining -= 1
        current_tier_pool -= 1

    slots_per_roll = 5
    expected_rolls = expected_slots / slots_per_roll
    gold_per_roll = 2
    return math.ceil(expected_rolls * gold_per_roll)

# 計算到 2 星（3 張）的期望金幣
def calculate_expected_gold_to_2star(level, cost, owned, outside, outside_other=0):
    return calculate_expected_gold(level, cost, owned, outside, outside_other, target_copies=3)

# 計算升級成本
def calculate_upgrade_cost(xp_to_next):
    """計算升級所需的金幣成本"""
    if xp_to_next <= 0:
        return 0
    buys_needed = math.ceil(xp_to_next / 4)
    return buys_needed * 4

# 模擬到指定張數的累積機率
def simulate_probability(level, cost, owned, outside, outside_other=0, max_gold=100, trials=1000, target_copies=9):
    """使用 Monte Carlo 模擬計算到指定張數的累積機率，預設目標為 9 張（3 星）"""
    initial_copies = COPIES_PER_CHAMP[cost]
    num_champs = NUM_CHAMPS_PER_TIER[cost]
    full_tier_pool = num_champs * initial_copies
    p_tier = DROP_RATES.get(level, [0] * 5)[cost - 1]

    gold_steps = list(range(0, max_gold + 1, 2))
    probabilities = []

    for gold in gold_steps:
        rolls = gold // 2
        slots = rolls * 5
        success = 0
        for _ in range(trials):
            current_owned = owned
            current_outside = outside
            remaining = initial_copies - current_owned - current_outside
            current_pool = max(0, full_tier_pool - current_outside - outside_other)
            for _ in range(slots):
                if current_pool <= 0 or current_owned >= target_copies:
                    break
                if remaining <= 0:
                    break
                p_specific = p_tier * (remaining / current_pool) if current_pool > 0 else 0
                if random.random() < p_specific:
                    current_owned += 1
                    remaining -= 1
                    current_pool -= 1
                else:
                    current_pool -= 1
                if current_owned >= target_copies:
                    success += 1
                    break
        probabilities.append(success / trials * 100)

    return gold_steps, probabilities

# 計算每個費用階層的總張數
def get_total_copies_per_tier():
    """計算每個費用階層的總棋子張數"""
    return {cost: NUM_CHAMPS_PER_TIER[cost] * COPIES_PER_CHAMP[cost] for cost in COST_TIERS}
