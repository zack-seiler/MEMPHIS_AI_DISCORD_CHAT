from googlesearch import search
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from transformers import GPT2Tokenizer
import logging


def google_search(query):
    url_list = []
    for url in search(str(query), stop=3):
        print("Google search: " + str(url))
        url_list.append(url)

    return url_list


def remove_urls_with_domain(urls, domain):
    """
    Accepts a list containing URLs and removes all elements of the list containing a URL with a specified domain name.

    Args:
    urls (list): a list containing URLs
    domain (str): the domain name to remove

    Returns:
    list: a new list with all elements that contain the specified domain name removed
    """

    # Create an empty list to store the filtered URLs
    filtered_urls = []

    # Loop through each URL in the list
    for url in urls:

        # Parse the URL to get the domain name
        parsed_url = urlparse(url)
        url_domain = parsed_url.netloc

        # If the domain name in the URL does not match the specified domain name, add it to the filtered URLs list
        if domain not in url_domain:
            filtered_urls.append(url)

    # Return the filtered URLs list
    return filtered_urls


def scrape_website(url):
    """
    Uses the BeautifulSoup library to visit a website and scrape all info contained within paragraph or heading tags.

    Args:
    url (str): the URL of the website to scrape

    Returns:
    str: a string containing all the text within paragraph or heading tags on the website
    """

    # Send a GET request to the URL to get the HTML content
    response = requests.get(url)
    html = response.content

    # Create a BeautifulSoup object from the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Find all paragraph and heading tags and extract the text from them
    paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    text = ''
    for p in paragraphs:
        text += p.get_text() + ' '
    print("Scraped data: " + text)
    return text


def truncate_string_to_token_limit(input_string, max_tokens=3000):
    # Suppress tokenization warnings from the transformers library
    logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)

    # Initialize the GPT-2 tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    # Tokenize the input string
    tokens = tokenizer.encode(input_string)

    # If the number of tokens in the input string is less than or equal to the max_tokens limit, return the
    # input_string as is
    if len(tokens) <= max_tokens:
        return input_string

    # If the number of tokens in the input string exceeds the max_tokens limit, keep only the first max_tokens tokens
    truncated_tokens = tokens[:max_tokens]

    # Convert the truncated tokens back into a string
    truncated_string = tokenizer.decode(truncated_tokens)

    # Return the truncated string
    return truncated_string


def cut_string_to_word_limit(text, limit):
    """
    Accepts a string and cuts it down to a specified number of words.

    Args:
    text (str): the string to cut down
    limit (int): the maximum number of words to include in the final string

    Returns:
    str: the original string with only the first 'limit' words
    """

    # Split the string into a list of words
    words = text.split()

    # If the number of words is less than or equal to the limit, return the original string
    if len(words) <= limit:
        return text

    # Otherwise, join the first 'limit' words with spaces and return the resulting string
    final_string = ' '.join(words[:limit])
    return final_string


def count_words(text):
    """
    Counts the number of words in a string.

    Args:
    text (str): the string to count words in

    Returns:
    int: the number of words in the string
    """

    # Split the string into a list of words using the split() method
    words = text.split()

    # Return the length of the list of words
    print("Number of words: ", len(words))
    return len(words)


def remove_newlines_and_tabs(text):
    """
    Removes all newlines and tabs from a string.

    Args:
    text (str): the string to remove newlines and tabs from

    Returns:
    str: the input string with all newlines and tabs removed
    """

    # Replace all newlines and tabs with spaces using the replace() method
    cleaned_text = text.replace('\n', ' ').replace('\t', ' ')

    return cleaned_text


def handle_search(query):
    url_blacklist = [
        "youtube.com"
    ]
    scraped_data_pile = ""
    refined_data_pile = ""
    google_search_url_list = google_search(query)

    for item in url_blacklist:
        google_search_url_list = remove_urls_with_domain(google_search_url_list, item)

    for item in google_search_url_list:
        print("Refined list: " + str(item))
        scraped_data_pile += scrape_website(item)
        refined_data_pile = truncate_string_to_token_limit(scraped_data_pile)
        # if count_words(scraped_data_pile) > 1000:
        #     scraped_data_pile = cut_string_to_word_limit(scraped_data_pile, 1000)
        #     break

    refined_data_pile = remove_newlines_and_tabs(refined_data_pile)
    print("Words in refined data pile: ", count_words(refined_data_pile))
    print(refined_data_pile)
    return refined_data_pile
