from requests_html import HTMLSession
from urllib.request import urlretrieve
from pathlib import Path
from urllib.parse import unquote


root = Path(__file__).parents[1]

session = HTMLSession()

r = session.get("http://doi.org/10.5281/zenodo.831455")

downloads = r.html.find("#files", first=True).links

home = "https://zenodo.org"

for download in sorted(downloads):
    filename = unquote(download.split("/")[-1])
    print("Downloading {}".format(filename))
    path = root / "archive" / filename
    urlretrieve(home + download, filename=path)
