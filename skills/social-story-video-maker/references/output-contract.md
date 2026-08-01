# Output Contract

Use this reference when checking whether a picture narration story video package is complete.

```text
asset/<Story Name>/
  original script/original.txt
  edited script/edited.txt
  edited script/name_map.json
  edited script/rewrite_prompt.md
  audio/
    narration-001.wav
    narration-002.wav
    narration-manifest.json
  scene-beats.json
  character-bible.json
  image-prompts.md
  images/
    scene-001-a.png
  comfyui-workflows/
    scene-001-workflow.json
  video/
    hyperframes/
    timeline/
    captions/
    sfx/
    music/
    renders/
  output/
    final.mp4
    final_with_captions.mp4
    thumbnail.png
    production_manifest.json
```

Do not collapse the editable source package into only `final.mp4`.
