from PyInstaller.utils.hooks import collect_all

# Collect all necessary files for requests
requests_datas, requests_binaries, requests_hiddenimports = collect_all('requests')

block_cipher = None

admin_manifest = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="1.0.0.0"
    processorArchitecture="X86"
    name="Guardian"
    type="win32"
  />
  <description>Guardian Security Application</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application>
      <!-- Windows 10 -->
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>
    </application>
  </compatibility>
</assembly>
'''

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=requests_binaries,
    datas=requests_datas + [
        ('views', 'views'),
        ('models', 'models'),
        ('controllers', 'controllers'),
        ('utils', 'utils'),  # Add utils directory
        ('assets', 'assets'),  # If you have any assets
    ],
    hiddenimports=requests_hiddenimports + [
        'requests',
        'urllib3',
        'charset_normalizer',
        'idna',
        'certifi',
        'plyer.platforms.win.notification',
        'customtkinter',
        'PIL',
        'PIL._tkinter_finder',  # Add this for PIL/Tkinter integration
        'xml.etree.ElementTree',
        'json',
        'os',
        'sys',
        'datetime',
        'logging',
        'threading',
        'asyncio',
        'aiohttp',  # For Shuffle API calls
        'reportlab',  # For PDF generation
        'csv',  # For CSV export
        'subprocess',  # For system commands
        'ctypes',  # For admin checks
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add additional data files for configuration
a.datas += [
    ('acknowledged_alerts.txt', '', 'DATA'),  # Empty file that will be created if needed
]

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Guardian',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to True temporarily for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    manifest=admin_manifest,
    icon='assets/Guardian.ico',  # Add your icon if you have one
    uac_admin=True
)