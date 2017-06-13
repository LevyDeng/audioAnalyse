import pylab
import wave
import pyaudio
import numpy
import os

AUDIOFILE="audio/V.A. - Kaos.wav"
PIANOKEY=('a0','a0m','b0','c1','c1m','d1','d1m','e1','f1','f1m','g1','g1m','a1','a1m','b1', \
          'c2', 'c2m', 'd2', 'd2m', 'e2', 'f2', 'f2m', 'g2', 'g2m','a2','a2m','b2', \
          'c3', 'c3m', 'd3', 'd3m', 'e3', 'f3', 'f3m', 'g3', 'g3m', 'a3', 'a3m', 'b3', \
          'c4', 'c4m', 'd4', 'd4m', 'e4', 'f4', 'f4m', 'g4', 'g4m', 'a4', 'a4m', 'b4', \
          'c5', 'c5m', 'd5', 'd5m', 'e5', 'f5', 'f5m', 'g5', 'g5m', 'a5', 'a5m', 'b5', \
          'c6', 'c6m', 'd6', 'd6m', 'e6', 'f6', 'f6m', 'g6', 'g6m', 'a6', 'a6m', 'b6', \
          'c7', 'c7m', 'd7', 'd7m', 'e7', 'f7', 'f7m', 'g7', 'g7m', 'a7', 'a7m', 'b7','c8')

class audioAnalyse():

    def __init__(self,file):
        self.filename=file.split("\/")[-1]
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
        time = int( self.nframes / self.framerate)
        N=int(self.framerate)
        y = []
        for i in range(time):
            wave_data2 = self.wave_data[0][N * i:N * (i + 1)]
            c = numpy.fft.fft(wave_data2) * 2 / N
            if wave_data2.__len__() != 0:
                y.append(max(abs(c)))
            else:
                y.append(0)
        self.freqs=y
        self.timeline=range(time)

    def graph(self):
        time=numpy.arange(0,self.nframes)*(1.0/self.framerate)
        pylab.plot(time,self.wave_data[0])
        pylab.subplot(212)
        pylab.plot(time,self.wave_data[1],c="g")
        pylab.xlabel("time (secoonds)")
        pylab.show()

    def graph2(self):
        x=int(self.nframes/self.framerate)*4
        N = int(self.framerate/4 )
        y=[]
        for n in range(x):
            df=N/(N-1)
            freq=[df*m for m in range(0,N)]
            wave_data2=self.wave_data[0][N*n:N*(n+1)]
            c=numpy.fft.fft(wave_data2)*2/N
            d=int(len(c)/2)
            c=[abs(d) for d in c[:d] ]
            y.append(c.index(max(c))*4)
        freq_a0=27.5
        #print(y)
        with open(self.filename.split(".")[0]+"_freqs.txt",'w') as f:
            for yy in y:
                if yy<4400 and yy > 20:
                    key=numpy.log2(yy/27.5)
                    k=key*12+0.5
                    n=int(k)
                    print(k)
                    f.write(PIANOKEY[n]+"\n")
                else:
                    f.write('0'+"\n")

        pylab.plot(range(x),y)
        pylab.show()

    def graph3(self):
        pylab.plot(self.timeline,self.freqs)
        #pylab.show()

    def graph4(self):
        l=sorted(list(abs(self.wave_data[0])))
        x=range(1,20)
        y=l[-19:]
        pylab.plot(x,y)
        pylab.title(self.filename.split(".")[0])
        pylab.savefig(self.filename.split(".")[0])

def getFreq():
    files = os.listdir("raw")
    res = {}
    for f in files:
        au = audioAnalyse("raw/" + f)
        N=au.framerate
        wave_data2=au.wave_data[0][0:N]
        c=numpy.fft.fft(wave_data2)
        l=list(abs(c))
        l=l[:int(len(l)/2)]
        freq=l.index((max(l)))
        print(f.split(".")[0]+":")
        print(freq)
        res[f.split(".")[0]] = freq
    with open("raw_freq.txt",'w') as f:
        for k,v in res.items():
            f.write(str(k)+":"+str(v)+"\n")

if __name__=="__main__":
    au=audioAnalyse(AUDIOFILE)
    au.graph2()
    #for f in os.listdir("raw"):
    #    au=audioAnalyse("raw/"+f)
    #    au.graph4()
    #getFreq()

