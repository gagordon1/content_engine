import wikipedia

class Wikipedia:
    """
    A class representing a Wikipedia source. It takes a Wikipedia article URL
    and provides a method to return its main textual content.
    """

    def __init__(self, url: str):
        """
        Initialize the Wikipedia source with a direct Wikipedia link.
        
        :param url: A valid Wikipedia article URL, for example:
                    'https://en.wikipedia.org/wiki/Artificial_intelligence'
        """
        self.url = url

    def get_text(self) -> str:
        """
        Retrieve the primary text from the Wikipedia page.
        (Skeleton only—no actual implementation here.)

        :return: A string containing the article's main content.
        """
        # Implementation placeholder
        article_name = self.clean_url(self.url)
        page = wikipedia.page(article_name)
        return page.content
    
    def clean_url(self, url: str) -> str:
        """
        Given a Wikipedia URL like 'https://en.wikipedia.org/wiki/Siege_of_Yorktown',
        return only the article part: 'Siege_of_Yorktown'.

        :param url: A full Wikipedia article URL.
        :return: The article name (e.g., 'Siege_of_Yorktown'), or
                 an empty string if '/wiki/' is not found.
        """
        marker = "/wiki/"
        idx = url.find(marker)
        if idx == -1:
            return ""  # '/wiki/' not found
        # The article name starts right after '/wiki/'
        return url[idx + len(marker):]
  

if __name__ == "__main__":
    # wik= Wikipedia("https://en.wikipedia.org/wiki/Siege_of_Yorktown")
    # text = wik.get_text()
    pass