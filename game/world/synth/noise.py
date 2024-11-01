"""
Module name: noise

This module defines the noise algorithm for the map generation.
"""

from math import cos, pi
from random import randint, uniform


class PerlinNoise:
    """
    Class for creating an instance of the perlin noise algorithm.
    """

    NOISE_INTENSITY_RANGE = 2**16
    FREQ_ALTER_RANGE = 0.04

    def __init__(self) -> None:
        self._permutations = list()
        self._persistence = randint(15, 20)
        self._octaves = 5
        self._noise_intensity = randint(-PerlinNoise.NOISE_INTENSITY_RANGE, PerlinNoise.NOISE_INTENSITY_RANGE)
        self._frequency = 0.40 + uniform(-PerlinNoise.FREQ_ALTER_RANGE, PerlinNoise.FREQ_ALTER_RANGE)

    def generate(self, x: int, y: int) -> int:
        """
        Generate and return perlin noise data.
        """
        result = 0
        for i in range(self._octaves - 1):
            freq = self._frequency ** i
            amplitude = self._persistence ** i
            result += self.interpolate_noise(x * freq, y * freq) * amplitude
        return result

    def noise(self, x: int, y: int) -> float:
        """
        Noise function.
        """
        n: int = x + y * self._noise_intensity
        n = (n << 13) ^ n
        return 1.0 - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0

    def smooth_noise(self, x: int, y: int) -> float:
        """
        Smooth noise function.
        """
        return ((self.noise(x - 1, y - 1) + self.noise(x + 1, y - 1) + self.noise(x - 1, y + 1)) / 16
                + (self.noise(x - 1, y) + self.noise(x + 1, y) + self.noise(x, y - 1) + self.noise(x, y + 1)) / 8
                + self.noise(x, y) / 4)

    @staticmethod
    def cosine_interpolate(a: float, b: float, x: float) -> float:
        """
        Cosine interpolation.
        """
        ft = x * pi
        f = (1 - cos(ft)) * 0.5
        return a * (1 - f) + b * f

    def interpolate_noise(self, x: float, y: float) -> float:
        """
        Interpolate noise.
        """
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
        """
        Set the permutations.
        """
        self._permutations = permutations

    def get_permutations(self) -> list | tuple:
        """
        Return the permutations.
        """
        return self._permutations

    def set_noise_intensity(self, noise_intensity: int):
        """
        Set the noise intensity.
        """
        self._noise_intensity = noise_intensity

    def get_noise_intensity(self) -> int:
        """
        Return the noise intensity.
        """
        return self._noise_intensity

    def set_frequency(self, frequency: float):
        """
        Set the frequency.
        """
        self._frequency = frequency

    def get_frequency(self) -> float:
        """
        Return the frequency.
        """
        return self._frequency
