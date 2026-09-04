[Setup]
AppName=Password Keeper
AppVersion={#Password KeeperVersion}
DefaultDirName={autopf}\Password Keeper
DefaultGroupName=Password Keeper
OutputBaseFilename=Password Keeper-{#Password KeeperVersion}-Windows-Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=..\..\dist

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
; Pulls the entire directory compiled by PyInstaller into the Program Files directory
Source: "..\..\dist\PasswordKeeper\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Password Keeper"; Filename: "{app}\PasswordKeeper.exe"
Name: "{autodesktop}\Password Keeper"; Filename: "{app}\PasswordKeeper.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked
