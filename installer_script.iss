[Setup]
AppName=Wind Sound Generator
AppVersion=1.0
DefaultDirName={pf}\WindSoundApp
DefaultGroupName=Wind Sound Generator
OutputDir=.
OutputBaseFilename=WindSoundAppInstaller
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=icon.ico

[Files]
Source: "dist\WindSoundApp.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Wind Sound Generator"; Filename: "{app}\WindSoundApp.exe"
Name: "{commondesktop}\Wind Sound Generator"; Filename: "{app}\WindSoundApp.exe"

[Run]
Filename: "{app}\WindSoundApp.exe"; Description: "Launch Wind Sound Generator"; Flags: nowait postinstall skipifsilent
