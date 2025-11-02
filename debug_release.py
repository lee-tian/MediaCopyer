#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
调试发布脚本 - 用于诊断发布过程中的问题
"""

import os
import sys
import subprocess
import time
import signal
from version import get_version, get_dmg_name

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("命令执行超时")

def run_command_with_timeout(cmd, description="", timeout=60, shell=True):
    """运行命令并设置超时"""
    print(f"🔄 {description}...")
    print(f"📝 执行命令: {cmd}")
    
    # 设置超时信号
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    
    try:
        start_time = time.time()
        
        if shell:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # 取消超时
        signal.alarm(0)
        
        if result.returncode == 0:
            print(f"✅ {description}完成 (耗时: {duration:.2f}秒)")
            if result.stdout.strip():
                print(f"📤 输出: {result.stdout.strip()[:200]}...")
            return True, result.stdout
        else:
            print(f"❌ {description}失败 (耗时: {duration:.2f}秒)")
            print(f"❌ 错误: {result.stderr}")
            return False, result.stderr
            
    except TimeoutError:
        print(f"⏰ {description}超时 (>{timeout}秒)")
        return False, "命令执行超时"
    except Exception as e:
        signal.alarm(0)  # 确保取消超时
        print(f"❌ {description}异常: {e}")
        return False, str(e)

def test_individual_steps():
    """逐步测试每个发布步骤"""
    print("🔍 逐步测试发布流程...")
    
    # 步骤1: 检查git状态
    success, output = run_command_with_timeout(
        "git status --porcelain", 
        "检查Git状态", 
        timeout=10
    )
    if not success:
        return False
    
    # 步骤2: 检查GitHub CLI
    success, output = run_command_with_timeout(
        "gh --version", 
        "检查GitHub CLI", 
        timeout=10
    )
    if not success:
        return False
    
    # 步骤3: 检查GitHub认证
    success, output = run_command_with_timeout(
        "gh auth status", 
        "检查GitHub认证", 
        timeout=15
    )
    if not success:
        return False
    
    # 步骤4: 测试构建（仅检查脚本存在）
    if not os.path.exists('build_app.py'):
        print("❌ build_app.py不存在")
        return False
    print("✅ 构建脚本存在")
    
    # 步骤5: 测试git push（dry run）
    success, output = run_command_with_timeout(
        "git push --dry-run", 
        "测试Git推送", 
        timeout=30
    )
    if not success:
        print("⚠️ Git推送测试失败，但继续...")
    
    return True

def test_build_only():
    """仅测试构建步骤"""
    print("🔨 测试构建步骤...")
    
    success, output = run_command_with_timeout(
        "python build_app.py", 
        "构建应用", 
        timeout=300  # 5分钟超时
    )
    
    return success

def test_github_operations():
    """测试GitHub相关操作"""
    print("🐙 测试GitHub操作...")
    
    version = get_version()
    test_tag = f"v{version}-debug-test"
    
    try:
        # 清理可能存在的测试标签
        print("🧹 清理测试标签...")
        subprocess.run(['git', 'tag', '-d', test_tag], capture_output=True)
        subprocess.run(['gh', 'release', 'delete', test_tag, '--yes'], capture_output=True)
        subprocess.run(['git', 'push', 'origin', '--delete', test_tag], capture_output=True)
        
        # 创建测试标签
        success, output = run_command_with_timeout(
            ['git', 'tag', '-a', test_tag, '-m', 'Debug test tag'], 
            "创建测试标签", 
            timeout=10,
            shell=False
        )
        if not success:
            return False
        
        # 推送标签
        success, output = run_command_with_timeout(
            ['git', 'push', 'origin', test_tag], 
            "推送测试标签", 
            timeout=60,
            shell=False
        )
        if not success:
            return False
        
        # 创建GitHub release
        dmg_name = get_dmg_name()
        cmd = [
            'gh', 'release', 'create', test_tag,
            '--title', f'Debug Test {version}',
            '--notes', 'This is a debug test release. Will be deleted shortly.',
            '--prerelease'
        ]
        
        if os.path.exists(dmg_name):
            cmd.append(dmg_name)
        
        success, output = run_command_with_timeout(
            cmd, 
            "创建GitHub Release", 
            timeout=120,
            shell=False
        )
        
        if success:
            print("✅ GitHub操作测试成功")
            # 清理测试release
            print("🧹 清理测试release...")
            subprocess.run(['gh', 'release', 'delete', test_tag, '--yes'], capture_output=True)
            subprocess.run(['git', 'tag', '-d', test_tag], capture_output=True)
            subprocess.run(['git', 'push', 'origin', '--delete', test_tag], capture_output=True)
        
        return success
        
    except Exception as e:
        print(f"❌ GitHub操作测试异常: {e}")
        return False

def main():
    """主函数"""
    version = get_version()
    print(f"🐛 MediaCopyer v{version} 发布调试工具")
    print("=" * 50)
    
    print("选择测试模式:")
    print("1. 逐步测试所有步骤")
    print("2. 仅测试构建")
    print("3. 仅测试GitHub操作")
    print("4. 完整发布流程测试")
    
    try:
        choice = input("请选择 (1-4): ").strip()
        
        if choice == "1":
            if test_individual_steps():
                print("✅ 所有步骤测试通过")
            else:
                print("❌ 某些步骤测试失败")
                
        elif choice == "2":
            if test_build_only():
                print("✅ 构建测试通过")
            else:
                print("❌ 构建测试失败")
                
        elif choice == "3":
            if test_github_operations():
                print("✅ GitHub操作测试通过")
            else:
                print("❌ GitHub操作测试失败")
                
        elif choice == "4":
            print("🚀 开始完整发布流程测试...")
            success, output = run_command_with_timeout(
                "python release.py", 
                "完整发布流程", 
                timeout=600  # 10分钟超时
            )
            if success:
                print("✅ 完整发布流程测试通过")
            else:
                print("❌ 完整发布流程测试失败")
        else:
            print("❌ 无效选择")
            
    except KeyboardInterrupt:
        print("\n🛑 用户中断测试")
    except Exception as e:
        print(f"❌ 测试过程中发生异常: {e}")

if __name__ == '__main__':
    main()