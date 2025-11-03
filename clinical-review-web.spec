# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Clinical Review Web App
웹 앱 버전용 빌드 설정
"""

import sys
from pathlib import Path

block_cipher = None

# Streamlit 패키지 경로 찾기
import streamlit
streamlit_path = Path(streamlit.__file__).parent

a = Analysis(
    ['web_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('src', 'src'),
        ('web_app.py', '.'),
        (str(streamlit_path / 'static'), 'streamlit/static'),
        (str(streamlit_path / 'runtime'), 'streamlit/runtime'),
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'pdfplumber',
        'pdfplumber.page',
        'pdfplumber.pdf',
        'yaml',
        'jinja2',
        'tabulate',
        'PIL',
        'PIL.Image',
        'PyPDF2',
        'openpyxl',
        'click',
        'tornado',
        'watchdog',
        'validators',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy.distutils',
        'IPython',
        'tkinter',
        'pytest',
        'setuptools',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ClinicalReview-Web',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 콘솔 표시 (로그 확인용)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
