"""
TODO: rewrite some strings eg CA,B, CAB, here CAB should be renamed to CBA
"""
import random
import time
import numpy as np
import pandas as pd
import pyqtgraph.opengl as gl
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QLabel
# from pyqtgraph.Qt import QtCore, QtGui
from PyQt6.QtGui import QFont
from PyQt6 import QtGui
import pyqtgraph as pg
import sys
import pickle
import json
import asyncio
import itertools
from functools import partial
from pathlib import Path
from musiclib.chord import SpecificChord
from musiclib.noteset import NoteSet
from musiclib.scale import Scale
from musiclib.note import SpecificNote
from musiclib.midi import player
import mido
import collections


import config
import util
import os
import enum

class State(enum.Enum):
    READY = 0
    WAITING = 1
    DONE = 2


if midi_device := os.environ.get('MIDI_DEVICE'):
    port = mido.open_output(midi_device)


scale = Scale.from_name('C', 'major')
GREEN_COLOR = 127, 255, 127, 255
RED_COLOR = 255, 0, 0, 255
BPM = 30

midi = mido.MidiFile('harmony.mid', type=1)
# track = util.parse_notes_seconds(midi, bpm=120)
track = midi.tracks[0]
# miditrack = [
#     MidiNote(
#         note.note,
#         mido.tick2second(note.on, midi.ticks_per_beat, BPM),
#         mido.tick2second(note.off, midi.ticks_per_beat, BPM),
#         note.track,
#     )
#     for note in parse_notes(midi)
# ]



def fit(v, oldmin, oldmax, newmin=0.0, newmax=1.0):
    return (v - oldmin) * (newmax - newmin) / (oldmax - oldmin) + newmin


# class MyGLViewWidget(gl.GLViewWidget):
#     """ Override GLViewWidget with enhanced behavior and Atom integration
#     """
#
#     def mouseMoveEvent(self, ev):
#         print(ev.pos())
#         super().mouseMoveEvent(ev)
#

