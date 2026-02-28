# Bangumi Rime 词库

适用于 Rime 输入法（雾凇拼音、小狼毫）的动漫、游戏相关扩展词库。

## 包含内容

- 中文动漫角色名、作品名、别名、昵称
- 英文工作室名、游戏名、标签
- 日语假名输入支持（平假名、片假名）
- 日本汉字多音字支持（雫、辻、峠、凪、喰等）
- 约 11.8 万词条

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

在 `rime_ice.dict.yaml` 的 `import_tables` 中添加：

```yaml
import_tables:
  - cn_dicts/8105
  - cn_dicts/base
  - cn_dicts/ext
  - cn_dicts/tencent
  - cn_dicts/others
  - bangumi           # 添加这一行
```

### 小狼毫默认方案 (luna_pinyin)

在 `luna_pinyin.dict.yaml` 的 `import_tables` 中添加：

```yaml
import_tables:
  - bangumi
```

## 重新部署

右键任务栏输入法图标 → 重新部署

## 词库格式

```
词语    拼音    权重
```

权重参考雾凇拼音标准，范围 1-25000。

## 特色功能

### 日语假名输入

支持通过罗马音输入平假名和片假名：
- `na` → な
- `ka` → か
- `shi` → し
- `tsu` → つ

### 日本汉字多音字

| 字 | 读音 | 说明 |
|---|------|------|
| 雫 | na | 汉语读音 nǎ，日本汉字读 shizuku |
| 辻 | shi | 日本汉字，意为十字路口 |
| 峠 | ka | 日本汉字，意为山口 |
| 凪 | zhi | 日本汉字，意为风平浪静 |
| 喰 | can/sun | 日本汉字 |

## 重新生成词库

```bash
pip install pypinyin opencc
python convert_to_rime_final.py
```

## 更新日志

- 2026-03-01: 添加日语假名输入、日本汉字多音字支持，精简英文词条，约 11.8 万词条
- 2026-02-28: 初始版本，约 21 万词条，权重适配雾凇拼音标准
