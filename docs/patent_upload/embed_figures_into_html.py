"""Create a single-file HTML with figures embedded as base64 so PDF can be made from anywhere."""
import base64
from pathlib import Path


def main():
    base = Path(__file__).resolve().parent
    parent = base.parent
    html_path = base / "Provisional_Patent_Specification_FULL_Dhiraj_Pokhrel.html"
    figures_dir = parent / "patent_figures"
    out_path = base / "Provisional_Patent_Specification_WITH_FIGURES_Dhiraj_Pokhrel.html"

    figures = [
        ("../patent_figures/Figure_1_System_Architecture.png", "Figure 1 - System Architecture"),
        ("../patent_figures/Figure_2_Quality_Metrics.png", "Figure 2 - Quality Metrics"),
        ("../patent_figures/Figure_3_Template_System.png", "Figure 3 - Template System"),
        ("../patent_figures/Figure_4_Provider_Abstraction.png", "Figure 4 - Provider Abstraction"),
        ("../patent_figures/Figure_5_Session_Management.png", "Figure 5 - Session Management"),
    ]

    html = html_path.read_text(encoding="utf-8")
    for rel_path, alt in figures:
        img_path = (base / rel_path).resolve() if rel_path.startswith("..") else base / rel_path
        if not img_path.exists():
            img_path = figures_dir / Path(rel_path).name
        if not img_path.exists():
            print(f"Skip (not found): {rel_path}")
            continue
        b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")
        data_uri = f"data:image/png;base64,{b64}"
        old_src = f'src="{rel_path}"'
        new_src = f'src="{data_uri}"'
        html = html.replace(old_src, new_src)
        print(f"Embedded: {img_path.name}")

    out_path.write_text(html, encoding="utf-8")
    print(f"Written: {out_path} (single file with embedded figures)")

if __name__ == "__main__":
    main()
