from ignis.widgets import Widget
from ignis.services.audio import AudioService

audio = AudioService.get_default()

class SpeakerButton(Widget.Button):
    def __init__(self):
        super().__init__(
            child=Widget.Icon(
                image=audio.speaker.bind('icon-name')
            ),
            tooltip_text=audio.speaker.bind(
                'volume',
                transform=lambda val: f'{str(val)}%' or 'Unavailable'
            )
        )
