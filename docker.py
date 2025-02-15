import platform
# Override platform.machine to return a valid CPU architecture.
# Change "aarch64" to "x86_64" if that better reflects your intended architecture.
platform.machine = lambda: "x86_64"
import app
