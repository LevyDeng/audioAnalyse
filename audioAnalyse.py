import pylab
import wave
import pyaudio
import numpy
import os

AUDIOFILE="raw/a5m.wav"

class audioAnalyse():

    def __init__(self,file):
        wf=wave.open(file,"rb")
        p=pyaudio.PyAudio()
        stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),\
                      channels=wf.getnchannels(),\
                      rate=wf.getframerate(),\
                      output=True)
        self.nframes=wf.getnframes()
        self.framerate=wf.getframerate()
        self.str_data=wf.readframes(self.nframes)
        wf.close()

        wave_data=numpy.fromstring(self.str_data,dtype=numpy.short)
        wave_data.shape=-1,2
        self.wave_data=wave_data.T

    def graph(self):
        time=numpy.arange(0,self.nframes)*(1.0/self.framerate)
        pylab.plot(time,self.wave_data[0])
        pylab.subplot(212)
        pylab.plot(time,self.wave_data[1],c="g")
        pylab.xlabel("time (secoonds)")
        pylab.show()

    def graph2(self):
        N=self.framerate
        n=0
        df=self.framerate/(N-1)
        freq=[df*n for n in range(0,N)]
        wave_data2=self.wave_data[0][N*n:N*(n+1)]
        c=numpy.fft.fft(wave_data2)*2/N
        d=int(len(c)/2)
        while freq[d]>4000:
            d -= 10
            pylab.plot(freq[:d-1],abs(c[:d-1]),'r')
        pylab.show()

    def graph3(self):
        time=int(4*self.nframes/self.framerate)
        N=11025
        df = self.framerate / (4*(N - 1))
        freq = [df * n for n in range(0, N)]
        x=[]
        y=[]
        for i in range(time):
            wave_data2 = self.wave_data[0][N * i:N * (i + 1)]
            #c = numpy.fft.fft(wave_data2) * 2 / N
            if wave_data2.__len__()!=0:
                y.append(max(abs(wave_data2)))
            else:
                y.append(0)
            x.append(i)
        pylab.plot(x,y)
        return max(y)
        #pylab.show()

def getFreq():
    files = os.listdir("raw")
    res = {}
    for f in files:
        au = audioAnalyse("raw/" + f)
        res[f.split(".")[0]] = au.graph3()
    print(res)

if __name__=="__main__":
    getFreq()


