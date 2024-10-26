import numpy as np


class okcolor:
    def __init__(self, color):
        if isinstance(color, str) and color.startswith("#"):
            self.hex = color.upper()
            self.rgb = self.hex_to_rgb(self.hex)
            self.oklch = self.rgb_to_oklch(self.rgb)
            self.luminance = self.calculate_relative_luminance(self.rgb)
        else:
            self.oklch = color
            self.rgb = self.oklch_to_rgb(self.oklch)
            self.hex = self.rgb_to_hex(self.rgb)
            self.luminance = self.calculate_relative_luminance(self.rgb)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return np.array([int(hex_color[i : i + 2], 16) / 255.0 for i in (0, 2, 4)])

    def rgb_to_hex(self, rgb):
        if isinstance(rgb, str):
            return rgb
        return "#{:02x}{:02x}{:02x}".format(
            int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
        ).upper()

    def oklch_to_oklab(self, oklch):
        L, C, H = oklch
        H_rad = np.radians(H)
        a = C * np.cos(H_rad)
        b = C * np.sin(H_rad)
        return (L, a, b)

    def oklab_to_linear_rgb(self, oklab):
        L, a, b = oklab
        lms = np.array(
            [
                L + 0.3963377774 * a + 0.2158037573 * b,
                L - 0.1055613458 * a - 0.0638541728 * b,
                L - 0.0894841775 * a - 1.2914855480 * b,
            ]
        )
        lms = lms**3
        M_inv = np.array(
            [
                [4.0767416621, -3.3077115913, 0.2309699292],
                [-1.2684380046, 2.6097574011, -0.3413193965],
                [-0.0041960863, -0.7034186147, 1.7076147010],
            ]
        )

        return M_inv @ lms

    def linear_rgb_to_srgb(self, rgb):
        if isinstance(rgb, str) or np.any(rgb < 0):
            return "can not convert"
        srgb = np.where(
            rgb <= 0.0031308, 12.92 * rgb, 1.055 * (rgb ** (1 / 2.4)) - 0.055
        )
        return np.clip(srgb, 0, 1)

    def srgb_to_linear_rgb(self, srgb):
        if isinstance(srgb, str) or np.any(srgb < 0):
            return "can not convert"
        linear_rgb = np.where(
            srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4
        )
        return np.clip(linear_rgb, 0, 1)

    def oklch_to_rgb(self, oklch):
        oklab = self.oklch_to_oklab(oklch)
        linear_rgb = self.oklab_to_linear_rgb(oklab)
        return self.linear_rgb_to_srgb(linear_rgb)

    def rgb_to_oklab(self, rgb):
        linear_rgb = self.srgb_to_linear_rgb(rgb)
        M = np.array(
            [
                [0.4121656120, 0.5362752080, 0.0514575653],
                [0.2118591070, 0.6807189570, 0.1074065790],
                [0.0883097947, 0.2818474174, 0.6302613616],
            ]
        )
        lms = (M @ linear_rgb) ** (1 / 3)
        L = 0.2104542553 * lms[0] + 0.7936177850 * lms[1] - 0.0040720468 * lms[2]
        a = 1.9779984951 * lms[0] - 2.4285922050 * lms[1] + 0.4505937099 * lms[2]
        b = 0.0259040371 * lms[0] + 0.7827717662 * lms[1] - 0.8086757660 * lms[2]
        return (L, a, b)

    def rgb_to_oklch(self, rgb):
        oklab = self.rgb_to_oklab(rgb)
        L = oklab[0]
        C = np.sqrt(oklab[1] ** 2 + oklab[2] ** 2)
        H = np.degrees(np.arctan2(oklab[2], oklab[1])) % 360
        return (L, C, H)

    def calculate_relative_luminance(self, rgb):
        rgb_linear = self.srgb_to_linear_rgb(rgb)
        if isinstance(rgb_linear, str):
            return rgb_linear
        return 0.2126 * rgb_linear[0] + 0.7152 * rgb_linear[1] + 0.0722 * rgb_linear[2]
