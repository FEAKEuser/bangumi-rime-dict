# Bangumi Rime 词库

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/release/FEAKEuser/bangumi-rime-dict.svg)](https://github.com/FEAKEuser/bangumi-rime-dict/releases)
[![GitHub stars](https://img.shields.io/github/stars/FEAKEuser/bangumi-rime-dict.svg)](https://github.com/FEAKEuser/bangumi-rime-dict/stargazers)

适用于 Rime 输入法（雾凇拼音、小狼毫）的动漫、游戏相关扩展词库。

## 功能特点

- 中文动漫角色名、作品名、别名、昵称
- 英文工作室名、游戏名、标签
- 日语假名输入支持（平假名、片假名）
- 日本汉字多音字支持（雫、辻、峠、凪、喰等）
- 约 11.8 万词条

**注意**：本词库为扩展词库，不包含常用字词（如"的"、"是"等）。常用字词由基础词库（如雾凇拼音的 `rime_ice`）提供。

## 数据来源

原始数据来自 [Bangumi Archive](https://github.com/bangumi/Archive)

## 平台支持

| 系统 | Rime 前端 | 备注 |
|------|-----------|------|
| Windows | [小狼毫 Weasel](https://github.com/rime/weasel) | ≥ 0.15.0 |
| macOS | [鼠须管 Squirrel](https://github.com/rime/squirrel) | ≥ 1.0.0 |
| Linux | fcitx5-rime / ibus-rime | 需安装 librime-lua |
| Android | [同文 Trime](https://github.com/osfans/trime) | ≥ 3.2.11 |
| Android | [小企鹅 fcitx5-android](https://github.com/fcitx5-android/fcitx5-android) | ≥ 0.0.8 |
| iOS | [仓输入法 Hamster](https://apps.apple.com/cn/app/id6446617683) | 内置雾凇拼音 |

## 安装

### 方法一：直接下载

下载最新的 `bangumi.dict.yaml` 文件，复制到 Rime 配置目录：
- Windows: `%APPDATA%\Rime\`
- macOS: `~/Library/Rime/`
- Linux: `~/.local/share/fcitx5/rime/` 或 `~/.config/ibus/rime/`

### 方法二：克隆仓库

```bash
git clone https://github.com/FEAKEuser/bangumi-rime-dict.git
cp bangumi-rime-dict/bangumi.dict.yaml <Rime配置目录>
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

## 特色功能

### 日语假名输入

支持通过罗马音输入平假名和片假名：

| 输入 | 输出 | 输入 | 输出 |
|------|------|------|------|
| `na` | な | `ka` | か |
| `shi` | し | `tsu` | つ |
| `n` | ん | `ji` | じ |

### 日本汉字多音字

| 字 | 读音 | 说明 |
|---|------|------|
| 雫 | na | 汉语读音 nǎ，日本汉字读 shizuku |
| 辻 | shi | 日本汉字，意为十字路口 |
| 峠 | ka | 日本汉字，意为山口 |
| 凪 | zhi | 日本汉字，意为风平浪静 |
| 喰 | can/sun | 日本汉字 |

### 动漫角色名示例

| 输入 | 输出 |
|------|------|
| `maoyuna` | 猫羽雫 |
| `xiamuna` | 夏目雫 |
| `sabulaina` | 梓布赖纳/梓布莱纳 |

## 常见问题

### Q: 输入后没有显示词库中的词？

A: 请确保：
1. `bangumi.dict.yaml` 文件已放入正确的 Rime 配置目录
2. 已在 `rime_ice.dict.yaml`（或其他方案文件）的 `import_tables` 中添加 `- bangumi`
3. 已重新部署 Rime

### Q: 为什么有些日本名字打不出来？

A: 部分日本名字可能：
1. 只有假名形式，需要用罗马音输入（如 `na` → な）
2. 中文翻译与预期不同，可尝试其他拼音组合
3. 该角色热度较低，被权重过滤掉了

### Q: 如何更新词库？

A: 下载最新的 `bangumi.dict.yaml` 覆盖原文件，然后重新部署即可。

### Q: 词库权重范围是多少？

A: 参考 [雾凇拼音](https://github.com/iDvel/rime-ice) 标准，权重范围 1-25000。

## 词库格式

```
词语<Tab>拼音<Tab>权重
```

示例：
```
猫羽雫	maoyuna	164
Galgame	galgame	24009
```

## 重新生成词库

如需从 Bangumi 原始数据重新生成词库：

```bash
# 1. 下载数据
# 从 https://github.com/bangumi/Archive/releases 下载 character.jsonlines, person.jsonlines, subject.jsonlines

# 2. 安装依赖
pip install pypinyin

# 3. 运行脚本
python convert_to_rime_final.py
```

## 致谢

- [Bangumi Archive](https://github.com/bangumi/Archive) - 数据来源
- [雾凇拼音 rime-ice](https://github.com/iDvel/rime-ice) - 词库格式参考、权重标准
- [pypinyin](https://github.com/mozillazg/python-pinyin) - 汉字转拼音
- [Japanese Surnames](https://github.com/solarkun/Japanese-Surnames) - 日本姓氏列表

## 开源协议

[MIT License](LICENSE)

## 更新日志

详见 [CHANGELOG.md](CHANGELOG.md)