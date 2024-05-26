import wave
import numpy as np
import matplotlib.pyplot as plt

def plot_wav_frequency_spectrum(fname, start=62000, duration=1.0):
    # WAVファイルを開く
    wfile = wave.open(fname, 'r')

    # WAVファイルの基本情報を取得
    numch = wfile.getnchannels()
    samplewidth = wfile.getsampwidth()
    samplerate = wfile.getframerate()
    numsamples = wfile.getnframes()

    print("チャンネル数 = ", numch)
    print("サンプル幅 (バイト数) = ", samplewidth)
    print("サンプリングレート(Hz) =", samplerate)
    print("サンプル数 =", numsamples)
    print("録音時間 =", numsamples / samplerate)

    # すべてのフレームを読み込む (bytesオブジェクトになる)
    buf = wfile.readframes(numsamples)
    wfile.close()

    # numpy の ndarray に変換する
    if samplewidth == 2:
        data = np.frombuffer(buf, dtype='int16')
        data = data / 32768.0
    elif samplewidth == 4:
        data = np.frombuffer(buf, dtype='int32')
        data = data / 2147483648.0

    # ステレオの場合は左チャンネルだけを取り出す
    if numch == 2:
        data = data[0::2]

    # 指定された位置から duration 秒分のデータを取り出し、範囲をチェックする
    N = int(samplerate * duration)
    end = start + N
    if end > len(data):
        end = len(data)
        start = end - N
        if start < 0:
            start = 0

    # 離散フーリエ変換する
    c = np.fft.fft(data[start:end])
    c = np.abs(c)

    # 結果をプロットする
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.title('Data')
    plt.plot(range(start, end), data[start:end])
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    plt.title('Frequency Spectrum')
    freqList = np.fft.fftfreq(N, d=1.0/samplerate)
    plt.plot(freqList[:N//2], c[:N//2], linestyle='-')  # この行だけでプロットします
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')

    plt.tight_layout()
    plt.show()

# 使用例
fname = 'KDark_16.wav'  # ここにWAVファイルのパスを入力してください
plot_wav_frequency_spectrum(fname, start=0, duration=1.0)  #　start duration を変更できます
