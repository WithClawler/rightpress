#!/usr/bin/env python3
"""Prepare Play listing images from RightPress's existing vector and screenshots.

Requires Pillow. No generated artwork or device screenshot retouching is used.
Run from any directory: python3 tools/prepare_play_store.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ANDROID = "{http://schemas.android.com/apk/res/android}"


def color(value: str) -> tuple[int, int, int, int]:
    text = value.removeprefix("#")
    if len(text) == 6:
        return tuple(bytes.fromhex(text)) + (255,)
    if len(text) == 8:
        alpha, red, green, blue = bytes.fromhex(text)
        return red, green, blue, alpha
    raise ValueError(f"Unsupported vector color: {value}")


def paths(data: str) -> list[tuple[list[tuple[float, float]], bool]]:
    """Flatten the absolute M/H/V/C/Z commands present in the approved icon."""
    tokens = re.findall(r"[A-Za-z]|[-+]?(?:\d*\.\d+|\d+)", data)
    output = []
    points = []
    current = (0.0, 0.0)
    index = 0
    command = None

    def values(count: int) -> list[float]:
        nonlocal index
        result = [float(v) for v in tokens[index:index + count]]
        if len(result) != count:
            raise ValueError("Incomplete vector command")
        index += count
        return result

    while index < len(tokens):
        if tokens[index].isalpha():
            command = tokens[index]
            index += 1
        if command == "M":
            if points:
                output.append((points, False))
            current = tuple(values(2))
            points = [current]
            command = "L"
        elif command == "L":
            current = tuple(values(2))
            points.append(current)
        elif command == "H":
            current = values(1)[0], current[1]
            points.append(current)
        elif command == "V":
            current = current[0], values(1)[0]
            points.append(current)
        elif command == "C":
            x1, y1, x2, y2, x3, y3 = values(6)
            x0, y0 = current
            for step in range(1, 65):
                t = step / 64
                a = 1 - t
                points.append((a**3*x0 + 3*a*a*t*x1 + 3*a*t*t*x2 + t**3*x3,
                               a**3*y0 + 3*a*a*t*y1 + 3*a*t*t*y2 + t**3*y3))
            current = x3, y3
        elif command == "Z":
            output.append((points, True))
            points = []
            command = None
        else:
            raise ValueError(f"Unsupported vector command: {command}")
    if points:
        output.append((points, False))
    return output


def render_icon(source: Path) -> Image.Image:
    vector = ET.parse(source).getroot()
    viewport = float(vector.attrib[ANDROID + "viewportWidth"])
    assert viewport == float(vector.attrib[ANDROID + "viewportHeight"])
    size = 512
    supersample = 4
    scale = size * supersample / viewport
    image = Image.new("RGBA", (size * supersample, size * supersample))
    draw = ImageDraw.Draw(image)
    for path in vector:
        fill = color(path.attrib.get(ANDROID + "fillColor", "#00000000"))
        stroke = color(path.attrib.get(ANDROID + "strokeColor", "#00000000"))
        width = round(float(path.attrib.get(ANDROID + "strokeWidth", "0")) * scale)
        for coordinates, closed in paths(path.attrib[ANDROID + "pathData"]):
            scaled = [(x * scale, y * scale) for x, y in coordinates]
            if fill[3]:
                draw.polygon(scaled, fill=fill)
            if stroke[3] and width:
                if closed:
                    scaled.append(scaled[0])
                draw.line(scaled, fill=stroke, width=width)
                # Pillow leaves seams between short, thick curve segments.
                # Union small discs at internal vertices to close those seams.
                radius = width / 2
                for x, y in scaled[1:-1]:
                    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=stroke)
    return image.resize((size, size), Image.Resampling.LANCZOS)


def font(path: str | None, bold: bool, size: int) -> ImageFont.FreeTypeFont:
    candidates = ([Path(path)] if path else []) + [
        Path("/System/Library/Fonts/Supplemental") / ("Arial Bold.ttf" if bold else "Arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    raise FileNotFoundError("Pass --font / --bold-font to use an installed font")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "output/play-store")
    parser.add_argument("--capture-version", default="1.0.0 (10)",
                        help="Version of the captured screenshots; do not infer it from current source")
    parser.add_argument("--font")
    parser.add_argument("--bold-font")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    vector = ROOT / "app/src/main/res/drawable/ic_rightpress.xml"
    icon = render_icon(vector)
    icon.save(output / "icon-512.png", optimize=True)

    screenshots = []
    for index, name in enumerate(("mouse", "keyboard"), start=1):
        source = ROOT / f"docs/images/{name}.png"
        image = Image.open(source).convert("RGB")
        width, height = image.size
        assert 320 <= min(width, height) <= max(width, height) <= 3840
        assert max(width, height) <= min(width, height) * 2
        destination = output / f"phone-{index:02d}-{name}.png"
        image.save(destination, optimize=True)
        # Export retains all screenshot pixels; only the alpha channel is removed.
        assert list(Image.open(destination).getdata()) == list(image.getdata())
        screenshots.append((source, image))

    # A listing composition of existing branding and actual app screens.
    feature = Image.new("RGB", (1024, 500), "#14181C")
    feature.paste(icon.resize((80, 80), Image.Resampling.LANCZOS), (48, 76))
    draw = ImageDraw.Draw(feature)
    draw.text((48, 190), "RightPress", font=font(args.bold_font, True, 64), fill="#EEF0F5")
    draw.text((50, 282), "Mouse actions.", font=font(args.font, False, 26), fill="#AAB3C1")
    draw.text((50, 321), "Keyboard shortcuts.", font=font(args.font, False, 26), fill="#AAB3C1")
    for x, (_, screenshot) in zip((572, 796), screenshots):
        feature.paste(screenshot.resize((200, 320), Image.Resampling.LANCZOS), (x, 90))
        draw.rectangle((x - 1, 89, x + 200, 410), outline="#344050", width=1)
    feature.save(output / "feature-1024x500.png", optimize=True)

    sources = [vector] + [entry[0] for entry in screenshots]
    records = []
    for path in sorted(output.glob("*.png")):
        image = Image.open(path)
        records.append({"file": path.name, "width": image.width, "height": image.height,
                        "mode": image.mode, "bytes": path.stat().st_size, "sha256": digest(path)})
    manifest = {
        "method": "Existing Android vector rasterization and screenshot reuse/composition; no generated artwork",
        "source_capture": f"docs/images: Android emulator, {args.capture_version}, actual B console UI",
        "screenshot_editing": "RGB format conversion only; no crop, stretch, or content edits",
        "sources": [{"file": str(path.relative_to(ROOT)), "sha256": digest(path)} for path in sources],
        "outputs": records,
        "phone_screenshot_minimums_checked": "2 files; each dimension 320..3840; long side <= 2x short side",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
