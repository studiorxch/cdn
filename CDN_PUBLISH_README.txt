# CDN Publish Quickstart

1) After running image batches, you should have files like:
   station-gen/out_img/168th-street/168th-street.png

2) Publish them into your CDN repo (flat /station/ folder) and build a manifest:
```bash
# from station-gen/
pip install pillow
python publish_to_cdn.py       --src out_img       --dst ../cdn/station       --url_base https://studiorxch.github.io/cdn/station/       --format webp --quality 92
```

3) Commit & push the CDN repo:
```bash
cd ../cdn
git add station/*.webp cdn_manifest.json
git commit -m "feat(cdn): add new station renders and manifest"
git push origin main
```

4) Your files will be live at:
   https://studiorxch.github.io/cdn/station/<slug>.webp
   Manifest at: https://studiorxch.github.io/cdn/cdn_manifest.json
