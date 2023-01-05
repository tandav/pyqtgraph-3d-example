# import dataclasses
# import functools
# from musictool.note import SpecificNote
# import mido
# import heapq
#
#
# @dataclasses.dataclass(frozen=True)
# @functools.total_ordering
# class MidiNote:
#     note: SpecificNote
#     on: float
#     off: float
#     track: int
#
#     def __eq__(self, other): return self.on == other.on
#     def __lt__(self, other): return self.on < other.on
#     def __hash__(self): return hash((self.note, self.track))
#
#
# def parse_notes_seconds(m: mido.MidiFile, bpm: float = 120) -> list[MidiNote]:
#     notes: list[MidiNote] = []
#     for track_i, track in enumerate(m.tracks):
#         seconds = 0.
#         t_buffer = {}
#         for message in track:
#             d_seconds = mido.tick2second(message.time, m.ticks_per_beat, mido.bpm2tempo(bpm))
#             seconds += d_seconds
#
#             if message.type == 'note_on' and message.velocity != 0:
#                 t_buffer[message.note] = seconds
#
#             elif message.type == 'note_off' or (
#                     message.type == 'note_on' and message.velocity == 0):  # https://stackoverflow.com/a/43322203/4204843
#                 heapq.heappush(notes, MidiNote(
#                     note=SpecificNote.from_absolute_i(message.note),
#                     on=t_buffer.pop(message.note), off=seconds,
#                     track=track_i,
#                 ))
#     return notes
