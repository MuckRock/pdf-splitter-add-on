"""
This Add-On uses pdftk: https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/ to 
split a DocumentCloud document into two documents and uploads the two resulting documents. 
"""

from documentcloud.addon import AddOn
import os
import subprocess

class Split(AddOn):
    """Creates a temp directory, downloads doc, splits along page, uploads split documents"""

    def main(self):
        page = self.data.get("page")
        page2 = page + 1
        os.makedirs(os.path.dirname("./out/"), exist_ok=True)
        for document in self.get_documents():
            title = document.title
            with open(f'{title}.pdf', 'wb') as f:
                f.write(document.pdf)
            cmd1 = f'pdftk "{title}.pdf" cat 1-{page} output "./out/{title}_1_{page}.pdf"'
            cmd2 = f'pdftk "{title}.pdf" cat {page2}-end output "./out/{title}_{page2}-end.pdf"'
            subprocess.call(cmd1, shell=True)
            subprocess.call(cmd2, shell=True)
        self.client.documents.upload_directory("./out/")
            

if __name__ == "__main__":
    Split().main()
