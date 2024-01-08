import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

headers = {"UserAgent": UserAgent().random}
URL = "https://www.mywaifulist.moe/random"


def save_image(image_url: str, image_title: str) -> None:
    """
    Saves the image of an anime character
    """
    image = requests.get(image_url, headers=headers)
    with open(image_title, "wb") as file:
        file.write(image.content)


def random_anime_character() -> tuple[str, str, str]:
    """
    Returns the Title, Description, and Image Title of a random anime character.
    """
    options = Options()
    options.add_argument(f"user-agent={headers['UserAgent']}")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(URL)
        page_text = driver.page_source

        soup = BeautifulSoup(page_text, "html.parser")

        title_element = soup.find("meta", attrs={"name": "og:title"})
        image_element = soup.find("meta", attrs={"name": "og:image"})
        description_element = soup.find("p", id="description")

        if not title_element or not image_element or not description_element:
            raise ValueError("Не удалось найти необходимые элементы на странице.")

        title = title_element.attrs["content"]
        image_url = image_element.attrs["content"]
        description = description_element.get_text()

        _, image_extension = os.path.splitext(os.path.basename(image_url))
        image_title = title.strip().replace(" ", "_")
        image_title = f"{image_title}{image_extension}"

        save_image(image_url, image_title)
        return (title, description, image_title)

    finally:
        driver.quit()


if __name__ == "__main__":

    try:
        title, desc, image_title = random_anime_character()
        print(f"{title}\n\n{desc}\n\nImage saved: {image_title}")

        with open(f"{title}_desc.txt", "w", encoding="utf-8") as file:
            file.write(desc)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
