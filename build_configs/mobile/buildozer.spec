[app]
title = Games Collection
domain = org.gamescollection
package.name = gamescollection
package.domain = org.gamescollection
source.dir = ../../
source.include_exts = py,png,jpg,kv,ttf,json,md
version = 2.0.1
requirements = python3,kivy,games-collection[mobile]
orientation = sensor
fullscreen = 0
presplash.filename = src/games_collection/assets/launcher/default_screenshot.png
icon.filename = src/games_collection/assets/launcher/default_thumbnail.png
android.permissions = INTERNET
android.release_keystore = %(ANDROID_KEYSTORE_PATH)s
android.release_keystore_pass = %(ANDROID_KEYSTORE_PASSWORD)s
android.release_keyalias = gamescollection
android.release_keyalias_pass = %(ANDROID_KEY_PASSWORD)s
android.gradle_dependencies = com.google.android.material:material:1.10.0

[buildozer]
log_level = 2
warn_on_root = 0
bin_dir = build/mobile/android/bin
# CI builds supply the keystore through $ANDROID_KEYSTORE_B64
# and decode it in the workflow before invoking buildozer.
