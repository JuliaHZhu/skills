#!/bin/bash
# Task Ball Machine 失败 Demo: JSON 手改 vs CLI 正规流程
#
# 用法: cd /home/ubuntu/task-ball-machine && bash /home/ubuntu/wiki/ball-machine/demo.sh

set -e

echo "============================================"
echo "🎯 Ball Machine 失败 Demo"
echo "============================================"
echo ""

# 确保路径
DATA_DIR="${DATA_DIR:-/home/ubuntu/task-ball-machine}"
SCRIPT="/home/ubuntu/.hermes/skills/productivity/task-ball-machine/scripts/ball-machine.py"

cd "$DATA_DIR" || { echo "❌ 无法进入 $DATA_DIR"; exit 1; }

echo "📁 工作目录: $DATA_DIR"
echo ""

# ----------------------------------------
# 首先，恢复到初始状态（和今天抽球后的样子）
# ----------------------------------------
echo "🔄 Step 0: 恢复 state 到今天抽球后的状态..."
cp state.json.bak state.json 2>/dev/null || true

echo ""
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  ❌ 演示 1：错误做法 —— 手改 JSON                             ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo ""

echo "时序：直接用 Python 脚本进攻 state.json..."
echo ""

# 获取当前 morning 的球信息
MORNING_BALL=$(python3 -c "
import json
from pathlib import Path
s = json.loads(Path('state.json').read_text(encoding='utf-8'))
m = s['days']['2026-06-04']['morning']
print(f\"{m['box']}|{m['ball_id']}\")
")
OLD_BOX=${MORNING_BALL%%|*}
OLD_BALL=${MORNING_BALL##*|}

echo "  当前 morning: $OLD_BOX / $OLD_BALL"

# 获取一颗 Rest 球
REST_BALL=$(python3 -c "
import json
from pathlib import Path
s = json.loads(Path('state.json').read_text(encoding='utf-8'))
rest = s['boxes']['Rest']['stack'][0]
print(rest)
")

echo "  准备偷抱的 Rest 球: $REST_BALL"

# 模拟错误做法：手改 JSON
python3 -c "
import json
from pathlib import Path

state = json.loads(Path('state.json').read_text(encoding='utf-8'))

# 获取动态的 ball id
old_box = '$OLD_BOX'
old_ball = '$OLD_BALL'
rest_ball = '$REST_BALL'

# 错误 1：直接抱走一颗 Rest 球
state['days']['2026-06-04']['morning'] = {
    'box': 'Rest',
    'content': '上午休息了',
    'status': 'completed',
    'ball_id': rest_ball
}

# 错误 2：手动调整 used/stack（完全绕过退弹）
# 返回旧球
state['boxes'][old_box]['used'].remove(old_ball)
state['boxes'][old_box]['stack'].append(old_ball)

# 偷新球
state['boxes']['Rest']['stack'].remove(rest_ball)
state['boxes']['Rest']['used'].append(rest_ball)

Path('state.json').write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
print('✅ 手改完成了！统计数字看上去对了。')
"

echo ""
python3 "$SCRIPT" --data-dir . status | grep -E "(Work|Rest|morning)"
echo ""
echo "⚠️ 问题：这颗 $REST_BALL 是从哪里来的？"
echo "→ 答：从 JSON 里“抱走”的。没有摇箱，没有退弹。"
echo ""

# ----------------------------------------
# 恢复，准备正确流程
# ----------------------------------------
echo "🔄 恢复 state.json 到原始状态..."
cp state.json.bak state.json 2>/dev/null || true

echo ""
echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
echo "┃  ✅ 演示 2：正确做法 —— 退弹重抽 + edit + complete              ┃"
echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
echo ""

echo "🎯 目标：morning 需要 🧘 Rest 球，现在是 $OLD_BOX 球"
echo ""

# 循环 redraw 直到抽到 Rest
count=0
while true; do
    count=$((count + 1))
    python3 "$SCRIPT" --data-dir . redraw morning >/dev/null 2>&1 || true

    # 检查当前抽到的盒子
    current_box=$(python3 -c "
import json
from pathlib import Path
state = json.loads(Path('state.json').read_text(encoding='utf-8'))
s = state['days']['2026-06-04'].get('morning')
print(s['box'] if s else 'empty')
" 2>/dev/null || echo "empty")

    echo "  第${count}次 redraw -> $current_box"

    if [ "$current_box" = "Rest" ]; then
        echo "  ✅ 第${count}次抽到了 Rest！"
        break
    fi

    if [ "$count" -gt 20 ]; then
        echo "❌ 超出最大重试次数"
        exit 1
    fi
done

echo ""
echo "📝 修改内容为 '上午休息了'..."
python3 -c "
import sys, importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('bm', '$SCRIPT')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
engine = mod.Engine(Path('$DATA_DIR'))
engine.edit('morning', '上午休息了')
engine.complete('morning')
engine._save()
print('✅ edit + complete 完成')
"

echo ""
echo "📊 最终状态："
python3 "$SCRIPT" --data-dir . status | grep -E "(morning|Work|Rest)"

echo ""
echo "✅ 这次每一次 redraw 都将旧球完整退回箱子，然后随机重新抽取。"
echo "   随机性是真的，数据是实的。"
echo ""

# 恢复原状
cp state.json.bak state.json 2>/dev/null || true
echo "🔄 已恢复原始 state.json"
