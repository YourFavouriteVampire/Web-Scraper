import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from urllib.parse import urlparse
import re
import tkinter.font as tkfont
import os
import urllib
import threading
from tkinter.ttk import Progressbar

def web_scraper():
    url = url_entry.get()
    query = query_entry.get()

    # Send an HTTP GET request to the URL
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    html_content = response.content

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract the text content from the parsed HTML
    text_content = soup.get_text()

    if scrape_whole.get():
        # Save the whole text content to a text file
        default_filename = urlparse(url).netloc + ".txt"
        filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_filename)
        if filename:
            with open(filename, "w") as file:
                file.write(text_content)
            messagebox.showinfo("Success", f"Whole text content saved to {filename}")
    elif scrape_numerical.get():
        # Scrape numerical data from the text content
        numerical_data = re.findall(r'\b\d+\b', text_content)
        if len(numerical_data) > 0:
            default_filename = urlparse(url).netloc + "_numerical.txt"
            filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_filename)
            if filename:
                with open(filename, "w") as file:
                    for data in numerical_data:
                        file.write(data + "\n")
                messagebox.showinfo("Success", f"Numerical data saved to {filename}")
        else:
            messagebox.showinfo("No Numerical Data", "No numerical data found.")
    elif scrape_special_chars.get():
        # Scrape alphanumeric data with special characters from the text content
        alphanumeric_data = re.findall(r'\b\w+\W+\b', text_content)
        if len(alphanumeric_data) > 0:
            default_filename = urlparse(url).netloc + "_alphanumeric.txt"
            filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_filename)
            if filename:
                with open(filename, "w") as file:
                    for data in alphanumeric_data:
                        file.write(data + "\n")
                messagebox.showinfo("Success", f"Alphanumeric data with special characters saved to {filename}")
        else:
            messagebox.showinfo("No Alphanumeric Data", "No alphanumeric data with special characters found.")
    elif scrape_images.get():
        # Scrape and save images from the website
        image_tags = soup.find_all('img')
        if len(image_tags) > 0:
            default_foldername = urlparse(url).netloc + "_images"
            foldername = filedialog.askdirectory(initialdir=".", title="Select Folder")
            if foldername:
                total_images = len(image_tags)
                progress_label.config(text=f"Scraping images: 0/{total_images}")
                progressbar["maximum"] = total_images

                def save_image(image_url, image_filename):
                    image_response = requests.get(image_url, stream=True)
                    if image_response.status_code == 200:
                        image_path = os.path.join(foldername, image_filename)
                        with open(image_path, 'wb') as image_file:
                            for chunk in image_response.iter_content(1024):
                                image_file.write(chunk)
                        progressbar.step()
                        progress_label.config(text=f"Scraping images: {progressbar['value']}/{total_images}")
                        window.update()

                for i, tag in enumerate(image_tags):
                    image_url = urllib.parse.urljoin(url, tag['src'])
                    image_filename = f"image{i+1}.{tag['src'].split('.')[-1]}"
                    t = threading.Thread(target=save_image, args=(image_url, image_filename))
                    t.start()

                def check_threads():
                    if threading.active_count() == 1:
                        messagebox.showinfo("Success", f"Images saved to {foldername}")
                        progress_label.config(text="")
                        progressbar["value"] = 0
                    else:
                        window.after(100, check_threads)

                window.after(100, check_threads)
            else:
                progress_label.config(text="")
        else:
            messagebox.showinfo("No Images", "No images found on the website.")
    elif scrape_videos.get():
        # Scrape and save videos from the website
        video_tags = soup.find_all('video')
        if len(video_tags) > 0:
            default_foldername = urlparse(url).netloc + "_videos"
            foldername = filedialog.askdirectory(initialdir=".", title="Select Folder")
            if foldername:
                total_videos = len(video_tags)
                progress_label.config(text=f"Scraping videos: 0/{total_videos}")
                progressbar["maximum"] = total_videos

                def save_video(video_url, video_filename):
                    video_response = requests.get(video_url, stream=True)
                    if video_response.status_code == 200:
                        video_path = os.path.join(foldername, video_filename)
                        with open(video_path, 'wb') as video_file:
                            for chunk in video_response.iter_content(1024):
                                video_file.write(chunk)
                        progressbar.step()
                        progress_label.config(text=f"Scraping videos: {progressbar['value']}/{total_videos}")
                        window.update()

                for i, tag in enumerate(video_tags):
                    video_url = urllib.parse.urljoin(url, tag['src'])
                    video_filename = f"video{i+1}.{tag['src'].split('.')[-1]}"
                    t = threading.Thread(target=save_video, args=(video_url, video_filename))
                    t.start()

                def check_threads():
                    if threading.active_count() == 1:
                        messagebox.showinfo("Success", f"Videos saved to {foldername}")
                        progress_label.config(text="")
                        progressbar["value"] = 0
                    else:
                        window.after(100, check_threads)

                window.after(100, check_threads)
            else:
                progress_label.config(text="")
        else:
            messagebox.showinfo("No Videos", "No videos found on the website.")
    else:
        # Find and extract the paragraphs or documents containing the query
        results = []
        for paragraph in text_content.split("\n"):
            if query.lower() in paragraph.lower():
                results.append(paragraph)

        # Save the results to a text file
        if len(results) > 0:
            default_filename = urlparse(url).netloc + "_results.txt"
            filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_filename)
            if filename:
                with open(filename, "w") as file:
                    for result in results:
                        file.write(result + "\n")
                messagebox.showinfo("Success", f"Matching results saved to {filename}")
        else:
            messagebox.showinfo("No Results", "No matching results found.")

# Create the GUI window
window = Tk()
window.title("Web Scraper")
window.geometry("800x600")

# Define the font style
font_style = tkfont.Font(size=11)

# URL input
url_label = Label(window, text="Enter URL:", font=font_style)
url_label.pack()
url_entry = Entry(window, width=50, font=font_style)
url_entry.pack()

# Query input
query_label = Label(window, text="Enter Text:", font=font_style)
query_label.pack()
query_entry = Entry(window, width=50, font=font_style)
query_entry.pack()

# Scrape whole site option
scrape_whole = BooleanVar()
scrape_whole_checkbox = Checkbutton(window, text="Scrape Whole Site", variable=scrape_whole, font=font_style)
scrape_whole_checkbox.pack()

# Scrape numerical data option
scrape_numerical = BooleanVar()
scrape_numerical_checkbox = Checkbutton(window, text="Scrape Numerical Data", variable=scrape_numerical, font=font_style)
scrape_numerical_checkbox.pack()

# Scrape alphanumeric data with special characters option
scrape_special_chars = BooleanVar()
scrape_special_chars_checkbox = Checkbutton(window, text="Scrape Alphanumeric Data with Special Characters", variable=scrape_special_chars, font=font_style)
scrape_special_chars_checkbox.pack()

# Scrape images option
scrape_images = BooleanVar()
scrape_images_checkbox = Checkbutton(window, text="Scrape Images", variable=scrape_images, font=font_style)
scrape_images_checkbox.pack()

# Scrape videos option
scrape_videos = BooleanVar()
scrape_videos_checkbox = Checkbutton(window, text="Scrape Videos", variable=scrape_videos, font=font_style)
scrape_videos_checkbox.pack()

# Scrape button
scrape_button = Button(window, text="Scrape", command=web_scraper, font=font_style)
scrape_button.pack()

# Progressbar
progressbar = Progressbar(window, length=200)
progressbar.pack()

# Progress label
progress_label = Label(window, text="", font=font_style)
progress_label.pack()

# Run the GUI event loop
window.mainloop()
