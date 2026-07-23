def show_welcome(max_tries):
    print(f"入力制限回数: {max_tries} 回")

def print_remaining(tries, max_tries):
    print(f"残り回数: {max_tries - tries} 回")

def is_game_over(tries, max_tries, secret):
    if tries >= max_tries:
        print(f"残念！制限回数（{max_tries} 回）に達しました。ゲームオーバーです。（答え {secret}）")
        return True
    return False
