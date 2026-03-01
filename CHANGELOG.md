# Changelog

All notable changes to this project will be documented in this file.

## [2026-03-01]

### Added
- Japanese kana input support (hiragana and katakana)
  - `na` → な, `ka` → か, `shi` → し, etc.
- Japanese kanji polyphonic character support
  - 雫 (na), 辻 (shi), 峠 (ka), 凪 (zhi), 喰 (can/sun)
- Kana to romaji conversion for untranslated Japanese names

### Changed
- Reduced English entries by 60% (removed 2707 low-weight entries, kept 1778)
- Fixed dictionary import configuration (use `import_tables` instead of `user_dict`)
- Updated version to 2026-03-01

### Fixed
- Dictionary not loading correctly due to wrong configuration method

## [2026-02-28]

### Added
- Initial release
- Chinese anime/game character names, work names, aliases, nicknames
- English studio names, game names, tags
- Name splitting for easier searching (surname + given name)
- Japanese to Chinese name translations (~50k entries)
- Weight scaling to Rime standard (1-25000 range)
- About 210k entries