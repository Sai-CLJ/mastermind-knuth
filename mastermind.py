import itertools
import random
from collections import defaultdict

# 计算反馈：黑（位置颜色正确），白（颜色正确位置错误）
def get_feedback(guess, code):
    black = sum(g == c for g, c in zip(guess, code))
    guess_counts = {x: guess.count(x) for x in set(guess)}
    code_counts = {x: code.count(x) for x in set(code)}
    white = sum(min(guess_counts.get(x, 0), code_counts.get(x, 0)) for x in guess_counts) - black
    return black, white

# 生成所有可能的组合（6种颜色，4个位置）
def all_codes():
    colors = range(1, 7)
    return list(itertools.product(colors, repeat=4))

# Knuth 的最优解法
def knuth_solver(secret):
    possible = all_codes()
    candidates = possible[:]
    guesses = []
    guess = (1, 1, 2, 2)  # Knuth 推荐首猜

    while True:
        guesses.append(guess)
        feedback = get_feedback(guess, secret)
        print(f"猜测: {guess}, 反馈: {feedback}")

        if feedback == (4, 0):
            print(f"✅ 找到答案，共 {len(guesses)} 步")
            return guesses

        possible = [p for p in possible if get_feedback(guess, p) == feedback]

        score_map = {}
        for g in candidates:
            partitions = defaultdict(int)
            for p in possible:
                fb = get_feedback(g, p)
                partitions[fb] += 1
            worst_case = max(partitions.values())
            score_map[g] = worst_case

        min_score = min(score_map.values())
        next_guesses = [g for g in score_map if score_map[g] == min_score]
        guess = next((g for g in next_guesses if g in possible), next_guesses[0])

# 自动模式
def auto_mode():
    secret = random.choice(all_codes())
    print(f"🎲 隐藏密码（内部使用）: {secret}\n")
    guesses = knuth_solver(secret)
    print("\n完整猜测序列:")
    for i, g in enumerate(guesses, 1):
        print(f"第 {i} 步: {g}")

# 交互模式
def knuth_interactive():
    possible = all_codes()
    candidates = possible[:]
    guess = (1, 1, 2, 2)
    step = 1

    print("\n🧩 Mastermind 交互模式")
    print("颜色用数字 1-6 表示，共 4 个位置。")
    print("输入反馈：黑 白 (例如 '2 1')。输入 'exit' 退出。\n")

    while True:
        print(f"\n第 {step} 步猜测: {guess}")
        fb_input = input("请输入反馈 (黑 白): ").strip()
        if fb_input.lower() == "exit":
            print("已退出。")
            break
        try:
            black, white = map(int, fb_input.split())
        except:
            print("⚠️ 输入格式错误，请输入类似 '2 1'")
            continue

        if (black, white) == (4, 0):
            print(f"🎉 解码成功！答案是 {guess}，共 {step} 步。")
            break

        possible = [p for p in possible if get_feedback(guess, p) == (black, white)]
        if not possible:
            print("❌ 没有可能的解，请检查反馈是否输入正确！")
            break

        score_map = {}
        for g in candidates:
            partitions = defaultdict(int)
            for p in possible:
                fb = get_feedback(g, p)
                partitions[fb] += 1
            worst_case = max(partitions.values())
            score_map[g] = worst_case

        min_score = min(score_map.values())
        next_guesses = [g for g in score_map if score_map[g] == min_score]
        guess = next((g for g in next_guesses if g in possible), next_guesses[0])
        step += 1

# 主菜单
def main():
    print("=== Mastermind (Knuth 解法) ===")
    print("1. 自动模式（电脑随机出题并解码）")
    print("2. 交互模式（你来出题，手动输入反馈）")
    print("0. 退出")
    choice = input("请选择模式: ").strip()
    if choice == "1":
        auto_mode()
    elif choice == "2":
        knuth_interactive()
    else:
        print("退出程序。")

if __name__ == "__main__":
    main()
