# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Get the current directory
current_dir = os.path.abspath('.')

a = Analysis(
    ['media_copyer_gui.py'],
    pathex=[current_dir],
    binaries=[],
    datas=[
        ('gui/locales', 'gui/locales'),
    ],
    hiddenimports=[
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'gui',
        'gui.main_window',
        'gui.widgets',
        'gui.processor',
        'gui.options_frame',
        'gui.i18n',
        'gui.locales.zh_CN',
        'gui.locales.en_US',
        'core',
        'core.organizer',
        'core.organizer.media_organizer',
        'core.organizer.scanner',
        'core.organizer.file_operations',
        'core.organizer.hash_utils',
        'core.utils',
        'core.utils.filesystem',
        'core.utils.string_utils',
        'core.metadata',
        'core.device',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MediaCopyer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 设置为False以隐藏控制台窗口
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/MediaCopyer.ico' if os.name == 'nt' else 'resources/MediaCopyer.icns',  # APP图标文件
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MediaCopyer',
)

app = BUNDLE(
    coll,
    name='MediaCopyer.app',
    icon='resources/MediaCopyer.icns',
    bundle_identifier='com.tianlee.mediacopyer',
    info_plist={
        'CFBundleName': 'MediaCopyer',
        'CFBundleDisplayName': 'MediaCopyer',
        'CFBundleGetInfoString': 'MediaCopyer - Media Organization Tool',
        'CFBundleIdentifier': 'com.tianlee.mediacopyer',
        'CFBundleVersion': '1.1.1',
        'CFBundleShortVersionString': '1.1.1',
        'CFBundleInfoDictionaryVersion': '6.0',
        'CFBundleExecutable': 'MediaCopyer',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': 'MCPY',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.15.0',
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'LSApplicationCategoryType': 'public.app-category.utilities',
        'NSHumanReadableCopyright': '© 2024-2025 MediaCopyer Team',
        'CFBundleDevelopmentRegion': 'en',
        'CFBundleLocalizations': ['en', 'zh_CN'],
        'NSRequiresAquaSystemAppearance': False,
        'LSUIElement': False,
        'NSSupportsAutomaticGraphicsSwitching': True,
    },
)