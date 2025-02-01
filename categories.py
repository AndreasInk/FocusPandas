def categorize_apps(df):
    """
    Categorize apps into detailed productivity levels given a screentime dataframe.
    """
    # Define app categories with finer granularity
    app_categories = {
    # Development Tools
    'com.microsoft.VSCode': 'Development',
    'com.apple.dt.Xcode': 'Development',
    'com.figma.Desktop': 'Development',
    'com.github.GitHubDesktop': 'Development',
    'cc.arduino.IDE2': 'Development',
    'app.codeedit.CodeEdit': 'Development',
    'com.roadesign.Codyeapp': 'Development',
    'org.openmv.openmvide': 'Development',
    'com.oracle.workbench.MySQLWorkbench': 'Development',
    'com.apple.dt.AutomationModeUI': 'Development',
    'com.apple.Terminal': 'Development',
    'com.apple.dt.CommandLineTools.installondemand': 'Development',

    # Marketing
    'com.apple.FinalCutTrial': 'Marketing',
    'com.Ai.NeuroNote': 'Development',  # As per your instruction
    'com.Ai.NeuroNote3': 'Development',  # As per your instruction
    'com.hnc.Discord': 'Social Media',  # Special case
    'company.thebrowser.Browser': 'Development',  # As per your instruction
    'com.hammerandchisel.discord': 'Social Media',
    'com.github.GitHubClient': 'Development',
    'com.framer.electron': 'Development',  # Assuming creative/development hybrid
    'com.nvidia.gfnpc.mall': 'Entertainment',  # Gaming/Entertainment
    'com.apple.VoiceOver': 'Utility',  # System Utility

    # Social Media
    'com.hnc.Discord': 'Social Media',  # Special case
    'com.apple.FaceTime': 'Social Media',
    'com.apple.findmy': 'Utility',
    'com.apple.VoiceOver': 'Utility',
    'com.apple.Spotlight': 'Utility',

    # Creative
    'com.canva.CanvaDesktop': 'Development',  # As per your instruction
    'com.framer.electron': 'Development',  # As per your instruction
    'com.apple.FontBook': 'Creative',
    'com.apple.Photos': 'Creative',
    'com.apple.GenerativePlaygroundApp': 'Creative',
    'com.apple.FolderActionsSetup': 'Creative',

    # Entertainment
    'com.netflix.Netflix': 'Entertainment',
    'com.apple.Music': 'Entertainment',
    'com.apple.PhotoBooth': 'Entertainment',
    'com.apple.Chess': 'Entertainment',
    'com.apple.TV': 'Entertainment',

    # Browsing
    'com.google.Chrome': 'Browsing',
    'com.apple.Safari': 'Browsing',

    # AI Productivity
    'com.openai.chat': 'Development',  # As per your instruction
    'com.Ai.NeuroNote': 'Development',
    'com.Ai.NeuroNote3': 'Development',

    # Utility
    'com.apple.calculator': 'Utility',
    'com.apple.Dictionary': 'Utility',
    'com.apple.DiskUtility': 'Utility',
    'com.apple.finder': 'Utility',
    'com.apple.Maps': 'Utility',
    'com.apple.SystemPreferences': 'Utility',
    'com.apple.Terminal': 'Development',  # Also fits Utility
    'com.apple.VoiceMemos': 'Utility',
    'com.apple.reminders': 'Utility',
    'com.apple.notes': 'Utility',
    'com.apple.calendar': 'Utility',
    'com.apple.ActivityMonitor': 'Utility',
    'com.apple.Console': 'Utility',
    'com.apple.DigitalColorMeter': 'Utility',
    'com.apple.DiskUtility': 'Utility',
    'com.apple.FontBook': 'Creative',
    'com.apple.GenerativePlaygroundApp': 'Creative',
    'com.apple.launchpad.launcher': 'Utility',
    'com.apple.mail': 'Utility',
    'com.apple.Passwords': 'Utility',
    'com.apple.Preview': 'Utility',
    'com.apple.TextEdit': 'Utility',
    'com.apple.QuickTimePlayerX': 'Entertainment',
    'com.apple.screencaptureui': 'Utility',
    'com.apple.scriptEditor': 'Utility',
    # ... Add additional Utility apps as needed

    # System
    'com.apple.MRT': 'System',
    'com.apple.XProtectFramework.XProtect': 'System',
    'com.apple.SyncServices.AppleMobileDeviceHelper': 'System',
    'com.apple.SyncServices.AppleMobileSync': 'System',
    'com.apple.MobileDeviceUpdater': 'System',
    'com.apple.ScriptEditor.id.cocoa-applet-template': 'System',
    'com.apple.ScriptEditor.id.droplet-with-settable-properties-template': 'System',
    'com.apple.ScriptEditor.id.file-processing-droplet-template': 'System',
    'com.apple.ScriptEditor.id.image-file-processing-droplet-template': 'System',
    'com.apple.python3': 'System',
    'com.apple.print.AirScanLegacyDiscovery': 'System',
    'com.apple.AppStore': 'Utility',  # System App
    'com.apple.Automator': 'Utility',  # System App
    'com.apple.iBooksX': 'Entertainment',  # System App
    'com.apple.calculator': 'Utility',  # System App
    'com.apple.iCal': 'Utility',  # System App
    'com.apple.Chess': 'Entertainment',  # System App
    'com.apple.clock': 'Utility',  # System App
    'com.apple.AddressBook': 'Utility',  # System App
    'com.apple.Dictionary': 'Utility',  # System App
    'com.apple.FaceTime': 'Social Media',  # System App
    'com.apple.findmy': 'Utility',  # System App
    'com.apple.FontBook': 'Creative',  # System App
    'com.apple.freeform': 'Creative',  # System App
    'com.apple.Home': 'Utility',  # System App
    'com.apple.Image_Capture': 'Utility',  # System App
    'com.apple.GenerativePlaygroundApp': 'Creative',  # System App
    'com.apple.launchpad.launcher': 'Utility',  # System App
    'com.apple.mail': 'Utility',  # System App
    'com.apple.Maps': 'Utility',  # System App
    'com.apple.MobileSMS': 'Utility',  # System App
    'com.apple.exposelauncher': 'Utility',  # System App
    'com.apple.Music': 'Entertainment',  # System App
    'com.apple.news': 'Entertainment',  # System App
    'com.apple.Notes': 'Utility',  # System App
    'com.apple.Passwords': 'Utility',  # System App
    'com.apple.PhotoBooth': 'Entertainment',  # System App
    'com.apple.Photos': 'Creative',  # System App
    'com.apple.podcasts': 'Entertainment',  # System App
    'com.apple.Preview': 'Utility',  # System App
    'com.apple.QuickTimePlayerX': 'Entertainment',  # System App
    'com.apple.reminders': 'Utility',  # System App
    'com.apple.shortcuts': 'Productive',  # System App
    'com.apple.siri.launcher': 'Utility',  # System App
    'com.apple.Stickies': 'Utility',  # System App
    'com.apple.stocks': 'Entertainment',  # System App
    'com.apple.systempreferences': 'Utility',  # System App
    'com.apple.TV': 'Entertainment',  # System App
    'com.apple.TextEdit': 'Utility',  # System App
    'com.apple.backup.launcher': 'Utility',  # System App
    'com.apple.helpviewer': 'Utility',  # System App
    'com.apple.ActivityMonitor': 'Utility',  # System App
    'com.apple.airport.airportutility': 'Utility',  # System App
    'com.apple.audio.AudioMIDISetup': 'Utility',  # System App
    'com.apple.BluetoothFileExchange': 'Utility',  # System App
    'com.apple.bootcampassistant': 'Utility',  # System App
    'com.apple.ColorSyncUtility': 'Utility',  # System App
    'com.apple.Console': 'Utility',  # System App
    'com.apple.DigitalColorMeter': 'Utility',  # System App
    'com.apple.DiskUtility': 'Utility',  # System App
    'com.apple.grapher': 'Utility',  # System App
    'com.apple.MigrateAssistant': 'Utility',  # System App
    'com.apple.printcenter': 'Utility',  # System App
    'com.apple.ScreenSharing': 'Utility',  # System App
    'com.apple.screenshot.launcher': 'Utility',  # System App
    'com.apple.ScriptEditor2': 'Utility',  # System App
    'com.apple.SystemProfiler': 'Utility',  # System App
    'com.apple.Terminal': 'Development',  # System App
    'com.apple.VoiceOverUtility': 'Utility',  # System App
    'com.apple.VoiceMemos': 'Utility',  # System App
    'com.apple.weather': 'Utility',  # System App
    'com.apple.ScreenContinuity': 'Utility',  # System App

    # Other Applications
    'com.if.Amphetamine': 'Marketing',  # As per your instruction
    'com.apple.configurator.ui': 'Utility',  # Apple Configurator
    'company.thebrowser.Browser': 'Browsing',  # As per your instruction
    'com.goodsnooze.bakery': 'Marketing',  # Assumed based on name
    'com.nonstrict.Bezel-appstore': 'Unknown',  # Limited info
    'org.blenderfoundation.blender': 'Development',  # Blender is 3D modeling
    'com.canva.CanvaDesktop': 'Development',  # As per your instruction
    'com.openai.chat': 'Development',  # As per your instruction
    'com.macpaw.CleanMyMac-mas': 'Utility',
    'app.codeedit.CodeEdit': 'Development',
    'com.roadesign.Codyeapp': 'Development',
    'de.ixeau.Curve': 'Development',  # Assumed
    'com.lukilabs.lukiapp': 'Marketing',  # As per your instruction
    'app.diagrams.DiagramsMac.mas': 'Development',
    'com.hnc.Discord': 'Social Media',
    'com.docker.docker': 'Development',
    'com.figma.Desktop': 'Development',  # As per your instruction
    'com.apple.FinalCutTrial': 'Marketing',  # As per your instruction
    'com.framer.electron': 'Development',  # As per your instruction
    'com.nvidia.gfnpc.mall': 'Entertainment',
    'com.github.GitHubClient': 'Development',
    'com.google.Chrome': 'Browsing',
    'com.jomo.Jomo': 'Unknown',  # Limited info
    'ai.elementlabs.lmstudio': 'Development',  # Assumed
    'com.microsoft.teams': 'School',
    'com.microsoft.Word': 'School',
    'com.oracle.workbench.MySQLWorkbench': 'Development',
    'com.Ai.NeuroNote': 'Development',
    'notion.id': 'Productive',  # Notion is productivity
    'com.apple.iWork.Numbers': 'Development',
    'com.electron.ollama': 'Development',
    'org.openmv.openmvide': 'Development',
    'com.postmanlabs.mac': 'Development',
    'org.prismlauncher.PrismLauncher': 'Development',
    'org.raspberrypi.imagingutility': 'Utility',
    'com.apple.RealityConverter': 'Development',  # Reality Converter is AR-related
    'com.swiftLee.RocketSim': 'Development',
    'com.mortenjust.Rendermock': 'Development',
    'com.apple.SFSymbols-beta': 'Development',
    'com.apple.Safari': 'Browsing',
    'com.timpler.screenstudio': 'Marketing',
    'com.tinyspeck.slackmacgap': 'Social Media',
    'com.sebvidal.Snippet': 'Development',
    'dev.erikschnell.CodeSnippets': 'Development',
    'com.termius.mac': 'Development',
    'com.apple.TestFlight': 'Development',  # TestFlight is for testing apps
    'com.install4j.1106-5897-7327-6550.5': 'School',  # Visual Paradigm is UML tool
    'com.microsoft.VSCode': 'Development',
    'com.apple.dt.Xcode': 'Development',
    'io.balena.etcher': 'Development',
    'com.mlobodzinski.Stoic': 'Development',
    'us.zoom.xos': 'Marketing',
    'com.apple.MRT': 'System',
    'com.apple.XProtectFramework.XProtect': 'System',
    'com.apple.SyncServices.AppleMobileDeviceHelper': 'System',
    'com.apple.SyncServices.AppleMobileSync': 'System',
    'com.apple.MobileDeviceUpdater': 'System',
    'com.apple.ScriptEditor.id.cocoa-applet-template': 'System',
    'com.apple.ScriptEditor.id.droplet-with-settable-properties-template': 'System',
    'com.apple.ScriptEditor.id.file-processing-droplet-template': 'System',
    'com.apple.ScriptEditor.id.image-file-processing-droplet-template': 'System',
    'com.apple.python3': 'System',
    'com.apple.print.AirScanLegacyDiscovery': 'System',
    'com.apple.AppStore': 'Utility',
    'com.apple.Automator': 'Utility',
    'com.apple.iBooksX': 'Entertainment',
    'com.apple.calculator': 'Utility',
    'com.apple.iCal': 'Utility',
    'com.apple.Chess': 'Entertainment',
    'com.apple.clock': 'Utility',
    'com.apple.AddressBook': 'Utility',
    'com.apple.Dictionary': 'Utility',
    'com.apple.FaceTime': 'Social Media',
    'com.apple.findmy': 'Utility',
    'com.apple.FontBook': 'Creative',
    'com.apple.freeform': 'Creative',
    'com.apple.Home': 'Utility',
    'com.apple.Image_Capture': 'Utility',
    'com.apple.GenerativePlaygroundApp': 'Creative',
    'com.apple.launchpad.launcher': 'Utility',
    'com.apple.mail': 'Utility',
    'com.apple.Maps': 'Utility',
    'com.apple.MobileSMS': 'Utility',
    'com.apple.exposelauncher': 'Utility',
    'com.apple.Music': 'Entertainment',
    'com.apple.news': 'Entertainment',
    'com.apple.Notes': 'Utility',
    'com.apple.Passwords': 'Utility',
    'com.apple.PhotoBooth': 'Entertainment',
    'com.apple.Photos': 'Creative',
    'com.apple.podcasts': 'Entertainment',
    'com.apple.Preview': 'Utility',
    'com.apple.QuickTimePlayerX': 'Entertainment',
    'com.apple.reminders': 'Utility',
    'com.apple.shortcuts': 'Productive',
    'com.apple.siri.launcher': 'Utility',
    'com.apple.Stickies': 'Utility',
    'com.apple.stocks': 'Entertainment',
    'com.apple.systempreferences': 'Utility',
    'com.apple.TV': 'Entertainment',
    'com.apple.TextEdit': 'Utility',
    'com.apple.backup.launcher': 'Utility',
    'com.apple.helpviewer': 'Utility',
    'com.apple.ActivityMonitor': 'Utility',
    'com.apple.airport.airportutility': 'Utility',
    'com.apple.audio.AudioMIDISetup': 'Utility',
    'com.apple.BluetoothFileExchange': 'Utility',
    'com.apple.bootcampassistant': 'Utility',
    'com.apple.ColorSyncUtility': 'Utility',
    'com.apple.Console': 'Utility',
    'com.apple.DigitalColorMeter': 'Utility',
    'com.apple.DiskUtility': 'Utility',
    'com.apple.grapher': 'Utility',
    'com.apple.MigrateAssistant': 'Utility',
    'com.apple.printcenter': 'Utility',
    'com.apple.ScreenSharing': 'Utility',
    'com.apple.screenshot.launcher': 'Utility',
    'com.apple.ScriptEditor2': 'Utility',
    'com.apple.SystemProfiler': 'Utility',
    'com.apple.Terminal': 'Development',
    'com.apple.VoiceOverUtility': 'Utility',
    'com.apple.VoiceMemos': 'Utility',
    'com.apple.weather': 'Utility',
    'com.apple.ScreenContinuity': 'Utility',

    # Helper and System Services (categorized as 'System')
    'com.apple.ClassroomStudentMenuExtra': 'System',
    'com.apple.ColorSyncCalibrator': 'System',
    'com.apple.AOSUIPrefPaneLauncher': 'System',
    'com.apple.AVB-Audio-Configuration': 'System',
    'com.apple.print.add': 'System',
    'com.apple.AddressBook.UrlForwarder': 'System',
    'com.apple.AirPlayUIAgent': 'System',
    'com.apple.AirPortBaseStationAgent': 'System',
    'com.apple.AppleScriptUtility': 'System',
    'com.apple.AboutThisMacLauncher': 'System',
    'com.apple.archiveutility': 'Utility',
    'com.apple.DVDPlayer': 'Entertainment',
    'com.apple.DeskCam': 'Utility',
    'com.apple.DirectoryUtility': 'Utility',
    'com.apple.ExpansionSlotUtility': 'Utility',
    'com.apple.appleseed.FeedbackAssistant': 'Utility',
    'com.apple.FolderActionsSetup': 'Creative',
    'com.apple.keychainaccess': 'Utility',
    'com.apple.Ticket-Viewer': 'Utility',
    'com.apple.wifi.diagnostics': 'Utility',
    'com.apple.IPAInstaller': 'Utility',
    'com.apple.AskToMessagesHost': 'Utility',
    'com.apple.Automator.Automator-Application-Stub': 'Utility',
    'com.apple.AutomatorInstaller': 'Utility',
    'com.apple.Batteries': 'Utility',
    'com.apple.BluetoothSetupAssistant': 'Utility',
    'com.apple.BluetoothUIServer': 'Utility',
    'com.apple.BluetoothUIService': 'Utility',
    'com.apple.CalendarFileHandler': 'Utility',
    'com.apple.CaptiveNetworkAssistant': 'Utility',
    'com.apple.CertificateAssistant': 'Utility',
    'com.apple.controlcenter': 'Utility',
    'com.apple.controlstrip': 'Utility',
    'com.apple.CoreLocationAgent': 'Utility',
    'com.apple.coreservices.uiagent': 'Utility',
    'com.apple.NewDeviceOutreachApp': 'Utility',
    'com.apple.databaseevents': 'Utility',
    'com.apple.DiagnosticsReporter': 'Utility',
    'com.apple.DiscHelper': 'Utility',
    'com.apple.DiskImageMounter': 'Utility',
    'com.apple.dock': 'Utility',
    'com.apple.DwellControl': 'Utility',
    'com.apple.EnhancedLogging': 'Utility',
    'com.apple.EraseAssistant': 'Utility',
    'com.apple.EscrowSecurityAlert': 'Utility',
    'com.apple.Family': 'Utility',
    'com.apple.FileProvider-Feedback': 'Utility',
    'com.apple.Finder': 'Utility',
    'com.apple.FolderActionsDispatcher': 'Utility',
    'com.apple.gamecenter': 'Entertainment',
    'com.apple.IOUIAgent': 'Utility',
    'com.apple.imageevents': 'Utility',
    'com.apple.dt.CommandLineTools.installondemand': 'Development',
    'com.apple.PackageUIKit.Install-in-Progress': 'Utility',
    'com.apple.Installer-Progress': 'Utility',
    'com.apple.installer': 'Utility',
    'com.apple.JavaLauncher': 'Development',
    'com.apple.KeyboardAccessAgent': 'Utility',
    'com.apple.KeyboardSetupAssistant': 'Utility',
    'com.apple.security.Keychain-Circle-Notification': 'Utility',
    'com.apple.Language-Chooser': 'Utility',
    'com.apple.MTLReplayer': 'Utility',
    'com.apple.ManagedClient': 'Utility',
    'com.apple.MediaMLPluginApp': 'Utility',
    'com.apple.MemorySlotUtility': 'Utility',
    'com.apple.musicrecognition.mac': 'Entertainment',
    'com.apple.NetAuthAgent': 'Utility',
    'com.apple.notificationcenterui': 'Utility',
    'com.apple.NowPlayingTouchUI': 'Utility',
    'com.apple.OBEXAgent': 'Utility',
    'com.apple.ODSAgent': 'Utility',
    'com.apple.OSDUIHelper': 'Utility',
    'com.apple.PIPAgent': 'Utility',
    'com.apple.PairedDevices': 'Utility',
    'com.apple.Pass-Viewer': 'Utility',
    'com.apple.PeopleMessageService': 'Utility',
    'com.apple.PeopleViewService': 'Utility',
    'com.apple.PowerChime': 'Utility',
    'com.apple.PreviewShell': 'Utility',
    'com.apple.displaycalibrator': 'Utility',
    'com.apple.ProblemReporter': 'Utility',
    'com.apple.mcx.ProfileHelper': 'Utility',
    'com.apple.RapportUIAgent': 'Utility',
    'com.apple.pluginIM.pluginIMRegistrator': 'Utility',
    'com.apple.RemoteDesktopAgent': 'Utility',
    'com.apple.RemoteDesktopMessageAgent': 'Utility',
    'com.apple.SSMenuAgent': 'Utility',
    'com.apple.OAHSoftwareUpdateApp': 'Utility',
    'com.apple.ScreenTimeWidgetApplication': 'Utility',
    'com.apple.ScreenSaver.Engine': 'Utility',
    'com.apple.ScriptMenuApp': 'Utility',
    'com.apple.ScriptMonitor': 'Utility',
    'com.apple.SetupAssistant': 'Utility',
    'com.apple.shortcuts.droplet': 'Utility',
    'com.apple.shortcuts.events': 'Utility',
    'com.apple.ShortcutsActions': 'Utility',
    'com.apple.Siri': 'Utility',
    'com.apple.SoftwareUpdate': 'Utility',
    'com.apple.SpacesTouchBarAgent': 'Utility',
    'com.apple.Spotlight': 'Utility',
    'com.apple.windowmanager.StageManagerOnboarding': 'Utility',
    'com.apple.systemevents': 'Utility',
    'com.apple.systemuiserver': 'Utility',
    'com.apple.TextInputMenuAgent': 'Utility',
    'com.apple.TextInputSwitcher': 'Utility',
    'com.apple.ThermalTrap': 'Utility',
    'com.apple.timemachine.HelperAgent': 'Utility',
    'com.apple.tips': 'Utility',
    'com.apple.UIKitSystemApp': 'Utility',
    'com.apple.UniversalAccessControl': 'Utility',
    'com.apple.universalcontrol': 'Utility',
    'com.apple.UnmountAssistantAgent': 'Utility',
    'com.apple.UserNotificationCenter': 'Utility',
    'com.apple.VoiceOver': 'Utility',
    'com.apple.wallpaper.agent': 'Utility',
    'com.apple.WatchFaceAlert': 'Utility',
    'com.apple.wifi.WiFiAgent': 'Utility',
    'com.apple.widgetkit.simulator': 'Utility',
    'com.apple.WindowManager': 'Utility',
    'com.apple.windowmanager.ShowDesktopEducation': 'Utility',
    'com.apple.WorkoutAlert-Mac': 'Utility',
    'com.apple.icq': 'Utility',
    'com.apple.CloudKit.ShareBear': 'Utility',
    'com.apple.loginwindow': 'System',
    'com.apple.rcd': 'System',
    'com.apple.screencaptureui': 'Utility',
    'com.apple.AddressBook.sync': 'Utility',
    'com.apple.ABAssistantService': 'Utility',
    'com.apple.AddressBook.abd': 'Utility',
    'com.apple.AddressBookSourceSync': 'Utility',
    'com.apple.FontRegistryUIAgent': 'Utility',
    'com.apple.speech.synthesis.SpeechSynthesisServer': 'Utility',
    'com.apple.CMViewSrvc': 'Utility',
    'com.apple.ContinuityCaptureOnboardingUI': 'Utility',
    'com.apple.ctkbind': 'Utility',
    'com.apple.quicklook.qlmanage': 'Utility',
    'com.apple.QuickLookDaemon': 'Utility',
    'com.apple.quicklook.QuickLookSimulator': 'Utility',
    'com.apple.quicklook.ui.helper': 'Utility',
    'com.apple.syncserver': 'Utility',
    'com.tcltk.wish': 'Development',  # Tcl/Tk interpreter
    'com.apple.BuildWebPage': 'Development',
    'com.apple.MakePDF': 'Development',
    'com.apple.AirScanScanner': 'Utility',
    'com.apple.50onPaletteIM': 'Utility',
    'com.apple.inputmethod.Ainu': 'Utility',
    'com.apple.inputmethod.AssistiveControl': 'Utility',
    'com.apple.CharacterPaletteIM': 'Utility',
    'com.apple.inputmethod.ironwood': 'Utility',
    'com.apple.EmojiFunctionRowItem-Container': 'Utility',
    'com.apple.JapaneseIM.KanaTyping': 'Utility',
    'com.apple.JapaneseIM.RomajiTyping': 'Utility',
    'com.apple.KIM-Container': 'Utility',
    'com.apple.inputmethod.PluginIM': 'Utility',
    'com.apple.PAH-Container': 'Utility',
    'com.apple.SCIM-Container': 'Utility',
    'com.apple.TCIM-Container': 'Utility',
    'com.apple.TYIM-Container': 'Utility',
    'com.apple.inputmethod.Tamil': 'Utility',
    'com.apple.TrackpadIM-Container': 'Utility',
    'com.apple.TransliterationIM-Container': 'Utility',
    'com.apple.VIM-Container': 'Utility',
    'com.apple.iCloudUserNotificationsd': 'Utility',
    'com.apple.AOSAlertManager': 'Utility',
    'com.apple.AOSHeartbeat': 'Utility',
    'com.apple.AOSPushRelay': 'Utility',
    'com.apple.accessibility.LiveTranscriptionAgent': 'Utility',
    'com.apple.accessibility.LiveSpeech': 'Utility',
    'com.apple.AccessibilityVisualsAgent': 'Utility',
    'com.apple.Calibration-Assistant': 'Utility',
    'com.apple.AppSSOAgent': 'Utility',
    'com.apple.KerberosMenuExtra': 'Utility',
    'com.apple.AMSEngagementViewService': 'Utility',
    'com.apple.AskPermissionUI': 'Utility',
    'com.apple.AutoFillPanelService': 'Utility',
    'com.apple.dt.AutomationModeUI': 'Development',
    'com.apple.backgroundtaskmanagement.agent': 'Utility',
    'com.apple.bird': 'Utility',
    'com.apple.storeuid': 'Utility',
    'com.apple.CCE.CIMFindInputCode': 'Utility',
    'com.apple.FollowUpUI': 'Utility',
    'com.apple.frameworks.diskimages.diuiagent': 'Utility',
    'com.apple.eap8021x.eaptlstrust': 'Utility',
    'com.apple.familycontrols.useragent': 'Utility',
    'com.apple.FeedbackRemoteView': 'Utility',
    'com.apple.FindMyMacMessenger': 'Utility',
    'com.apple.identityservicesd': 'Utility',
    'com.apple.idsfoundation.IDSRemoteURLConnectionAgent': 'Utility',
    'com.apple.imagent': 'Utility',
    'com.apple.IMAutomaticHistoryDeletionAgent': 'Utility',
    'com.apple.imtransferservices.IMTransferAgent': 'Utility',
    'com.apple.nbagent': 'Utility',
    'com.apple.LinkedNotesUIService': 'Utility',
    'com.apple.privatecloudcomputed': 'Utility',
    'com.apple.ScreenReaderUIServer': 'Utility',
    'com.apple.VoiceOverQuickstart': 'Utility',
    'com.apple.AquaAppearanceHelper': 'Utility',
    'com.apple.sociallayerd': 'Utility',
    'com.apple.SoftwareUpdateNotificationManager': 'Utility',
    'com.apple.speech.SpeechDataInstallerd': 'Utility',
    'com.apple.speech.SpeechRecognitionServer': 'Utility',
    'com.apple.STMFramework.UIHelper': 'Utility',
    'com.apple.syncservices.ConflictResolver': 'Utility',
    'com.apple.syncservices.syncuid': 'Utility',
    'com.apple.accessibility.AXVisualSupportAgent': 'Utility',
    'com.apple.AccessibilityOnboarding': 'Utility',
    'com.apple.accessibility.DFRHUD': 'Utility',
    'com.apple.accessibility.universalAccessAuthWarn': 'Utility',
    'com.apple.coreservices.UASharedPasteboardProgressUI': 'Utility',
    'com.apple.ChineseTextConverterService': 'Utility',
    'com.apple.SummaryService': 'Utility',

    # Applications Without Info.plist
    # These are typically system apps or incomplete installations. Categorize as 'System' or 'Unknown'
    'Bento|Craft.app': 'Unknown',
    'My School.app': 'Unknown',
    'Odio.app': 'Unknown',
    'SchoolMate.app': 'Unknown',
    'liquiddetectiond.app': 'System',
    'monitorproduct': 'Utility',
    'Cisco-Systems.Spark': 'Social Media',
    'Cisco-Systems.Spark': 'Social Media',  # Duplicate, same category
    'WebEx-PT.webexAppLauncher': 'Social Media',
    'us.zoom.ZoomAutoUpdater': 'Marketing',
    'com.apple.systemevents': 'Utility',
    'com.apple.windowmanager.ShowDesktopEducation': 'Utility',
    'com.apple.QuickLookDaemon': 'Utility',
    # ... add any remaining apps with "Info.plist not found"

    # Developer Builds and Derived Data
    'com.Ai.NeuroNote3': 'Development',
    # Additional Derived Data entries categorized as 'Development'
    'com.apple.BuildWebPage': 'Development',
    'com.apple.MakePDF': 'Development',
    'com.apple.AirScanScanner': 'Utility',
    'com.apple.50onPaletteIM': 'Utility',
    'com.apple.inputmethod.Ainu': 'Utility',
    'com.apple.inputmethod.AssistiveControl': 'Utility',
    'com.apple.CharacterPaletteIM': 'Utility',
    'com.apple.inputmethod.ironwood': 'Utility',
    'com.apple.EmojiFunctionRowItem-Container': 'Utility',
    'com.apple.JapaneseIM.KanaTyping': 'Utility',
    'com.apple.JapaneseIM.RomajiTyping': 'Utility',
    'com.apple.KIM-Container': 'Utility',
    'com.apple.inputmethod.PluginIM': 'Utility',
    'com.apple.PAH-Container': 'Utility',
    'com.apple.SCIM-Container': 'Utility',
    'com.apple.TCIM-Container': 'Utility',
    'com.apple.TYIM-Container': 'Utility',
    'com.apple.inputmethod.Tamil': 'Utility',
    'com.apple.TrackpadIM-Container': 'Utility',
    'com.apple.TransliterationIM-Container': 'Utility',
    'com.apple.VIM-Container': 'Utility',
    # ... continue for all derived data apps

    # Dotnet Shared Apps (System Utilities)
    'com.dotnet.shared.Microsoft.AspNetCore.App': 'System',
    'com.dotnet.shared.Microsoft.NETCore.App': 'System',
    # ... continue as needed

    # Default Category for Uncategorized Apps
    # Any Bundle ID not explicitly listed will be categorized as 'Unknown'
}

    # Apply categories to the DataFrame
    df['category'] = df['app'].map(app_categories).fillna('Other')
    
    # Optional: Add hierarchical categories
    parent_categories = {
        'Development': 'Productive',
        'Marketing': 'Productive',
        'Creative': 'Productive',
        'Social Media': 'Distracting',
        'Entertainment': 'Distracting',
        'Utility': 'Neutral',
        'Browsing': 'Neutral',
        'AI Productivity': 'Productive',
        'Other': 'Unknown'
    }
    df['parent_category'] = df['category'].map(parent_categories).fillna('Other')

    return df