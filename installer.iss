; ============================================================
;  AWWA Lunch Project — Inno Setup Installer Script
;  Generates:  AWWA_Canteen_Setup.exe
;  Installs to:  C:\Program Files\AWWA Lunch Project\
;  Creates:  Desktop shortcut + Start Menu shortcut
;  Includes:  Uninstaller
; ============================================================

[Setup]
AppName=AWWA Lunch Project - Canteen Management
AppVersion=5.0
AppPublisher=Indian Army AWWA
AppPublisherURL=https://github.com/rohankumarrawat/CANTEEN
AppSupportURL=https://github.com/rohankumarrawat/CANTEEN
AppUpdatesURL=https://github.com/rohankumarrawat/CANTEEN

; Installation directory
DefaultDirName={autopf}\AWWA Lunch Project
DefaultGroupName=AWWA Lunch Project

; Output
OutputDir=installer_output
OutputBaseFilename=AWWA_Canteen_Setup_v5

; Visuals
SetupIconFile=app_icon.ico
WizardStyle=modern
WizardSmallImageFile=app_icon.ico

; Compression
Compression=lzma2
SolidCompression=yes

; Windows version requirement (Windows 10+)
MinVersion=10.0

; Uninstaller icon
UninstallDisplayIcon={app}\AWWA_Lunch_Project.exe
UninstallDisplayName=AWWA Lunch Project - Canteen Management

; Privileges
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Show license step
;LicenseFile=LICENSE.txt

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon";   Description: "Create a &Desktop shortcut";       GroupDescription: "Additional icons:"; Flags: checked
Name: "startmenuicon"; Description: "Create a &Start Menu shortcut";    GroupDescription: "Additional icons:"; Flags: checked

[Files]
; Main application executable
Source: "dist\AWWA_Lunch_Project.exe";  DestDir: "{app}"; Flags: ignoreversion

; Database — only copy if one does NOT already exist (preserve client data)
Source: "canteen.db";                   DestDir: "{app}"; Flags: onlyifdoesntexist uninsneveruninstall

; App icon for shortcuts
Source: "app_icon.ico";                 DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Desktop shortcut
Name: "{commondesktop}\AWWA Canteen"; Filename: "{app}\AWWA_Lunch_Project.exe"; IconFilename: "{app}\app_icon.ico"; Comment: "AWWA Lunch Project — Canteen Management System v5.0"; Tasks: desktopicon

; Start Menu group
Name: "{group}\AWWA Canteen Management"; Filename: "{app}\AWWA_Lunch_Project.exe"; IconFilename: "{app}\app_icon.ico"; Comment: "AWWA Lunch Project — Canteen Management System v5.0"; Tasks: startmenuicon

; Uninstaller in Start Menu
Name: "{group}\Uninstall AWWA Canteen"; Filename: "{uninstallexe}"

[Run]
; Offer to launch after install
Filename: "{app}\AWWA_Lunch_Project.exe"; Description: "Launch AWWA Canteen Management System"; Flags: nowait postinstall skipifsilent; WorkingDir: "{app}"

[UninstallDelete]
; Remove the backups folder created by the app on uninstall
Type: filesandordirs; Name: "{app}\backups"