class Window(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        pg.setConfigOption('background', (12, 0, 53))
        # pg.setConfigOption('background', 'w')
        # pg.setConfigOption('foreground', 'k')
        
        self.setWindowTitle('Earth Cities')

        # self.data_file = Path('X.csv')
        # self.data_file = Path('X3.csv')
        # self.data_file = Path('tiers.json')
        self.data_file_mtime = None
        self.n_range = 1000
        self.chord_to_text = {}
        # self.playing_notes = {}
        self.playing_notes = set()

        self.w = gl.GLViewWidget()
        # self.w = MyGLViewWidget()

        # self.w.mouseMoveEvent
        # self.sp = QSlider(orientation=Qt.Orientation.Horizontal)
        # sliders_width = 300
        # self.sp.setFixedWidth(sliders_width)

        self.values = dict()
        self.sliders = dict()
        self.labels = dict()
        self.ranges = {
            'z': (-5, 5),
            'radius': (0, 5),
            'angle': (-np.pi, + np.pi),
        }

        self.play_button = QPushButton('play')
        # self.play_button.clicked.connect(self.play)
        # self.t_start = time.monotonic()
        self.message_i = 0
        self.t = time.monotonic()
        # self.t_sleep = 0
        self.state = State.WAITING

        self.noteset = None
        self.queue = collections.deque(maxlen=4)


        self.layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.right_layout.addWidget(self.play_button)

        self.left_layout.addWidget(self.w)
        # self.right_layout.addWidget(self.sp)
        self.layout.addLayout(self.left_layout)
        # self.layout.addLayout(self.right_layout)

        # layout = QVBoxLayout()
        # self.layout.addWidget(self.w)

        self.setLayout(self.layout)
        self.setGeometry(0, 0, 2500, 1600)
        self.w.setCameraPosition(distance=40)

        # self.make_sliders()
        self.update()
        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.update)
        # self.timer.start(1000)

        self.player_timer = pg.QtCore.QTimer()
        self.player_timer.timeout.connect(self.play)
        self.player_timer.start(0)
        # self.play()

    def mouseMoveEvent(self, event):
        """
        The Qt event handler when the mouse is released

        Release potentially selected slicing planes.
        Then pass the event to the parent class

        :param QMouseEvent event: the qt mouse event
        """
        print(self.w.mouseMoveEvent(event))
        print(event)

    def play_new_chord(self):
        duration = 2 * random.random()
        chord = SpecificChord(frozenset(SpecificNote(note, octave=1) for note in random.sample(scale.notes_ascending, random.randint(2, 3))))
        print('playing', chord)
        t = time.monotonic()
        for note in chord:
            player.send_message('note_on', note=note.absolute_i, channel=0)
            self.playing_notes[note] = {'t_start': t, 'duration': duration, 'chord': chord}
        self.chord_to_text[chord.abstract].setData(color=RED_COLOR)

    def update_text(self):
        new_noteset = SpecificNote.to_abstract(self.playing_notes)

        if self.noteset is None:
            self.chord_to_text[new_noteset].setData(color=RED_COLOR)
            self.noteset = new_noteset
            return

        if new_noteset == self.noteset:
            return

        if t := self.chord_to_text.get(self.noteset):
            t.setData(color=GREEN_COLOR)
        if t := self.chord_to_text.get(new_noteset):
            t.setData(color=RED_COLOR)
        self.noteset = new_noteset


    def play(self):
        message = track[self.message_i]
        if self.state == State.READY:
            # m = mido.Message(type=message.type, )
            # port.send(m)
            if message.type in {'note_on', 'note_off'}:
                if message.type == 'note_on':
                    self.playing_notes.add(SpecificNote.from_i(message.note))
                elif message.type == 'note_off':
                    self.playing_notes.remove(SpecificNote.from_i(message.note))
                self.update_text()
                print(message)
                port.send(message)
            self.t = time.monotonic()
            if self.message_i + 1 == len(track):
                self.state = State.DONE
            else:
                self.message_i += 1
                self.state = State.WAITING
            # self.t_sleep = mido.tick2second(message.time, midi.ticks_per_beat, mido.bpm2tempo(BPM))
            self.state = State.WAITING
        elif self.state == State.WAITING:
            # if time.monotonic() < self.t + self.t_sleep:
            if time.monotonic() < self.t + mido.tick2second(message.time, midi.ticks_per_beat, mido.bpm2tempo(BPM)):
                return
            # if self.message_i + 1 == len(track):
            #     self.state = State.DONE
            #     return
            # self.message_i += 1
            self.state = State.READY
            # self.play()
        elif self.state == State.DONE:
            return
        else:
            raise ValueError



        # if len(self.playing_notes) < 3 and random.random() > 0.5:
        #     self.play_new_chord()
        #
        # t = time.monotonic()
        # notes_off = set()
        # chords_off = set()
        # for note, payload in self.playing_notes.items():
        #     if payload['t_start'] + payload['duration'] < t:
        #         player.send_message('note_off', note=note.absolute_i, channel=0)
        #         notes_off.add(note)
        #         chords_off.add(payload['chord'])
        #
        # for note in notes_off:
        #     del self.playing_notes[note]
        #
        # for chord in chords_off:
        #     self.chord_to_text[chord.abstract].setData(color=GREEN_COLOR)


    def add_axes_labels(self):
        self.axes_labels = []
        for ax in range(3):
            for note in config.noterange:
                pos = [0, 0, 0]
                pos[ax] = note.absolute_i
                t = gl.GLTextItem(
                    pos=pos,
                    color=GREEN_COLOR,
                    text=str(note),
                    font=QFont('SF Mono', 18),
                )
                # t.onC
                # t.valueChanged.connect(partial(self.slider_changed, tier, 'z'))

                # t.setData(pos=(row.x, row.y, row.z), color=GREEN_COLOR, text=str(note))
                self.w.addItem(t)

    def make_axes_grids(self, grid_shift = 50, grid_spacing = 1):
        gx = gl.GLGridItem(color=(255, 255, 255, 0.1))
        gx.setSize(grid_shift, grid_shift, grid_shift)
        gx.rotate(90, 0, 1, 0)
        gx.translate(-grid_shift/2, 0, grid_shift/2)
        gx.setSpacing(grid_spacing, grid_spacing, grid_spacing)
        self.w.addItem(gx)
        gy = gl.GLGridItem()
        gy.setSize(grid_shift, grid_shift, grid_shift)
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -grid_shift/2, grid_shift/2)
        gy.setSpacing(grid_spacing, grid_spacing, grid_spacing)
        self.w.addItem(gy)
        gz = gl.GLGridItem()
        gz.setSize(grid_shift, grid_shift, grid_shift)
        gz.setSpacing(grid_spacing, grid_spacing, grid_spacing)
        # gz.translate(0, 0, -grid_shift/2)
        self.w.addItem(gz)

    def update_plot(self):
        # data, index = [], []
        #
        # for tier in tiers:
        #     points_names = tier['points']
        #     index += points_names
        #     n = len(points_names)
        #
        #     points = []
        #     for i in range(n):
        #         points.append(tier['radius'] * np.exp(2j * np.pi * i / n))
        #     points = np.array(points)
        #     # rot = 2 * np.pi / tier['rotation'] if tier['rotation'] else 0
        #     rot = 2 * np.pi * tier['rotation']
        #     points = points * np.exp(1j * rot)
        #
        #     data += zip(points.real, points.imag, itertools.repeat(tier['z']))
        #
        # X = pd.DataFrame(data, index, columns=list('xyz'))

        # self.w.opts['viewport'] = (0, 0, 200, 300)
        # self.w.opts['distance'] = 150
        self.w.clear()
        self.make_axes_grids()
        self.add_axes_labels()

        self.main_scatter_plot = gl.GLScatterPlotItem()
        self.color = (1, 0.7, 0.4, 1)
        self.w.addItem(self.main_scatter_plot)


        # self.main_scatter_plot.setData(pos=self.X[list('xyz')].values, size=0.01, color=self.color, pxMode=False)

        # for row in self.X.itertuples():
        #     t = gl.GLTextItem(font=QFont('Helvetica', 18))
        #     t.setData(pos=(row.x, row.y, row.z), color=GREEN_COLOR, text=row.Index)
        #     self.chord_to_text[NoteSet.from_str(row.Index).notes] = t
        #     self.w.addItem(t)

        # for k, v in graph.items():
        # for vv in v:





app = QApplication(sys.argv)
gui = Window()
gui.show()
app.exec()
