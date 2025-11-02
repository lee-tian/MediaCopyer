#!/bin/bash
# MediaCopyer 快速发布脚本 (Unix/macOS)

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 显示帮助
show_help() {
    echo "MediaCopyer 快速发布脚本"
    echo "=========================="
    echo
    echo "用法:"
    echo "  ./scripts/platform/release.sh <命令> [参数...]"
    echo
    echo "命令:"
    echo "  build                    仅构建应用程序"
    echo "  patch [changes...]       发布补丁版本 (x.y.Z)"
    echo "  minor [changes...]       发布次版本 (x.Y.z)"
    echo "  major [changes...]       发布主版本 (X.y.z)"
    echo "  release <version> [changes...]  发布指定版本"
    echo "  version                  显示当前版本"
    echo "  clean                    清理构建文件"
    echo
    echo "示例:"
    echo "  ./scripts/platform/release.sh build"
    echo "  ./scripts/platform/release.sh patch '修复重要bug'"
    echo "  ./scripts/platform/release.sh minor '添加新功能'"
    echo "  ./scripts/platform/release.sh release 1.2.0 '重大更新'"
}

# 检查Python环境
check_python() {
    if ! command -v python &> /dev/null; then
        print_error "Python 未安装或不在 PATH 中"
        exit 1
    fi
    
    if [ ! -f "scripts/utils/make.py" ]; then
        print_error "未找到 make.py 脚本"
        exit 1
    fi
}

# 主函数
main() {
    if [ $# -eq 0 ] || [ "$1" = "help" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_help
        exit 0
    fi
    
    check_python
    
    print_info "执行命令: python scripts/utils/make.py $*"
    python scripts/utils/make.py "$@"
    
    if [ $? -eq 0 ]; then
        print_success "操作完成!"
    else
        print_error "操作失败!"
        exit 1
    fi
}

# 使脚本可执行
chmod +x "$0" 2>/dev/null || true

main "$@"