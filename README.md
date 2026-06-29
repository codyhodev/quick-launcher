# quick-launcher

Linux X11 系统托盘应用，通过静态 YAML 配置快速启动应用程序或脚本。

## 安装

```bash
uv tool install .
```

或者直接运行：`python -m quick_launcher`

## 配置

路径：`~/.config/quick-launcher/config.yaml`

```yaml
terminal_cmd: gnome-terminal
font_size: 14

launchers:
  - name: Browser
    command: firefox

  - type: separator

  - name: Dev Tools
    items:
      - name: Editor
        command: code
      - name: htop
        command: htop
        terminal: true
```

### 启动器字段

| 字段 | 说明 |
|------|------|
| `name` | 菜单显示名称 |
| `command` | 要执行的命令 |
| `terminal` | 是否在终端中运行（默认 `false`） |
| `type` | `separator` 插入分隔线 |
| `items` | 子菜单条目（嵌套） |

## 运行

```bash
uv run quick-launcher
```

## 开发

```bash
uv sync
QT_QPA_PLATFORM=offscreen uv run pytest
```
