import os
import shutil

# Source directories
icon_base = 'resources/android/icon'
splash_base = 'resources/android/splash'
values_base = 'resources/values'

# Target directory (Android platform)
platform_res = 'platforms/android/app/src/main/res'

# 1. Copy Colors (for Adaptive Icon Background)
if os.path.exists(os.path.join(values_base, 'colors.xml')):
    os.makedirs(os.path.join(platform_res, 'values'), exist_ok=True)
    shutil.copy(os.path.join(values_base, 'colors.xml'), os.path.join(platform_res, 'values/colors.xml'))
    print("Copied values/colors.xml")

# 2. Copy Adaptive Icons (Foreground/Background)
adaptive_map = {
    'ldpi': 'mipmap-ldpi',
    'mdpi': 'mipmap-mdpi',
    'hdpi': 'mipmap-hdpi',
    'xhdpi': 'mipmap-xhdpi',
    'xxhdpi': 'mipmap-xxhdpi',
    'xxxhdpi': 'mipmap-xxxhdpi',
}

for density, mipmap_folder in adaptive_map.items():
    # Foreground
    fg_src = os.path.join(icon_base, f'{density}-foreground.png')
    fg_target = os.path.join(platform_res, mipmap_folder, 'ic_launcher_foreground.png')
    if os.path.exists(fg_src):
        os.makedirs(os.path.dirname(fg_target), exist_ok=True)
        shutil.copy(fg_src, fg_target)
        print(f"Copied {fg_src} to {fg_target}")

    # Background
    bg_src = os.path.join(icon_base, f'{density}-background.png')
    bg_target = os.path.join(platform_res, mipmap_folder, 'ic_launcher_background.png')
    if os.path.exists(bg_src):
        os.makedirs(os.path.dirname(bg_target), exist_ok=True)
        shutil.copy(bg_src, bg_target)
        print(f"Copied {bg_src} to {bg_target}")

    # Standard Icon (ic_launcher.png) - Overwrite existing
    icon_src = os.path.join(icon_base, f'drawable-{density}-icon.png')
    icon_target = os.path.join(platform_res, mipmap_folder, 'ic_launcher.png')
    if os.path.exists(icon_src):
        shutil.copy(icon_src, icon_target)
        print(f"Copied {icon_src} to {icon_target}")

# 3. Update 'smallicon' in Resources (to satisfy config.xml resource-file copy)
# Map drawable-density to simplified density name if needed
smallicon_map = {
    'ldpi': 'ldpi',
    'mdpi': 'mdpi',
    'hdpi': 'hdpi',
    'xhdpi': 'xhdpi',
    'xxhdpi': 'xxhdpi', # config.xml might not have all, but we update what we can
    'xxxhdpi': 'xxxhdpi'
}

for density in smallicon_map:
    # Source is our new generated icon
    new_icon = os.path.join(icon_base, f'drawable-{density}-icon.png')
    # Target is the 'smallicon' in resources folder
    target_smallicon = os.path.join(icon_base, f'drawable-{density}-smallicon.png')

    if os.path.exists(new_icon):
        # We copy our NEW icon to overwrite usage of 'smallicon'
        shutil.copy(new_icon, target_smallicon)
        print(f"Updated {target_smallicon} with new icon")

# 4. Copy Legacy Splash Screens (drawable-port-*, drawable-land-*)
# cordova-res generates: drawable-port-hdpi-screen.png, etc. inside 'resources/android/splash'
# OR it might be folder based. Let's check listing logic.
# Based on typical cordova-res: resources/android/splash/drawable-port-hdpi-screen.png
# We need to copy to: platforms/android/app/src/main/res/drawable-port-hdpi/screen.png

if os.path.exists(splash_base):
    for filename in os.listdir(splash_base):
        if filename.endswith('.png'):
            # Example: drawable-port-hdpi-screen.png
            # We need to extract folder name: drawable-port-hdpi
            parts = filename.split('-screen.png')
            if len(parts) > 0:
                folder_name = parts[0]
                target_folder = os.path.join(platform_res, folder_name)
                target_file = os.path.join(target_folder, 'screen.png')

                src_file = os.path.join(splash_base, filename)

                os.makedirs(target_folder, exist_ok=True)
                shutil.copy(src_file, target_file)
                print(f"Copied splash {src_file} to {target_file}")

print("Resource update complete.")
