import os
import requests
from tqdm import tqdm

# Function to download an image into a specific folder
def download_image(url, folder_path):
    try:
        # Ensure the target folder exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Download the image
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_name = os.path.join(folder_path, os.path.basename(url))
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded {url} to {folder_path}")
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

# Function to create folder structure based on the original path or category of the image
def create_category_folder(base_folder, subfolder):
    category_folder = os.path.join(base_folder, subfolder)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)
    return category_folder

# Function to download images from the WordPress REST API
def download_images_from_api(api_url, base_folder):
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    page = 1
    while True:
        response = requests.get(api_url, params={'page': page, 'per_page': 100})
        if response.status_code != 200:
            print(f"Failed to retrieve images from {api_url}")
            break

        images = response.json()
        if not images:
            break

        for image in tqdm(images, desc=f"Downloading images from page {page}"):
            img_url = image.get('source_url')
            # Extract the category from the image metadata (e.g., date, folder structure)
            if img_url and img_url.lower().endswith('.jpg'):
                # Determine the category or structure based on image URL or metadata
                # Assuming URL structure like /wp-content/uploads/YYYY/MM/filename.jpg
                relative_path = img_url.split("uploads/")[-1]
                category_folder = create_category_folder(base_folder, os.path.dirname(relative_path))
                
                # Download the image to the specified category folder
                download_image(img_url, category_folder)
        
        page += 1

# Main script
def main():
    base_url = 'https://www.kagati.nl/wp-json/wp/v2/media'  # Replace with your WordPress site URL
    download_folder = "downloaded_images"

    download_images_from_api(base_url, download_folder)

    print("All images have been downloaded and organized into category folders.")

if __name__ == "__main__":
    main()
