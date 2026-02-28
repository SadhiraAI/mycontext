#!/usr/bin/env python3
"""
Create animated GIFs from tutorial screenshots.

Usage:
  python create_tutorial_gif.py                    # Creates gifs from frames in ./frames/
  python create_tutorial_gif.py frames/*.png       # Creates from specific files
  python create_tutorial_gif.py -o flow.gif f1.png f2.png f3.png

Install: pip install Pillow
"""

import argparse
import glob
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow")
    sys.exit(1)


def create_gif(
    images: list[Path],
    output: Path,
    duration_ms: int = 800,
    loop: int = 0,
    resize: tuple[int, int] | None = None,
) -> None:
    """Create an animated GIF from a list of image paths."""
    if not images:
        print("No images provided.")
        sys.exit(1)

    frames = []
    for p in images:
        img = Image.open(p).convert("RGBA")
        if resize:
            img = img.resize(resize, Image.Resampling.LANCZOS)
        frames.append(img)

    # GIF doesn't support alpha; use white background for transparency
    if frames[0].mode == "RGBA":
        bg = Image.new("RGB", frames[0].size, (255, 255, 255))
        rgb_frames = []
        for f in frames:
            bg_copy = bg.copy()
            bg_copy.paste(f, mask=f.split()[3])
            rgb_frames.append(bg_copy)
        frames = rgb_frames

    frames[0].save(
        output,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=loop,
        optimize=True,
    )
    print(f"Created: {output} ({len(frames)} frames)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create tutorial GIFs from screenshots")
    parser.add_argument(
        "inputs",
        nargs="*",
        help="Image files or glob pattern (default: frames/*.png)",
    )
    parser.add_argument("-o", "--output", default="tutorial-flow.gif", help="Output GIF path")
    parser.add_argument("-d", "--duration", type=int, default=800, help="Frame duration in ms")
    parser.add_argument("--resize", type=str, help="Resize to WxH (e.g. 800x600)")
    args = parser.parse_args()

    base = Path(__file__).parent
    if args.inputs:
        images = []
        for pat in args.inputs:
            p = Path(pat)
            if "*" in pat:
                images.extend(sorted(p.parent.glob(p.name)))
            else:
                images.append(p)
        images = sorted(set(Path(str(x)).resolve() for x in images))
    else:
        frames_dir = base / "frames"
        frames_dir.mkdir(exist_ok=True)
        images = sorted(frames_dir.glob("*.png"))
        if not images:
            print(
                f"No images found. Add PNG screenshots to {frames_dir}/ "
                "or pass files: python create_tutorial_gif.py frame1.png frame2.png"
            )
            sys.exit(1)

    resize = None
    if args.resize:
        w, h = map(int, args.resize.split("x"))
        resize = (w, h)

    out = Path(args.output)
    if not out.is_absolute():
        out = base / out

    create_gif(images, out, duration_ms=args.duration, resize=resize)


if __name__ == "__main__":
    main()
