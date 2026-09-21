#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Детектор брака по одной картинке.

Правило простое: если доля "красных" пикселей в кадре превышает порог —
считаем, что это DEFECT (брак), иначе OK (норма).

Запуск:
    python3 detect.py путь/к/файлу.png [--threshold 0.15]
"""

import sys
import argparse
from PIL import Image

# Порог доли красных пикселей, после которого считаем деталь бракованной
DEFAULT_THRESHOLD = 0.15


def is_red_pixel(r: int, g: int, b: int) -> bool:
    """Пиксель считается 'красным', если красный канал заметно выше
    зелёного и синего (а не просто светлый/белый)."""
    return r > 120 and r > g * 1.5 and r > b * 1.5


def red_ratio(image: Image.Image) -> float:
    img = image.convert("RGB")
    width, height = img.size
    pixels = img.load()
    total = width * height
    red_count = 0
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            if is_red_pixel(r, g, b):
                red_count += 1
    return red_count / total if total else 0.0


def classify(path: str, threshold: float = DEFAULT_THRESHOLD) -> str:
    image = Image.open(path)
    ratio = red_ratio(image)
    verdict = "DEFECT" if ratio >= threshold else "OK"
    return verdict, ratio


def main():
    parser = argparse.ArgumentParser(description="Определить брак по фото (доля красного цвета)")
    parser.add_argument("image", help="путь к файлу изображения (ok.png / defect.png / своё фото)")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                         help=f"порог доли красных пикселей (по умолчанию {DEFAULT_THRESHOLD})")
    args = parser.parse_args()

    verdict, ratio = classify(args.image, args.threshold)
    print(f"Файл: {args.image}")
    print(f"Доля красных пикселей: {ratio:.1%}")
    print(f"Результат: {verdict}")


if __name__ == "__main__":
    main()
