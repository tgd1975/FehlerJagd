from fjp0.audio import Clip, read_wav, silence, tone, write_wav


def test_roundtrip_wav(tmp_path):
    clip = tone(440, 0.25, sample_rate=16000, amplitude=0.5)
    path = tmp_path / "a.wav"
    write_wav(path, clip)
    back = read_wav(path)
    assert back.sample_rate == 16000
    assert abs(back.duration_s - 0.25) < 1e-3
    # 16-bit-Quantisierung → kleine Abweichung erlaubt.
    assert abs(back.rms() - clip.rms()) < 0.01


def test_tone_rms_positive_silence_zero():
    assert tone(220, 0.2, amplitude=0.3).rms() > 0.1
    assert silence(0.2).rms() == 0.0


def test_duration_and_empty():
    assert Clip([], 16000).duration_s == 0.0
    assert Clip([], 16000).rms() == 0.0
    assert Clip([0.0] * 16000, 16000).duration_s == 1.0


def test_stereo_downmix(tmp_path):
    import struct, wave
    path = tmp_path / "stereo.wav"
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(16000)
        # links = +amp, rechts = -amp → Mittel = 0
        frames = struct.pack("<" + "h" * 4, 1000, -1000, 1000, -1000)
        w.writeframes(frames)
    clip = read_wav(path)
    assert clip.sample_rate == 16000
    assert max(abs(s) for s in clip.samples) < 1e-6
