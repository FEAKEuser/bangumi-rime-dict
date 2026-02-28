# Bangumi Rime 词库

适用于 Rime 输入法（小狼毫、雾凇拼音）的动漫、游戏相关词库。

## 包含内容

- 中文动漫角色名、作品名、别名、昵称
- 英文工作室名、游戏名、标签
- 约 21 万词条

## 数据来源

原始数据来自 [Bangumi Archive](https://github.com/bangumi/Archive)

## 使用方法

### 1. 下载词库

下载最新的 `bangumi.dict.yaml` 文件。

### 2. 安装

复制 `bangumi.dict.yaml` 到 Rime 配置目录：
- Windows: `%APPDATA%\Rime\`
- macOS: `~/Library/Rime/`
- Linux: `~/.config/ibus/rime/`

### 3. 配置

在 `rime_ice.custom.yaml`（雾凇拼音）中添加：

```yaml
patch:
  translator/dictionary: rime_ice
  translator/user_dict: bangumi
  translator/enable_user_dict: true
```

或者在 `luna_pinyin.custom.yaml`（小狼毫默认）中添加：

```yaml
patch:
  translator/dictionary: luna_pinyin
  translator/user_dict: bangumi
```

### 4. 重新部署

右键任务栏输入法图标 → 重新部署

## 词库格式

```
词语    拼音    权重
```

示例：
```
命运石之门    mingyunshizhimen    6933
Fate    fate    81186
Galgame    galgame    480191
```

## 重新生成词库

如果需要从原始数据重新生成词库，运行：

```bash
pip install pypinyin opencc
python convert_to_rime_v4.py
```

## 更新日志

- 2026-02-28: 初始版本，约 21 万词条
