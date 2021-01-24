from typing import List
from block import Block
import numpy as np
import cv2
from hashlib import md5


class LayoutViewer:
    def __init__(self, images: List[np.ndarray], pages: List[List[Block]], filename: str):
        self.images = images
        self.pages = pages
        self.filename = filename

    def __get_images_html(self, pdf_hash):
        n = len(self.images)
        return "\n".join(['<div class="viewer-image" id="img-{0}"><img src="/images/{2}_page_{0}.png?v={1}"></div>'.format(i, pdf_hash, self.filename) for i in range(n)])

    def __get_blocks_html(self) -> str:
        blocks = []

        for page_id, page in enumerate(self.pages):
            for block_id, block in enumerate(page):
                blocks.append(block.convert_to_html(page_id, block_id))

        return "\n".join(blocks)

    def __get_blocks_js(self) -> str:
        return "\n".join(['[' + "\n".join([block.convert_to_js() for block in page]) + '],' for page in self.pages])

    def get_md5(self, path: str) -> str:
        with open(path, 'rb') as f:
            return md5(f.read()).hexdigest()

    def save_images(self):
        for i, image in enumerate(self.images):
            img = np.array(image)
            cv2.imwrite('images/{0}_page_{1}.png'.format(self.filename, i), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    def get_html(self, pdf_hash):
        images_html = self.__get_images_html(pdf_hash)
        blocks_html = self.__get_blocks_html()
        blocks_js = self.__get_blocks_js()

        hash_style = self.get_md5('styles/styles.css')
        hash_js = self.get_md5('js/viewer.js')

        return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Layout viewer</title>
                <link rel="stylesheet" type="text/css" href="/styles/styles.css?v={hash}">
            </head>
            <body>
                <div class="viewer">
                    <div class="viewer-images">{images}</div>
                    <div class="viewer-layout"><div class="viewer-content">{pages}</div></div>
                </div>

                <script src="/js/viewer.js?v={hash_js}"></script>
                <script>
                    let blocks = [{blocks}]
                    let layoutViewer = new LayoutViewer(blocks)
                </script>
            </body>
            </html>
        '''.format(images=images_html, pages=blocks_html, blocks=blocks_js, hash=hash_style, hash_js=hash_js)