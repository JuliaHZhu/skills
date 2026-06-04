# Unicode 双转义陷阱 — 写含 Emoji 的 Python 脚本

> 在使用 Hermes `write_file` 工具写入含 emoji 的 Python 脚本时，emoji 可能被双转义成 `\ud83c\udf05`，导致运行时 UnicodeEncodeError。

## 问题现象

用 `write_file` 写入以下内容到 `.py` 文件：

```python
DISPLAY = {
    "morning": "🌅 morning",
    "afternoon": "🌅 afternoon",
}
```

实际写入文件的内容变成：

```python
DISPLAY = {
    "morning": "\\ud83c\\udf05 morning",   # 错误！双转义
    "afternoon": "\\ud83c\\udf05 afternoon",
}
```

运行时 `print(DISPLAY["morning"])` 输出：

```
\ud83c\udf05 morning
```

而不是预期的 emoji。更糟糕的是，如果通过 `json.dumps` 写入这个字典到 JSON，运行时可能抛出 `UnicodeEncodeError`：

```
UnicodeEncodeError: 'utf-8' codec can't encode characters in position ...
```

因为 `\ud83c` 和 `\udf05` 是 surrogate pair 的文本表示，不是合法的 UTF-8 字节序列。

## 根因分析

Hermes 的 `write_file` 工具在处理含 emoji 的内容时，可能将 emoji 字符转义为 surrogate pair 的文本表示（`\uXXXX` 形式）。这种双转义在 JSON 序列化时特别容易出问题。

## 解决方案

### 方法 A：用 Python 脚本生成文件（推荐）

不用 `write_file` 直接写含 emoji 的 Python 文件，而是用 `execute_code` 运行一段 Python 代码来生成：

```python
from pathlib import Path

SCRIPT = r'''#!/usr/bin/env python3
# ... 脚本内容，其中含有真实 emoji ...
DISPLAY = {
    "morning": "🌅 morning",
    "afternoon": "🌅 afternoon",
}
# ... 其余代码 ...
'''

Path('/path/to/ball-machine.py').write_text(SCRIPT, encoding='utf-8')
```

关键点：`r'''...'''` raw string + `write_text(encoding='utf-8')` 确保 emoji 按原样写入。

### 方法 B：用 json.dumps 保护 emoji

如果必须用 `write_file`，先用 Python 将内容正确编码：

```python
import json
content = json.dumps({"morning": "🌅 morning"}, ensure_ascii=False)
# content 现在包含正确的 UTF-8 emoji
```

然后将 `content` 作为 `write_file` 的参数。

### 方法 C：写入后验证

写入文件后，立即运行简单验证：

```bash
python -c "print('🌅')"
```

如果输出是 emoji 而不是 `\ud83c\udf05`，则说明写入正确。

## 预防措施

1. 在任何含 emoji 的文件写入后，用 `read_file` 检查前 5 行确认 emoji 未被转义
2. 优先使用 `execute_code` 生成含 emoji 的脚本，而非 `write_file` 直写
3. 如果用 `write_file`，避免在内容中直接写入 emoji，改用 ASCII fallback 或后续动态替换
