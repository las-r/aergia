# Aergia Syntax Highlighting for Notepad++

## Prerequisites
1. Open Notepad++.
2. Go to Plugins, Plugins Admin...
3. Search for Enhance AnyLexer, check the box, and click Install. 
4. Notepad++ will restart automatically to complete the installation.

## Installation Steps
### Step 1: Create the Aergia Language Profile
1. In the top menu, go to Language, User Defined Language, Define your language...
2. Click Create New... at the top, type `Aergia` (exactly as written), and click OK.
3. In the **Ext.:** box under the *Folder & Default* tab, type `aer` (do not include a period).
4. Close the User Defined Language panel.

### Step 2: Inject the Styles
1. Open any `.aer` file in Notepad++.
2. Ensure the language profile is active by going to Language (top menu), scrolling to the bottom, and clicking Aergia.
3. Go to the top menu and select Plugins, Enhance AnyLexer, Enhance current language.
4. A configuration file will open in a new tab. Replace all the text inside of it with the config found in `EnhancedAnyLexerConfig.ini` and save the file.

If you want, you can change the colors here to better fit your preferences. The provided ones are based off of the Tokyo Night theme.