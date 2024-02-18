from random import randint, uniform
from math import cos, pi


class PerlinNoise:

    NOISE_INTENSITY_RANGE = 2**16
    FREQ_ALTER_RANGE = 0.08

    def __init__(self):
        self._permutations = list()
        self._persistence = 20
        self._octaves = 5
        self._noise_intensity = randint(-PerlinNoise.NOISE_INTENSITY_RANGE, PerlinNoise.NOISE_INTENSITY_RANGE)
        self._frequency = 0.40 + uniform(-PerlinNoise.FREQ_ALTER_RANGE, PerlinNoise.FREQ_ALTER_RANGE)

    def generate(self, x: int, y: int):
        result = 0
        for i in range(self._octaves - 1):
            freq = self._frequency ** i
            amplitude = self._persistence ** i
            result += self.interpolate_noise(x * freq, y * freq) * amplitude
        return result

    def noise(self, x: int, y: int):
        n: int = x + y * self._noise_intensity
        n = (n << 13) ^ n
        return 1.0 - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0

    def smooth_noise(self, x: int, y: int):
        return ((self.noise(x - 1, y - 1) + self.noise(x + 1, y - 1) + self.noise(x - 1, y + 1)) / 16
                + (self.noise(x - 1, y) + self.noise(x + 1, y) + self.noise(x, y - 1) + self.noise(x, y + 1)) / 8
                + self.noise(x, y) / 4)

    def cosine_interpolate(self, a, b, x):
        ft = x * pi
        f = (1 - cos(ft)) * 0.5
        return a * (1 - f) + b * f

    def interpolate_noise(self, x: float, y: float):
        ix, iy = int(x), int(y)
        fx, fy = x - ix, y - iy
        v1 = self.smooth_noise(ix, iy)
        v2 = self.smooth_noise(ix + 1, iy)
        v3 = self.smooth_noise(ix, iy + 1)
        v4 = self.smooth_noise(ix + 1, iy + 1)

        interp1 = self.cosine_interpolate(v1, v2, fx)
        interp2 = self.cosine_interpolate(v3, v4, fx)

        return self.cosine_interpolate(interp1, interp2, fy)

    def set_permutations(self, permutations: list | tuple) -> None:
        self._permutations = permutations

    def get_permutations(self) -> list | tuple:
        return self._permutations

    def set_noise_intensity(self, noise_intensity):
        self._noise_intensity = noise_intensity

    def get_noise_intensity(self):
        return self._noise_intensity

    def set_frequency(self, frequency):
        self._frequency = frequency

    def get_frequency(self):
        return self._frequency
