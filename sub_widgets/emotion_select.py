from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtWidgets import QComboBox

from acts_system.character_emotion import CharacterEmotion


class EmotionSelect(QComboBox):
    def __init__(self, emotion=CharacterEmotion.NEUTRAL, parent=None):
        super().__init__(parent)
        for emotion_ in CharacterEmotion:
            variant = QVariant(emotion_)
            self.addItem(str(emotion_), variant)

        self.set_emotion(emotion)

    def set_emotion(self, emotion):
        for idx in range(self.count()):
            emotion_ = self.itemData(idx, Qt.UserRole)
            if emotion_ == emotion:
                self.setCurrentIndex(idx)
                break

    def current_emotion(self):
        return self.currentData(Qt.UserRole)
