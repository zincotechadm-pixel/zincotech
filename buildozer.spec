[app]

title = Zincotech
package.name = zincotech
package.domain = org.zincotech

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,db,pdf

version = 1.0

requirements = python3,kivy,pillow,reportlab

orientation = portrait

fullscreen = 0

icon.filename = logo.png

presplash.filename = fundo_home.png

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21

android.archs = arm64-v8a, armeabi-v7a

log_level = 2

warn_on_root = 1


[buildozer]

log_level = 2

warn_on_root = 1