from __future__ import division
import wave
import random
import struct
import math

styles = {
    "norm": [[1, 1]],
    "org": [[1, 1], [2, 0.61], [3, 0.15]],
    "nirv": [[1, 0.5], [2**(7/12), 0.5], [2, 0.5]]
}

def styleChange(string):
    if string[0] == "#":
        result = [[1, 1]]
        if string[1] == "M":
            result.append([2**(1/3), 1])
        elif string[1] == "m":
            result.append([2**(1/4), 1])
        elif string[1] == "s":
            result.append([2**(5/12), 1])
        if string[2] == "p":
            result.append([2**(7/12), 1])
        elif string[2] == "d":
            result.append([2**(1/2), 1])
        elif string[2] == "a":
            result.append([2**(2/3), 1])
        if len(string) > 3:
            add = []
            for digit in range(3, len(string)):
                add.append(string[digit])
            result.append([2**(int("".join(add))/12), 1])
        return result
    else:
        return styles["".join(string)]

def note(frequencies, index, on):
    fs = []
    for f in frequencies:
        fs.append([float(f[0]), f[1]])
    return [fs, int(index), on]

def chord(notes, values, rate):
    i = 0
    while i < 88250/rate:
        value = 0
        for n in notes:
            for f in n[0]:
                value += math.sin((n[1]+i)/28160*f[0])*32756/len(notes)/len(n[0])*n[2]*f[1]
        packed_value = struct.pack('h', value)
        values.append(packed_value)
        i += 1
    return values

def song(name, volume, base, gap, transpose, scores):
    noise_output = wave.open(name + '.wav', 'w')
    noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
    rate = scores[0]
    del scores[0]
    values = []
    started = []
    startFreqs = []
    chars = []
    for i in range(len(scores)):
        started.append(False)
        startFreqs.append([])
    for s in range(len(scores)):
        for j in range(len(scores[s])):
            if scores[s][j] not in "1234567890.":
                started[s] = True
            if not started[s]:
                startFreqs[s].append(scores[s][j])
    freqs = []
    rates = []
    for freq in startFreqs:
        freqs.append([[float("".join(freq))*2**(transpose/base), 1]])
        rates.append(16)
    for i in range(len(scores)):
        chars.append(len(startFreqs[i]))
    tune = []
    for s in range(len(scores)):
        index = 0
        beat = 0
        done = False
        while not done:
            play = False
            if scores[s][chars[s]] == "*":
                if beat >= len(tune):
                    tune.append([note(freqs[s], index, 1)])
                else:
                    tune[beat].append(note(freqs[s], index, 1))
                chars[s] += 1
                play = True
            elif scores[s][chars[s]] == "/":
                if beat >= len(tune):
                    tune.append([note(freqs[s], index, 0)])
                else:
                    tune[beat].append(note(freqs[s], index, 0))
                chars[s] += 1
                play = True
            elif scores[s][chars[s]] == "[":
                num = []
                n = 1
                while scores[s][chars[s]+n] != "]":
                    num.append(scores[s][chars[s]+n])
                    n += 1
                chars[s] += n+1
                for f in range(len(freqs[s])):
                    freqs[s][f][0] *= gap**int("".join(num))
            elif scores[s][chars[s]] == "<":
                num = []
                n = 1
                while scores[s][chars[s]+n] != ">":
                    num.append(scores[s][chars[s]+n])
                    n += 1
                chars[s] += n+1
                rates[s] *= 2**int("".join(num))
            elif scores[s][chars[s]] == "{":
                string = []
                n = 1
                while scores[s][chars[s]+n] != "}":
                    string.append(scores[s][chars[s]+n])
                    n += 1
                chars[s] += n+1
                freq = freqs[s][0][0]
                newStyle = []
                for f in styleChange(string):
                    newStyle.append([freq*f[0], f[1]])
                freqs[s] = newStyle
            if play:
                beat += 1
            if chars[s] >= len(scores[s]):
                done = True
            index += 88250/rate
    for beat in range(len(tune)):
        print int((beat+1)/len(tune)*100),"%"
        values = chord(tune[beat], values, rate)
    value_str = ''.join(values)
    noise_output.writeframes(value_str)
    noise_output.close()
