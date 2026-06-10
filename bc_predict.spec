# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# 收集 xgboost 的所有依赖（包括 DLL）
xgboost_datas, xgboost_binaries, xgboost_hiddenimports = collect_all('xgboost')

a = Analysis(
    ['bc_predict.py'],                     # 你的主脚本
    pathex=[],
    binaries=xgboost_binaries,             # 关键：添加 xgboost 的二进制文件（.dll）
    datas=xgboost_datas,                   # 关键：添加 xgboost 的数据文件
    hiddenimports=[
        'sklearn',
        'numpy',
        'pandas',
        'joblib',
        'tkinter',
        'xgboost'
    ] + xgboost_hiddenimports,             # 添加 xgboost 的隐藏导入
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='BC_Predictor',                   # 生成的 exe 名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,                          # 显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
