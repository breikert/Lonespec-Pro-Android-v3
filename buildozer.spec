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
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a

# Viktigt: tvinga Buildozer att använda en stabil version
# så den inte försöker hämta Build-Tools 37.
android.accept_sdk_license = True
android.build_tools_version = 35.0.0
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
