# -*- coding: utf-8 -*-
"""4.2.2. Krāsains, visi kopā, oktāvas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HEvdrY7VFu9Zxa79EENnv3_0UFEVuTT5
"""

!pip install music21;

#tiek ieimportētas nepieciešamās bibliotēkas
from music21 import instrument, note, stream
from google.colab import files
import matplotlib.pyplot as plt
import numpy as np

#fja, kas nosaka nošu garumu daļā, ja tam padod attēla daļas masīvu
def note_length (arr):
  dens = np.average(arr)/255
  #100/5=20% katram garumam
  if dens < 0.2 : return 4
  elif 0.2 <= dens < 0.4 : return 2
  elif 0.4 <= dens < 0.6 : return 1
  elif 0.6 <= dens < 0.8 : return 0.5
  else: return 0.25

#fja, kas nosaka nots augstumu (do mažorā), ja tam padod attēla daļas masīvu
def note_pitch (arr):
  dens = np.average(arr)/255
  #100/7=14.285...~14.3% notij
  if dens < 0.143 : return 0 #C
  elif 0.143 <= dens < 0.286 : return 2 #D
  elif 0.286 <= dens < 0.429 : return 4 #E
  elif 0.429 <= dens < 0.572 : return 5 #F
  elif 0.572 <= dens < 0.715 : return 7 #G
  elif 0.715 <= dens < 0.858 : return 9 #A
  else: return 11 #B

#fja, kas piešķir oktāvu, sākot ar vismazāk intensīvai krāsai zemāko, un uz augšu (2-4)
def determine_octave (red, green, blue):
  rgb_dens = [np.average(red)/255, 
              np.average(green)/255, 
              np.average(blue)/255]
  octaves = []
  rgb_sorted = sorted(rgb_dens)
  for i in range(len(rgb_sorted)):
    octaves.append(rgb_sorted.index(rgb_dens[i])+2)
  return octaves

#fja, kas sadala padoto 2D masīvu n vienādās daļās pa vertikālēm
def split_array (arr, n):
  x = arr.shape[0]
  y = int(arr.shape[1]/n)
  split_arr = np.empty([n,x,y])
  for i in range(n):
    split_arr[i] = arr[0:x, i*y:(i+1)*y]
  return split_arr

#fja nošu veidošanai
def create_music (arr, output_notes, oct):
  offset = 0
  #attēls tiek sadalīts 4 daļās
  arr_in_4 = split_array(arr, 4)
  
  #attēla daļas pa vienai tiek apstaigātas
  for arr_part in arr_in_4:
    #daļai tiek noteikts nots garums
    note_l = note_length(arr_part)

    #atkarībā no nots garuma, attēla daļa tiek sadalīta vēl sīkāk n daļās
    arr_part_in_n = split_array(arr_part,int(4/note_l))

    #katrai "apakšdaļai" tiek noteikts nots augstums un izveidots nots objekts
    for arr_subpart in arr_part_in_n:
      note_p = note_pitch(arr_subpart)
      #parametrs quarterLenght apzīmē nots garumu ceturtdaļās
      #offset ir nots atskaņošanas laiks attiecībā pret sākumu
      new_note = note.Note(note_p, quarterLength=note_l)
      new_note.offset = offset
      new_note.octave = oct
      new_note.storedInstrument = instrument.Piano()
      output_notes.append(new_note)
    
      #palielina offset katrā iterācijā, lai notis nepārklājas
      offset += note_l
  return output_notes

#fja MIDI faila generēšanai
def generate(pic, fn, download=True, printMIDI=False):
  #attēla krāsas tiek sadalītas pa slāņiem
  red=pic[:, :, 0]
  green=pic[:, :, 1]
  blue=pic[:, :, 2]

  #tiek noteiktas oktāvas krāsām
  octaves = determine_octave(red, green, blue)

  #tiek veikta nošu ģenerēšana pēc kārtas katram krāsu slānim
  output = []
  create_music(red, output, octaves[0])
  create_music(green, output, octaves[1])
  create_music(blue, output, octaves[2])  
  
  #ģenerēto nošu informācija tiek ierakstīta failā
  midi_stream = stream.Stream(output)
  midi_stream.write('midi', fp='{name}_422.mid'.format(name=fn.split('.')[0]))
  
  #ģenerētā MIDI faila lejuplāde
  if download == 1:
    files.download('{name}_422.mid'.format(name=fn.split('.')[0]))

  #ģenerēto nošu izprintēšana
  if printMIDI == 1:
    for element in output:
      print(element.nameWithOctave, element.offset, element.quarterLength)

#attēla augšupielāde
uploaded = files.upload()

#tiek nolasīts faila nosaukums un pats attēls
filename = list(uploaded.keys())[0]
uploaded_picture=plt.imread(filename)

#attēla masīvs tiek padots mūzikas ģenerēšanas fjai
generate(uploaded_picture, filename, 1, 1)

#iespēja attēlot attēlu, ja vajag
plt.imshow(uploaded_picture);