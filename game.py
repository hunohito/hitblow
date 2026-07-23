"""ゲームの進行（入力・表示・ループ）。

★ チームで足す機能は **自分の担当の場所**に書く（1機能=1ファイル）。
   下の「ここに足す」場所は3か所（① 開始時 ② 入力コマンド ③ 勝利時）。
   ペアごとに**別の場所**を直すので、並行作業でも衝突しない。
   import も自分の場所の近くに書くこと（ファイル先頭にまとめない＝衝突回避）。
"""

from .core import judge, make_secret


def play(digits=None):
    # 桁数の選択
    print("=== 桁数選択 ===")
    print("  [3] 3桁モード")
    print("  [4] 4桁モード")
    while True:
        digits_input = input("桁数を選択 (3 または 4) > ").strip()
        if digits_input in ('3', '4'):
            digits = int(digits_input)
            break
        print("3 または 4 を入力してください")

    # 難易度の選択と設定
    # easy: 3桁=20回/30s, 4桁=50回/60s
    # medium: 3桁=15回/20s, 4桁=30回/30s
    # hard: 3桁=10回/10s, 4桁=15回/10s
    settings = {
        3: {
            'e': {'tries': 20, 'time': 30},
            'm': {'tries': 15, 'time': 20},
            'h': {'tries': 10, 'time': 10}
        },
        4: {
            'e': {'tries': 50, 'time': 60},
            'm': {'tries': 30, 'time': 30},
            'h': {'tries': 15, 'time': 10}
        }
    }
    
    print("\n=== 難易度選択 ===")
    s = settings[digits]
    print(f"  [e] easy   (制限回数: {s['e']['tries']}回 / 制限時間: {s['e']['time']}秒)")
    print(f"  [m] medium (制限回数: {s['m']['tries']}回 / 制限時間: {s['m']['time']}秒)")
    print(f"  [h] hard   (制限回数: {s['h']['tries']}回 / 制限時間: {s['h']['time']}秒)")
    
    while True:
        diff_input = input("難易度を選択 (e, m, h) > ").strip().lower()
        if diff_input in ('e', 'm', 'h'):
            max_tries = s[diff_input]['tries']
            time_limit = s[diff_input]['time']
            break
        print("e, m, h のいずれかを入力してください")

    secret = make_secret(digits)
    print(f"\nHit & Blow（{digits} 桁・重複なし・難易度: {diff_input.upper()}）")

    # ===== ① 開始時に足す（難易度・あいさつ など）: ここに書く =====
    from .count import show_welcome
    show_welcome(max_tries)
    print(f"制限時間: {time_limit} 秒")

    tries = 0
    while True:
        from .count import print_remaining
        print_remaining(tries, max_tries)
        from .sec import input_with_timeout
        guess = input_with_timeout("予想 > ", time_limit, secret).strip()

        # ===== ② 入力コマンドに足す（ヒント など）: ここに書く（import もここに） =====
        # 例:  from .hint import hint
        #      if guess == "h":
        #          print(hint(secret)); continue

        if len(guess) != digits or not guess.isdigit():
            print(f"{digits} 桁の数字で入力してね")
            continue
        tries += 1
        hit, blow = judge(secret, guess)
        # HitとBlowを強調（Hit: 赤太字, Blow: 青太字）
        print(f"  \033[1;31mHit={hit}\033[0m  \033[1;34mBlow={blow}\033[0m")
        if hit == digits:

            # ===== ③ 勝利時に足す（スコア・履歴 など）: ここに書く =====

            print(f"正解！ {tries} 回で当たり（答え {secret}）")
            break

        from .count import is_game_over
        if is_game_over(tries, max_tries, secret):
            break
