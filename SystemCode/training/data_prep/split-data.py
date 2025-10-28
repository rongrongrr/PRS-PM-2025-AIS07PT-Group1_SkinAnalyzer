import os
import random
import shutil

def split_dataset(image_dir, label_dir, output_dir, train_split=0.8):
    # paths for training & eval
    train_images_path = os.path.join(output_dir, 'images', 'train')
    val_images_path = os.path.join(output_dir, 'images', 'val')
    train_labels_path = os.path.join(output_dir, 'labels', 'train')
    val_labels_path = os.path.join(output_dir, 'labels', 'val')

    # Create the directories if they don't exist
    print("Creating destination directories...")
    os.makedirs(train_images_path, exist_ok=True)
    os.makedirs(val_images_path, exist_ok=True)
    os.makedirs(train_labels_path, exist_ok=True)
    os.makedirs(val_labels_path, exist_ok=True)
    print("Directories created successfully.")

    image_extensions = {'.png', '.jpg', '.jpeg'}
    all_images = [f for f in os.listdir(image_dir) if os.path.splitext(f)[1].lower() in image_extensions]
    
    # shuffling here randomly to ensure unbiased splits
    random.shuffle(all_images)
    
    total_images = len(all_images)
    if total_images == 0:
        print("Error: No images found in the source directory.")
        return
        
    print(f"Found {total_images} total images.")

    # calc index val
    split_index = int(total_images * train_split)
    train_files = all_images[:split_index]
    val_files = all_images[split_index:]

    print(f"Splitting into {len(train_files)} training files and {len(val_files)} validation files.")

    #copiying files to destination folders
    def copy_files(file_list, image_dest, label_dest):
        """Helper function to copy image and its corresponding label."""
        copied_count = 0
        for filename in file_list:
            base_filename = os.path.splitext(filename)[0]
            
            image_src_path = os.path.join(image_dir, filename)
            label_src_path = os.path.join(label_dir, base_filename + '.txt')
            image_dest_path = os.path.join(image_dest, filename)
            label_dest_path = os.path.join(label_dest, base_filename + '.txt')

            if os.path.exists(label_src_path):
                shutil.copy(image_src_path, image_dest_path)
                shutil.copy(label_src_path, label_dest_path)
                copied_count += 1
            else:
                print(f"Warning: Label not found for image {filename}. Skipping this file.")
        return copied_count

    print("\nCopying training files...")
    train_copied = copy_files(train_files, train_images_path, train_labels_path)
    print(f"Copied {train_copied} training images and their labels.")

    print("\nCopying validation files...")
    val_copied = copy_files(val_files, val_images_path, val_labels_path)
    print(f"Copied {val_copied} validation images and their labels.")
    
    print("\n--- Dataset splitting complete! ---")
    print(f"New dataset created at: {os.path.abspath(output_dir)}")


if __name__ == '__main__':
    SOURCE_IMAGE_DIR = 'data/images'  # The folder with all your source images
    SOURCE_LABEL_DIR = 'data/labels'  # The folder with all your source .txt labels
    OUTPUT_DATASET_DIR = 'data/yolo_training_split' # The root folder for your new split dataset
    
    # Set the desired split ratio (e.g., 0.8 means 80% train, 20% validation)
    TRAIN_VALIDATION_SPLIT = 0.8 
    
    split_dataset(SOURCE_IMAGE_DIR, SOURCE_LABEL_DIR, OUTPUT_DATASET_DIR, TRAIN_VALIDATION_SPLIT)

