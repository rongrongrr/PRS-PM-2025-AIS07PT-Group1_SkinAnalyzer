import kagglehub

# Download latest version
path = kagglehub.dataset_download("volodymyrpivoshenko/skin-cancer-lesions-segmentation")

print("Path to dataset files:", path)