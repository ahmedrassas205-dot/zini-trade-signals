import json
import os
from datetime import datetime

from config import SIGNALS_FILE, COUNTER_FILE, PAIR


def _ensure_files():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("1")

    if not os.path.exists(SIGNALS_FILE):
        with open(SIGNALS_FILE, "w") as f:
            json.dump([], f)


def get_next_signal_id():
    _ensure_files()

    with open(COUNTER_FILE, "r") as f:
        signal_id = int(f.read().strip())

    with open(COUNTER_FILE, "w") as f:
        f.write(str(signal_id + 1))

    return signal_id


def load_signals():
    _ensure_files()

    with open(SIGNALS_FILE, "r") as f:
        return json.load(f)


def save_signals(signals):
    with open(SIGNALS_FILE, "w") as f:
        json.dump(signals, f, indent=4)


def create_signal(signal_type, entry, sl, tp1, tp2, tp3):
    signals = load_signals()

    signal = {
        "id": get_next_signal_id(),
        "pair": PAIR,
        "type": signal_type.upper(),
        "entry": float(entry),
        "sl": float(sl),
        "tp1": float(tp1),
        "tp2": float(tp2),
        "tp3": float(tp3),
        "status": "OPEN",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    signals.append(signal)
    save_signals(signals)

    return signal


def build_message(signal):
    icon = "🟢" if signal["type"] == "BUY" else "🔴"

    return (
        "🚨 Zini Trade Signals\n\n"
        f"#{signal['id']:04d}\n\n"
        f"{icon} {signal['type']} {signal['pair']}\n\n"
        f"💰 Entry: {signal['entry']}\n"
        f"🛑 Stop Loss: {signal['sl']}\n\n"
        f"🎯 TP1: {signal['tp1']}\n"
        f"🎯 TP2: {signal['tp2']}\n"
        f"🎯 TP3: {signal['tp3']}\n\n"
        f"📅 {signal['created_at']}\n"
        f"📊 Status: {signal['status']}"
    )