#!/usr/bin/env python3
"""
Test script for multi-source directory functionality
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def create_test_structure():
    """Create test directory structure with sample files"""
    # Create temporary directories
    test_dir = Path(tempfile.mkdtemp(prefix="mediacopyer_test_"))
    
    # Create multiple source directories
    source1 = test_dir / "source1"
    source2 = test_dir / "source2"
    source3 = test_dir / "source3"
    
    for src in [source1, source2, source3]:
        src.mkdir(parents=True, exist_ok=True)
        
        # Create some test image files (empty files for testing)
        (src / "IMG_001.jpg").touch()
        (src / "IMG_002.png").touch()
        (src / "VID_001.mp4").touch()
    
    # Create multiple destination directories
    dest1 = test_dir / "dest1"
    dest2 = test_dir / "dest2"
    
    for dest in [dest1, dest2]:
        dest.mkdir(parents=True, exist_ok=True)
    
    return test_dir, [source1, source2, source3], [dest1, dest2]

def test_multi_source_gui():
    """Test the multi-source functionality with GUI"""
    try:
        # Create test structure
        test_dir, sources, destinations = create_test_structure()
        
        print("创建测试目录结构:")
        print(f"测试根目录: {test_dir}")
        print("\n源目录:")
        for i, src in enumerate(sources, 1):
            files = list(src.iterdir())
            print(f"  源目录 {i}: {src}")
            print(f"    文件: {[f.name for f in files]}")
        
        print("\n目标目录:")
        for i, dest in enumerate(destinations, 1):
            print(f"  目标目录 {i}: {dest}")
        
        # Import GUI components
        from gui.main_window import MediaCopyerGUI
        
        print("\n启动 GUI 进行测试...")
        print("请在 GUI 中:")
        print("1. 添加以下源目录:")
        for src in sources:
            print(f"   - {src}")
        print("2. 添加以下目标目录:")
        for dest in destinations:
            print(f"   - {dest}")
        print("3. 选择 '预览模式' 进行安全测试")
        print("4. 点击 '开始处理' 查看多源目录处理结果")
        
        # Start GUI
        gui = MediaCopyerGUI()
        gui.run()
        
        # Check results after GUI closes
        print("\n测试完成!")
        print("检查目标目录内容:")
        for i, dest in enumerate(destinations, 1):
            print(f"\n目标目录 {i}: {dest}")
            if dest.exists():
                for item in dest.rglob("*"):
                    if item.is_file():
                        print(f"  {item.relative_to(dest)}")
    
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        try:
            import shutil
            if 'test_dir' in locals():
                print(f"\n清理测试目录: {test_dir}")
                shutil.rmtree(test_dir)
        except Exception as e:
            print(f"清理失败: {e}")

if __name__ == "__main__":
    test_multi_source_gui()
