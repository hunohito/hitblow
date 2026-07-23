import sys
import time
import msvcrt

def input_with_timeout(prompt="予想 > ", timeout=10.0):
    """制限時間付きでキーボード入力を受け付け、残り時間を表すバーを表示する。
    
    制限時間を経過した場合はタイムアップを表示してゲームを強制終了する。
    """
    start_time = time.time()
    input_str = ""
    bar_length = 20

    # 画面のチラつき防止のためにカーソルを一時的に非表示にする
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        while True:
            elapsed = time.time() - start_time
            remaining = timeout - elapsed

            # 時間切れ判定
            if remaining <= 0:
                # カーソルを再表示してタイムアップメッセージを出力
                sys.stdout.write("\033[?25h")
                # 行をクリアしてから出力
                sys.stdout.write(f"\r\033[K")
                sys.stdout.flush()
                print(f"\n【タイムアップ！】{timeout}秒が経過しました。ゲームを終了します。")
                sys.exit(0)

            # プログレスバーの比率
            ratio = max(0.0, min(1.0, remaining / timeout))
            filled = int(bar_length * ratio)

            # 残り時間に応じた色分け (緑 -> 黄 -> 赤)
            if ratio > 0.5:
                color = "\033[32m"  # 緑
            elif ratio > 0.2:
                color = "\033[33m"  # 黄
            else:
                color = "\033[31m"  # 赤
            reset = "\033[0m"

            # バーの生成 (cp932エンコード対応のため、■ と □ を使用)
            bar = "■" * filled + "□" * (bar_length - filled)

            # 入力中のカーソル点滅エフェクト
            cursor = "_" if int(time.time() * 2) % 2 == 0 else " "

            # 画面に出力 (\r で行頭に戻り、\033[K で行末までクリア)
            sys.stdout.write(f"\r{color}[{bar}] 残り {remaining:4.1f}秒{reset} | {prompt}{input_str}{cursor}\033[K")
            sys.stdout.flush()

            # キー入力があるか確認
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                if ch in ('\r', '\n'):  # Enterキーで入力確定
                    break
                elif ch == '\x08':  # Backspaceキー
                    if len(input_str) > 0:
                        input_str = input_str[:-1]
                elif ch == '\x03':  # Ctrl+Cで中断
                    sys.stdout.write("\033[?25h\n")
                    sys.stdout.flush()
                    print("\nゲームを中断しました。")
                    sys.exit(0)
                elif ch.isprintable():  # 入力可能な文字を追加
                    input_str += ch

            # CPU負荷軽減のためのスリープ
            time.sleep(0.05)

    finally:
        # 確実にカーソルを再表示させる
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()

    return input_str
