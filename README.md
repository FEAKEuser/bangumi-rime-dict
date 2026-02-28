# Bangumi Rime 词库

适用于 Rime 输入法（雾凇拼音、小狼毫）的动漫、游戏相关扩展词库。

## 包含内容

- 中文动漫角色名、作品名、别名、昵称
- 英文工作室名、游戏名、标签
- 约 21 万词条

**注意**：本词库为扩展词库，不包含常用字词（如"的"、"是"等）。常用字词由基础词库（如雾凇拼音的 `rime_ice`）提供。

## 数据来源

原始数据来自 [Bangumi Archive](https://github.com/bangumi/Archive)

## 安装

### 方法一：直接下载

下载最新的 `bangumi.dict.yaml` 文件，复制到 Rime 配置目录：
- Windows: `%APPDATA%\Rime\`
- macOS: `~/Library/Rime/`
- Linux: `~/.config/ibus/rime/`

### 方法二：克隆仓库

```bash
git clone https://github.com/FEAKEuser/bangumi-rime-dict.git
cp bangumi-rime-dict/bangumi.dict.yaml ~/.config/ibus/rime/
```

## 配置

### 雾凇拼音 (rime_ice)

在 `rime_ice.custom.yaml` 中添加：

```yaml
patch:
  translator/dictionary: rime_ice
  translator/user_dict: bangumi
  translator/enable_user_dict: true
```

### 小狼毫默认方案 (luna_pinyin)

在 `luna_pinyin.custom.yaml` 中添加：

```yaml
patch:
  translator/dictionary: luna_pinyin
  translator/user_dict: bangumi
```

## 重新部署

右键任务栏输入法图标 → 重新部署

## 词库格式

```
词语    拼音    权重
```

权重参考雾凇拼音标准，范围 1-25000。

## 重新生成词库

```bash
pip install pypinyin opencc
python convert_to_rime_final.py
```

## 更新日志

- 2026-02-28: 初始版本，约 21 万词条，权重适配雾凇拼音标准
