#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单调试脚本 - 找出发布卡住的原因
"""

import subprocess
import sys
import time

def test_command(cmd, description):
    """测试单个命令"""
    print(f"测试: {description}")
    print(f"命令: {cmd}")
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        end_time = time.time()
        
        print(f"耗时: {end_time - start_time:.2f}秒")
        print(f"返回码: {result.returncode}")
        
        if result.stdout:
            print(f"输出: {result.stdout[:200]}...")
        if result.stderr:
            print(f"错误: {result.stderr[:200]}...")
        
        print("-" * 40)
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ 命令超时 (30秒)")
        print("-" * 40)
        return False
    except Exception as e:
        print(f"❌ 异常: {e}")
        print("-" * 40)
        return False

def main():
    print("🔍 简单发布调试")
    print("=" * 40)
    
    # 测试基本命令
    commands = [
        ("git --version", "Git版本"),
        ("gh --version", "GitHub CLI版本"),
        ("gh auth status", "GitHub认证状态"),
        ("git status --porcelain", "Git状态"),
        ("git branch --show-current", "当前分支"),
        ("python --version", "Python版本"),
        ("ls -la build_app.py", "构建脚本检查"),
    ]
    
    for cmd, desc in commands:
        if not test_command(cmd, desc):
            print(f"❌ {desc} 失败，可能是卡住的原因")
            break
    else:
        print("✅ 所有基本命令都正常")
        
        # 测试可能卡住的操作
        print("\n测试可能卡住的操作:")
        
        risky_commands = [
            ("git push --dry-run", "Git推送测试"),
            ("gh repo view", "GitHub仓库访问"),
        ]
        
        for cmd, desc in risky_commands:
            print(f"\n⚠️ 测试可能卡住的命令: {desc}")
            if not test_command(cmd, desc):
                print(f"❌ 找到问题: {desc}")
                break

if __name__ == '__main__':
    main()