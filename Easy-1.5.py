import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import time
import random
import string
import os

# メモリと状態の管理
variables = {}
output_widget = None
SAVE_FILE_NAME = "my_code.txt"  # コードを保存するファイル名

# --- 多言語メッセージの設定 ---
LANG_TEXTS = {
    "日本語": {
        "title": "マスター自作言語・ゲームエディタ", 
        "label": "コードを入力してください:", 
        "btn": "▶ 実行する", 
        "output": "実行結果 / ログ:",
        "btn_save": "[保存]",
        "btn_load": "[読込]",
        "btn_close": "❌ 終了",
        "sample": "保存 得点 = 0\n得点 得点\n\n表示 敵が現れた！\nカラー 赤\nバイブ 2\nHP 40\n\n待つ 1\n表示 会心の一撃！敵を倒した！\nカラー 緑\n計算 得点 = 得点 + 100\n得点 得点\nHP 100\n\n警告 ゲームクリア！"
    },
    "English": {
        "title": "Master Game Editor", 
        "label": "Enter Code:", 
        "btn": "▶ RUN", 
        "output": "Output / Log:",
        "btn_save": "[Save]",
        "btn_load": "[Load]",
        "btn_close": "❌ CLOSE",
        "sample": "let score = 0\nscore score\n\nprint Enemy appeared!\ncolor red\nvibe 2\nhp 40\n\nwait 1\nprint Critical hit!\ncolor green\ncalc score = score + 100\nscore score\nhp 100\n\nalert Game Clear!"
    }
}

# --- 画面（GUI）の構築 ---
root = tk.Tk()
root.title("My Master Language App")
root.geometry("420x680") # ゲージ追加に伴い少し縦幅を拡張
APP_FONT = ("Helvetica", 11)

# --- 【新設】ゲーム表示用ヘッダーパネル ---
frame_game_ui = tk.LabelFrame(root, text=" ゲームステータス (Game UI) ", font=("Helvetica", 9, "bold"), fg="#1565c0")
frame_game_ui.pack(fill="x", padx=10, pady=5)

# HPゲージのラベルとバー
label_hp_title = tk.Label(frame_game_ui, text="HP:", font=("Helvetica", 10, "bold"))
label_hp_title.pack(side="left", padx=(5, 2))

progress_hp = ttk.Progressbar(frame_game_ui, orient="horizontal", length=150, mode="determinate")
progress_hp.pack(side="left", padx=5, pady=5)
progress_hp["value"] = 100 # 初期値は満タン

# 得点表示ラベル
label_score = tk.Label(frame_game_ui, text="SCORE: 0", font=("Helvetica", 11, "bold"), fg="#e65100")
label_score.pack(side="right", padx=10)


# 変数の値または数値を評価する補助関数
def evaluate_expression(expr):
    expr = expr.strip()
    if expr in variables:
        return variables[expr]
    try:
        if "." in expr:
            return float(expr)
        return int(expr)
    except ValueError:
        return expr

# 条件式の評価関数
def evaluate_condition(condition_str):
    operators = ["==", "!=", ">=", "<=", ">", "<"]
    for op in operators:
        if op in condition_str:
            left_str, right_str = condition_str.split(op, 1)
            left_val = evaluate_expression(left_str)
            right_val = evaluate_expression(right_str)
            
            try:
                left_val, right_val = float(left_val), float(right_val)
            except:
                left_val, right_val = str(left_val), str(right_val)
                
            if op == "==": return left_val == right_val
            if op == "!=": return left_val != right_val
            if op == ">=": return left_val >= right_val
            if op == "<=": return left_val <= right_val
            if op == ">": return left_val > right_val
            if op == "<": return left_val < right_val
    return False

