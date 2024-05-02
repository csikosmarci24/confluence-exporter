from atlassian import Confluence
from data import *


confluence = Confluence(url=url, username=user, password=token, api_version="cloud")

# https://github.com/gergelykalman/confluence-markdown-exporter
def sanitize_filename(page_title):
        for invalid in ["..", "/"]:
            if invalid in page_title:
                print("Dangerous page title: \"{}\", \"{}\" found, replacing it with \"_\"".format(
                    page_title,
                    invalid))
                page_title = page_title.replace(invalid, "_")
        return page_title

def export_page(page_id):
    page_title = sanitize_filename(confluence.get_page_by_id(page_id)["title"])
    with open(f"./out/{page_title}.pdf", "wb") as file:
        file.write(confluence.get_page_as_pdf(page_id))
    
    child_ids = confluence.get_child_id_list(page_id)
    for child_id in child_ids:
        export_page(child_id)

space = confluence.get_space(space_name)
homepage_id = space["homepage"]["id"]
export_page(homepage_id)
