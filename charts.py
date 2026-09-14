"""Generate simple PNG charts from the structured chart_data returned by the LLM."""
import os
import uuid
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def build_charts(chart_data, output_dir="charts"):
    os.makedirs(output_dir, exist_ok=True)
    images = []
    for chart in chart_data:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        if chart.get("type") == "line":
            ax.plot(chart["labels"], chart["values"], marker="o")
        else:
            ax.bar(chart["labels"], chart["values"])
        ax.set_title(chart["title"], fontsize=11)
        ax.set_xlabel(f"Source : {chart.get('source', '')}", fontsize=8)
        fig.tight_layout()

        filename = f"{uuid.uuid4().hex}.png"
        path = os.path.join(output_dir, filename)
        fig.savefig(path, dpi=120)
        plt.close(fig)

        images.append({"path": path, "cid": filename, "title": chart["title"]})
    return images
