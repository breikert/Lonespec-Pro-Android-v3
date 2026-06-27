[app]
title = Lönespec Pro
package.name = lonespecpro
package.domain = org.lonespecpro
source.dir = .
source.include_exts = py,png,jpg,kv,json,txt
version = 3.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

android.permissions =
android.api = 35

# Viktigt:
# API 23 gav kompileringsfel med preadv/pwritev i Python/remote_debugging.c.
# API 24 löser det och fungerar på Android 7.0 och senare.
android.minapi = 24

# Bygg bara arm64 för att minska byggtid och minska risken för fel.
# Moderna Android-telefoner, inklusive nyare Samsung, använder arm64.
android.archs = arm64-v8a

android.accept_sdk_license = True
android.build_tools_version = 35.0.0
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
