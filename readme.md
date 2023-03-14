# GitHub Contributions Painter

Paints a bit image on the `(inf)*7` grid for GitHub Contributions

## Details

Uses the GitHub actions workflow in [draw.yml](.github/workflows/draw.yml) to commit to repo

1) Runs `main.py` to get the commit count for the current day   
This is determined by offset into `image.txt`  
     
2) Commits a bump the required times to `bump` file and pushes to same repo  
   Uses the [GITHUB_TOKEN](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret) from the actions workflow to push the changes

## Painter GUI 

Users can use the helper **painter.py** GUI to draw bit images for printing

```
python painter.py
```

This GUI supports the following functionality:

> **Draw:**  Color squares by clicking. 5 color levels supported  
**Load:**  Load the most recent image from `INPUT_IMAGE_PATH`  
**Clear:** Clear the grid    
**Save:**  Save the image to `INPUT_IMAGE_PATH`  


![GUI Example](readme_images/img_1.png)

## Environment Variables

| Key | Value | Desc |
| --- | ---| ---|
| INPUT_IMAGE_PATH | `image.txt` | The path to save/load/generate the bit image from |