# MediaCopyer 发布指南

## 快速发布流程

### 1. 更新版本号
```bash
python update_version.py 1.1.0 "修复了重复文件处理bug" "添加了新的文件格式支持"
```

### 2. 自动发布
```bash
python release.py
```

### 3. 在GitHub上完成发布
1. 访问 GitHub Releases 页面
2. 找到新创建的标签
3. 编辑发布说明
4. 上传 `release-v{version}/` 目录中的DMG文件
5. 发布 Release

## 详细说明

### 版本号规则
- 使用语义化版本号：`主版本.次版本.修订版本`
- 主版本：不兼容的API修改
- 次版本：向下兼容的功能性新增
- 修订版本：向下兼容的问题修正

### 文件结构
```
MediaCopyer/
├── version.py              # 版本信息
├── build_app.py           # 构建脚本
├── release.py             # 发布脚本
├── update_version.py      # 版本更新脚本
└── .github/workflows/     # GitHub Actions
    └── release.yml        # 自动构建工作流
```

### 生成的文件
- `MediaCopyer-v{version}.dmg` - macOS安装包
- `release-v{version}/` - 发布资源目录
  - `MediaCopyer-v{version}.dmg` - DMG文件副本
  - `RELEASE_NOTES.md` - 发布说明

### GitHub Actions
推送标签时会自动触发构建：
```bash
git push origin v1.1.0
```

### 手动构建
如果需要手动构建：
```bash
# 激活虚拟环境
source venv/bin/activate

# 构建应用
python build_app.py
```

## 注意事项

1. 确保在发布前测试应用功能
2. 更新README中的下载链接
3. 检查版本历史是否正确更新
4. 确保Git仓库状态干净
5. 推送代码和标签到GitHub

## 故障排除

### 构建失败
- 检查虚拟环境是否激活
- 确保所有依赖已安装
- 检查PyInstaller是否正常工作

### DMG创建失败
- 确保在macOS系统上运行
- 检查hdiutil命令是否可用
- 确保有足够的磁盘空间

### Git操作失败
- 检查Git仓库状态
- 确保有推送权限
- 检查远程仓库连接