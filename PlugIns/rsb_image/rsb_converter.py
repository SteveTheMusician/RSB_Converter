#!/usr/bin/env python3
"""
rsb_converter.py - Ghost Recon 2001 RSB Converter
Layout:
    [0]      28 Bytes    Header (version, width, height, RGBA bits)
    [28]     Pixel data  RGB 24-bit, Textur-Puffer (1024×512)
    [EOF-65] 65 Bytes    Texture Properties

Das eigentliche Bild ist kleiner als der Textur-Puffer (z.B. 640×480 in 1024×512).
Das Skript erkennt automatisch den sichtbaren Bereich und schneidet ihn zu.

Abhängigkeiten: pip install Pillow
"""

import struct
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("FEHLER: pip install Pillow")
    sys.exit(1)

HEADER_SIZE = 28
TEX_PROPS_SIZE = 65

def read_rsb(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    
    version = struct.unpack("<I", data[0:4])[0]
    tex_w  = struct.unpack("<I", data[4:8])[0]
    tex_h  = struct.unpack("<I", data[8:12])[0]
    r_bits = struct.unpack("<I", data[12:16])[0]
    g_bits = struct.unpack("<I", data[16:20])[0]
    b_bits = struct.unpack("<I", data[20:24])[0]
    a_bits = struct.unpack("<I", data[24:28])[0]
    bpp = (r_bits + g_bits + b_bits + a_bits) // 8
    
    pixel_data = data[HEADER_SIZE : HEADER_SIZE + tex_w * tex_h * bpp]
    
    return data, version, tex_w, tex_h, r_bits, g_bits, b_bits, a_bits, bpp, pixel_data

def detect_content_bbox(img):
    """Findet den sichtbaren Bereich (nicht-schwarz) in einem Bild."""
    # In Graustufen wandeln und Histogramm analysieren
    gray = img.convert("L")
    pixels = gray.load()
    w, h = img.size
    
    min_x, min_y = w, h
    max_x, max_y = 0, 0
    
    threshold = 10  # Alles unter 10 = schwarz
    
    for y in range(h):
        for x in range(w):
            if pixels[x, y] > threshold:
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
    
    if min_x > max_x or min_y > max_y:
        return None  # Komplett schwarz
    
    return (min_x, min_y, max_x + 1, max_y + 1)

def rsb_to_png(rsb_path, outdir):
    data, ver, tex_w, tex_h, rb, gb, bb, ab, bpp, pixel_data = read_rsb(rsb_path)
    
    print(f"Version:   {ver}")
    print(f"Textur:    {tex_w}×{tex_h} ({bpp*8}-bit)")
    print(f"Datei:     {len(data):,} Bytes")
    
    # Volles Bild aus Textur-Puffer
    if bpp == 3:
        full_img = Image.frombytes("RGB", (tex_w, tex_h), pixel_data, "raw", "RGB")
    elif bpp == 4:
        full_img = Image.frombytes("RGBA", (tex_w, tex_h), pixel_data, "raw", "RGBA")
    else:
        print(f"FEHLER: {bpp} Bytes/Pixel nicht unterstützt")
        return False
    
    # Automatisch schwarzen Rand erkennen
    print(f"\nSuche sichtbaren Bereich...")
    bbox = detect_content_bbox(full_img)
    
    if bbox:
        x1, y1, x2, y2 = bbox
        crop_w = x2 - x1
        crop_h = y2 - y1
        print(f"  Gefunden: {crop_w}×{crop_h} ab ({x1},{y1})")
        
        cropped = full_img.crop(bbox)
    else:
        print(f"  Kein sichtbarer Bereich gefunden, verwandle volle Textur")
        cropped = full_img
        crop_w, crop_h = tex_w, tex_h
        x1, y1 = 0, 0
    
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    stem = Path(rsb_path).stem
    
    # Normal speichern
    png_path = outdir / f"{stem}.png"
    cropped.save(str(png_path))
    print(f"\n✓ Gespeichert: {png_path}")
    print(f"  {crop_w}×{crop_h} aus {tex_w}×{tex_h} Textur (Offset {x1},{y1})")
    
    # Metadaten für to_rsb speichern
    meta_path = outdir / f"{stem}.meta"
    with open(meta_path, "w") as f:
        f.write(f"tex_width={tex_w}\n")
        f.write(f"tex_height={tex_h}\n")
        f.write(f"crop_x={x1}\n")
        f.write(f"crop_y={y1}\n")
        f.write(f"crop_w={crop_w}\n")
        f.write(f"crop_h={crop_h}\n")
        f.write(f"bpp={bpp}\n")
    print(f"  Metadaten: {meta_path}")
    
    return True

def png_to_rsb(png_path, rsb_path):
    """Konvertiert PNG zurück zu RSB, mit Padding auf Power-of-2."""
    img = Image.open(png_path)
    crop_w, crop_h = img.size
    
    # Metadaten laden (falls vorhanden)
    meta_path = Path(png_path).with_suffix(".meta")
    tex_w, tex_h, x_off, y_off = 1024, 512, 0, 0
    bpp = 3
    
    if meta_path.exists():
        with open(meta_path) as f:
            for line in f:
                key, val = line.strip().split("=")
                if key == "tex_width": tex_w = int(val)
                elif key == "tex_height": tex_h = int(val)
                elif key == "crop_x": x_off = int(val)
                elif key == "crop_y": y_off = int(val)
                elif key == "bpp": bpp = int(val)
        print(f"Metadaten geladen: Textur {tex_w}×{tex_h}, Offset ({x_off},{y_off})")
    else:
        # Automatisch kleinste PoT-Größe finden
        import math
        def next_pot(n):
            p = 1
            while p < n:
                p *= 2
            return p
        tex_w = next_pot(crop_w)
        tex_h = next_pot(crop_h)
        print(f"Keine Metadaten, verwende PoT: {tex_w}×{tex_h}")
    
    # Bild in Textur-Puffer einbetten (mit schwarzem Padding)
    if bpp == 4:
        full_buf = Image.new("RGBA", (tex_w, tex_h), (0, 0, 0, 0))
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        full_buf.paste(img, (x_off, y_off))
        pixel_data = full_buf.tobytes("raw", "RGBA")
        r_bits, g_bits, b_bits, a_bits = 8, 8, 8, 8
    else:
        full_buf = Image.new("RGB", (tex_w, tex_h), (0, 0, 0))
        if img.mode != "RGB":
            img = img.convert("RGB")
        full_buf.paste(img, (x_off, y_off))
        pixel_data = full_buf.tobytes("raw", "RGB")
        r_bits, g_bits, b_bits, a_bits = 8, 8, 8, 0
    
    # Header bauen
    header = bytearray(HEADER_SIZE)
    struct.pack_into("<I", header, 0, 6)        # version
    struct.pack_into("<I", header, 4, tex_w)    # width
    struct.pack_into("<I", header, 8, tex_h)    # height
    struct.pack_into("<I", header, 12, r_bits)
    struct.pack_into("<I", header, 16, g_bits)
    struct.pack_into("<I", header, 20, b_bits)
    struct.pack_into("<I", header, 24, a_bits)
    
    # Texture Properties (leer)
    tex_props = bytearray(TEX_PROPS_SIZE)
    
    with open(rsb_path, "wb") as f:
        f.write(bytes(header))
        f.write(pixel_data)
        f.write(bytes(tex_props))
    
    print(f"✓ Gespeichert: {rsb_path}")
    print(f"  Bild {crop_w}×{crop_h} in Textur {tex_w}×{tex_h} (Offset {x_off},{y_off})")
    print(f"  Gesamt: {HEADER_SIZE + len(pixel_data) + TEX_PROPS_SIZE:,} Bytes")

def main():
    if len(sys.argv) < 3:
        print("Verwendung:")
        print("  python rsb_converter.py to_png  input.rsb  output_dir/")
        print("  python rsb_converter.py to_rsb  input.png  output.rsb")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "to_png" and len(sys.argv) == 4:
        rsb_to_png(sys.argv[2], sys.argv[3])
    elif mode == "to_rsb" and len(sys.argv) == 4:
        png_to_rsb(sys.argv[2], sys.argv[3])
    else:
        print("Verwendung:")
        print("  python rsb_converter.py to_png  input.rsb  output_dir/")
        print("  python rsb_converter.py to_rsb  input.png  output.rsb")
        sys.exit(1)

if __name__ == "__main__":
    main()