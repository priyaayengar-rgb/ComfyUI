#!/usr/bin/env python3
"""Generate a dog image using ComfyUI API."""

import json
import urllib.request
import urllib.parse
import time
import sys
import os

COMFYUI_URL = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")


def queue_prompt(workflow: dict) -> str:
    payload = json.dumps({"prompt": workflow}).encode("utf-8")
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    return result["prompt_id"]


def get_history(prompt_id: str) -> dict:
    url = f"{COMFYUI_URL}/history/{urllib.parse.quote(prompt_id)}"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read())


def wait_for_completion(prompt_id: str, poll_interval: float = 1.0) -> dict:
    print(f"Waiting for prompt {prompt_id} to complete...", flush=True)
    while True:
        history = get_history(prompt_id)
        if prompt_id in history:
            return history[prompt_id]
        time.sleep(poll_interval)


def download_image(filename: str, subfolder: str, folder_type: str) -> bytes:
    params = urllib.parse.urlencode(
        {"filename": filename, "subfolder": subfolder, "type": folder_type}
    )
    url = f"{COMFYUI_URL}/view?{params}"
    with urllib.request.urlopen(url) as resp:
        return resp.read()


def main():
    workflow_path = os.path.join(os.path.dirname(__file__), "workflows", "generate_dog.json")
    with open(workflow_path) as f:
        workflow = json.load(f)

    print("Submitting dog image generation workflow to ComfyUI...")
    prompt_id = queue_prompt(workflow)
    result = wait_for_completion(prompt_id)

    outputs = result.get("outputs", {})
    saved = []
    for node_id, node_output in outputs.items():
        for image in node_output.get("images", []):
            filename = image["filename"]
            subfolder = image.get("subfolder", "")
            folder_type = image.get("type", "output")
            print(f"Downloading {filename}...")
            data = download_image(filename, subfolder, folder_type)
            out_path = os.path.join(os.path.dirname(__file__), filename)
            with open(out_path, "wb") as f:
                f.write(data)
            saved.append(out_path)
            print(f"Saved: {out_path}")

    if not saved:
        print("No images were generated.", file=sys.stderr)
        sys.exit(1)

    print(f"\nDone! Generated {len(saved)} image(s).")


if __name__ == "__main__":
    main()
