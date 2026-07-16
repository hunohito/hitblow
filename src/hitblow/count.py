MAX_TRIES = 10

def show_welcome():
    print(f"入力制限回数: {MAX_TRIES} 回")

def print_remaining(tries):
    print(f"残り回数: {MAX_TRIES - tries} 回")

def is_game_over(tries, secret):
    if tries >= MAX_TRIES:
        print(f"残念！制限回数（{MAX_TRIES} 回）に達しました。ゲームオーバーです。（答え {secret}）")
        return True
    return False
