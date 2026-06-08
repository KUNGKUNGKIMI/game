#!/usr/bin/env python3
"""生成简单的游戏音效文件"""
import wave
import struct
import math
import os

def generate_wav(filename, samples, sample_rate=22050):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f'{len(samples)}h', *samples))

def generate_eat_sound():
    """短促上升音 - 吃食物"""
    sample_rate = 22050
    duration = 0.15
    n_samples = int(sample_rate * duration)
    samples = []
    for i in range(n_samples):
        t = i / sample_rate
        freq = 400 + (800 - 400) * (i / n_samples)
        val = 12000 * math.sin(2 * math.pi * freq * t)
        # 快速淡出
        val *= (1 - i / n_samples) ** 2
        samples.append(max(-32768, min(32767, int(val))))
    return samples, sample_rate

def generate_game_over_sound():
    """低沉下降音 - 游戏结束"""
    sample_rate = 22050
    duration = 0.8
    n_samples = int(sample_rate * duration)
    samples = []
    for i in range(n_samples):
        t = i / sample_rate
        freq = 250 - (200) * (i / n_samples)
        val = 10000 * math.sin(2 * math.pi * freq * t)
        # 淡出
        val *= (1 - i / n_samples) ** 1.5
        samples.append(max(-32768, min(32767, int(val))))
    return samples, sample_rate

def main():
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'sounds')
    os.makedirs(assets_dir, exist_ok=True)
    
    # 生成吃食物音效
    samples, rate = generate_eat_sound()
    generate_wav(os.path.join(assets_dir, 'eat.wav'), samples, rate)
    print(f"✅ Generated eat.wav ({len(samples)} samples)")
    
    # 生成游戏结束音效
    samples, rate = generate_game_over_sound()
    generate_wav(os.path.join(assets_dir, 'game_over.wav'), samples, rate)
    print(f"✅ Generated game_over.wav ({len(samples)} samples)")
    
    print("🎵 所有音效生成完成！")

if __name__ == '__main__':
    main()
