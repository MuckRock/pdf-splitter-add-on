"""
This Add-On uses pdftk: https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/ to 
split a DocumentCloud document into two documents and uploads the two resulting documents. 
"""
import os
import subprocess
from documentcloud.addon import AddOn


class Split(AddOn):
    """Creates a temp directory, downloads doc, splits along page, uploads split documents"""

    def main(self):
        """Runs the document through pdfkit and splits across that page,
        then uploads two output documents"""
        # Pulls the page to split on from front end
        page = self.data["page"]
        page2 = page + 1
        # Creates temporary directory where the split documents will live
        os.makedirs(os.path.dirname("./out/"), exist_ok=True)
        if not self.documents:
            self.set_message("Please select at least one document.")
            return
        for document in self.get_documents():
            title = document.title
            with open(f"{title}.pdf", "wb") as file:
                file.write(document.pdf)
            # Split the document into two documents along the designated page using pdftk
            cmd1 = (
                f'pdftk "{title}.pdf" cat 1-{page} output "./out/{title}_1-{page}.pdf"'
            )
            cmd2 = f'pdftk "{title}.pdf" cat {page2}-end output "./out/{title}_{page2}-end.pdf"'
            subprocess.call(cmd1, shell=True)
            subprocess.call(cmd2, shell=True)
        # Uploads the split documents to DocumentCloud
        self.client.documents.upload_directory("./out/")


if __name__ == "__main__":
    Split().main()
