from PySide6.QtCore import QObject, Signal

class LogSignalEmitter(QObject):
    log_message = Signal(str, str)  # (level, message)

# globales Signalobjekt
log_signals = LogSignalEmitter()