# ファイル保存
def press_save_file():
    user_code = code_entry.get("1.0", tk.END).strip()
    try:
        with open(SAVE_FILE_NAME, "w", encoding="utf-8") as f:
            f.write(user_code)
        lang = lang_combo.get()
        messagebox.showinfo("成功" if lang == "日本語" else "Success", "Saved!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ファイル読み込み
def press_load_file():
    if not os.path.exists(SAVE_FILE_NAME):
        return
    try:
        with open(SAVE_FILE_NAME, "r", encoding="utf-8") as f:
            content = f.read()
        code_entry.delete("1.0", tk.END)
        code_entry.insert("1.0", content)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def press_close_app():
    root.destroy()

def on_language_change(event=None):
    lang = lang_combo.get()
    text = LANG_TEXTS[lang]
    root.title(text["title"])
    label_code.config(text=text["label"])
    btn_run.config(text=text["btn"])
    label_out.config(text=text["output"])
    btn_save_file.config(text=text["btn_save"])
    btn_load_file.config(text=text["btn_load"])
    btn_close.config(text=text["btn_close"])
    code_entry.delete("1.0", tk.END)
    code_entry.insert("1.0", text["sample"])

# レイアウト
frame_top = tk.Frame(root)
frame_top.pack(fill="x", padx=10, pady=5)

lang_combo = ttk.Combobox(frame_top, values=list(LANG_TEXTS.keys()), state="readonly", width=8, font=APP_FONT)
lang_combo.set("日本語")
lang_combo.pack(side="left")
lang_combo.bind("<<ComboboxSelected>>", on_language_change)

btn_save_file = tk.Button(frame_top, text="", font=("Helvetica", 9), bg="#e1f5fe", command=press_save_file)
btn_save_file.pack(side="left", padx=5)

btn_load_file = tk.Button(frame_top, text="", font=("Helvetica", 9), bg="#efebe9", command=press_load_file)
btn_load_file.pack(side="left", padx=5)

label_code = tk.Label(root, text="", anchor="w", font=APP_FONT)
label_code.pack(fill="x", padx=10, pady=(5, 2))
code_entry = tk.Text(root, height=12, font=APP_FONT)
code_entry.pack(fill="both", expand=True, padx=10, pady=2)


# --- 自作言語の処理エンジン ---
def run_my_language(code):
    global variables
    lines = code.split("\n")
    outputs = []
    if_stack = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 条件分岐制御
        if line.startswith("もし ") or line.startswith("if "):
            _, cond_str = line.split(" ", 1)
            is_true = evaluate_condition(cond_str)
            parent_executing = if_stack[-1]["executing"] if if_stack else True
            current_exec = parent_executing and is_true
            if_stack.append({"executing": current_exec, "done": current_exec})
            continue

        if line.startswith("それとも ") or line.startswith("elif "):
            _, cond_str = line.split(" ", 1)
            if if_stack:
                parent_executing = if_stack[:-1][-1]["executing"] if len(if_stack) > 1 else True
                if parent_executing and not if_stack[-1]["done"]:
                    is_true = evaluate_condition(cond_str)
                    if_stack[-1]["executing"] = is_true
                    if is_true: if_stack[-1]["done"] = True
                else:
                    if_stack[-1]["executing"] = False
            continue

        if line in ["その他", "else"]:
            if if_stack:
                parent_executing = if_stack[:-1][-1]["executing"] if len(if_stack) > 1 else True
                if parent_executing and not if_stack[-1]["done"]:
                    if_stack[-1]["executing"] = True
                    if_stack[-1]["done"] = True
                else:
                    if_stack[-1]["executing"] = False
            continue

        if line in ["終わり", "endif"]:
            if if_stack: if_stack.pop()
            continue

        if if_stack and not if_stack[-1]["executing"]:
            continue

        # --- 【新機能 1】 HPゲージ操作コマンド (例: HP 50 / hp 100) ---
        if any(line.startswith(cmd + " ") for cmd in ["HP", "hp"]):
            _, val_str = line.split(" ", 1)
            hp_val = int(evaluate_expression(val_str.strip()))
            # 0〜100の間に制限して反映
            hp_val = max(0, min(100, hp_val))
            progress_hp["value"] = hp_val
            root.update()
            outputs.append(f"[GAME UI] HP updated to {hp_val}%")
            continue

        # --- 【新機能 2】 得点表示コマンド (例: 得点 スコア変数 / score score_var) ---
        if any(line.startswith(cmd + " ") for cmd in ["得点", "score"]):
            _, val_str = line.split(" ", 1)
            score_val = evaluate_expression(val_str.strip())
            label_score.config(text=f"SCORE: {score_val}")
            root.update()
            outputs.append(f"[GAME UI] Score updated to {score_val}")
            continue

        # --- 【新機能 3】 BGM再生コマンド (例: 音楽 bgm.wav / bgm bgm.mp3) ---
        if any(line.startswith(cmd + " ") for cmd in ["音楽", "bgm"]):
            _, file_str = line.split(" ", 1)
            filename = str(evaluate_expression(file_str.strip()))
            outputs.append(f"[BGM] Play request: {filename}")
            
            # Windows標準の非同期音声再生を試みる
            if os.name == "nt":
                import winsound
                try:
                    # SND_ASYNCでループ、SND_FILENAMEでファイル指定
                    winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
                except:
                    outputs.append(f"[BGM_ERROR] Could not play {filename} (Ensure it is a .wav file)")
            else:
                # Mac/Linuxの場合は簡易的にOSのコマンド呼び出し
                outputs.append("[BGM] OS standard sound play triggered")
            continue

        # --- 【新機能 4】 BGM停止コマンド (音楽停止 / bgm_stop) ---
        if line in ["音楽停止", "bgm_stop"]:
            if os.name == "nt":
                import winsound
                winsound.PlaySound(None, winsound.SND_PURGE) # 再生中の音を消去
            outputs.append("[BGM] Stopped all music")
            continue

        # 計算
        if any(line.startswith(cmd + " ") for cmd in ["計算", "calc"]):
            _, rest = line.split(" ", 1)
            var_name, expr_str = rest.split("=", 1)
            parsed_expr = expr_str.strip()
            for v_name, v_val in variables.items():
                parsed_expr = parsed_expr.replace(v_name, str(v_val))
            try:
                if all(c in "0123456789+-*/(). " for c in parsed_expr):
                    calc_res = eval(parsed_expr)
                    variables[var_name.strip()] = calc_res
                    outputs.append(f"[CALC] {var_name.strip()} = {calc_res}")
            except:
                outputs.append("[CALC_ERROR] Failed")
            continue

        # カラー
        if any(line.startswith(cmd + " ") for cmd in ["カラー", "color"]):
            _, color_name = line.split(" ", 1)
            outputs.append(f"[COLOR] Background -> {color_name.strip()}")
            continue

        # バイブ
        if any(line.startswith(cmd + " ") for cmd in ["バイブ", "vibe"]):
            _, count_str = line.split(" ", 1)
            count = int(evaluate_expression(count_str.strip()))
            orig_bg = output_widget.cget("bg")
            for _ in range(min(count, 10)):
                output_widget.config(bg="#ff8a80"); root.update(); time.sleep(0.06)
                output_widget.config(bg=orig_bg); root.update(); time.sleep(0.06)
            outputs.append(f"[VIBE] Shook {count} times")
            continue

        # その他の既存コマンド
        if line in ["消去", "clear"]: outputs = ["CLEAR_SIGNAL"]; continue
        if line in ["音", "beep"]: root.bell(); outputs.append("[BEEP]"); continue
        if line in ["アプリ終了", "close"]: root.destroy(); return "CLOSED"
        
        if any(line.startswith(cmd + " ") for cmd in ["警告", "alert"]):
            _, msg = line.split(" ", 1)
            msg_val = str(evaluate_expression(msg.strip()))
            messagebox.showwarning("Alert", msg_val)
            continue
        if any(line.startswith(cmd + " ") for cmd in ["アニメ", "type"]):
            _, msg = line.split(" ", 1)
            outputs.append(f"__TYPE_EFFECT__:{str(evaluate_expression(msg.strip()))}")
            continue
        if any(line.startswith(cmd + " ") for cmd in ["待つ", "wait"]):
            _, sec_str = line.split(" ", 1)
            time.sleep(float(evaluate_expression(sec_str.strip())))
            continue
        if any(line.startswith(cmd + " ") for cmd in ["表示", "print"]):
            _, expr = line.split(" ", 1)
            outputs.append(str(evaluate_expression(expr.strip())))
            continue

    return outputs

def animate_text(target_widget, text_line, delay=0.04):
    for char in text_line:
        target_widget.insert(tk.END, char); target_widget.see(tk.END); target_widget.update(); time.sleep(delay)
    target_widget.insert(tk.END, "\n")

def press_run_code():
    user_code = code_entry.get("1.0", tk.END)
    global variables
    variables = {}
    
    # 実行ごとにUIを初期化
    progress_hp["value"] = 100
    label_score.config(text="SCORE: 0")
    
    results = run_my_language(user_code)
    if results == "CLOSED": return
        
    output_widget.config(state="normal")
    output_widget.delete("1.0", tk.END)
    
    for res in results:
        if res.startswith("__TYPE_EFFECT__:"):
            animate_text(output_widget, res.replace("__TYPE_EFFECT__:", ""))
        else:
            output_widget.insert(tk.END, res + "\n")
    output_widget.see(tk.END)
    output_widget.config(state="disabled")

# 下段UI
btn_run = tk.Button(root, text="", font=("Helvetica", 12, "bold"), bg="#c8e6c9", fg="#1b5e20", command=press_run_code)
btn_run.pack(fill="x", padx=10, pady=5)

label_out = tk.Label(root, text="", anchor="w", font=APP_FONT)
label_out.pack(fill="x", padx=10, pady=(5, 2))

output_widget = tk.Text(root, height=6, font=APP_FONT, bg="#fafafa", state="disabled")
output_widget.pack(fill="both", expand=True, padx=10, pady=(2, 10))

btn_close = tk.Button(root, text="", font=("Helvetica", 10), bg="#ffcdd2", command=press_close_app)
btn_close.pack(side="right", padx=10, pady=(0, 10))

on_language_change()
root.mainloop()
