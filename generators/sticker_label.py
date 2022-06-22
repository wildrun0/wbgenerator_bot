import os
import textwrap
import logging
from io import BytesIO
from utilities import Utils as utils
from config import DEFAULT_FONT

from PIL import Image
from PIL import ImageFont, ImageDraw

from docx import Document
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

class StickerLabelGenerator():
    def __init__(self):
        self.label_width, self.label_height = (342, 1080)
        self.barcode_width = self.label_width
        self.font_size = 16
        self.STICKERS = {}
        self.STICKERS_ALONE = {}

    def clear(self, uid: str|int) -> None:
        for i in os.listdir(f"userdata/{uid}/"):
            logging.info(f"CLEANING USER'S (id: {uid}) TEMP FILES")
            if i.startswith("temp_") or i.startswith("stickers_"):
                os.remove(f"userdata/{uid}/{i}")

    def label_create(self, uid: str|int, product_params:dict, barcode_img:BytesIO) -> str:
        SAVE_DIR = f"userdata/{uid}/"
        FILENAME = f"label_{product_params['Артикул']}.png"

        barcode_png = Image.open(barcode_img)

        w, h = barcode_png.size

        barcode_height = int(self.barcode_width * h / w)
        barcode_png = barcode_png.resize((
            self.barcode_width, barcode_height
        ), Image.ANTIALIAS)

        img = Image.new(
            'RGB',
            (self.label_width, self.label_height),
            (255, 255, 255)  # White
        )

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(DEFAULT_FONT, size=self.font_size)

        i = barcode_height
        for k, v in product_params.items():
            if k not in ['Штрихкод']:
                textwrapped = textwrap.wrap(f"{k}: {v}", width=31)
                offset = (35, i)
                text = '\n'.join(textwrapped)
                draw.text((offset), text, font=font, fill="black")
                newlines = text.count("\n")+1
                i = i+(20*(newlines if newlines > 0 else 1))

        img = img.crop((0,0, self.label_width, i+5))
        img.paste(
            barcode_png, (
                (self.label_width - self.barcode_width) // 2,
                0
            )
        )
        img.save(os.path.join(SAVE_DIR, FILENAME), quality=100)
        logging.info(f"USER'S (id: {uid}) NEW LABEL CREATED")
        return (SAVE_DIR+FILENAME)

    def sticker_add(self, uid: str|int, user_code_png: str, should_double:bool = False) -> None:
        SAVE_DIR = f"userdata/{uid}/"
        user_CodePng = Image.open(SAVE_DIR+user_code_png)

        try:
            self.STICKERS[uid].append([user_CodePng])
        except KeyError:
            self.STICKERS[uid] = [[user_CodePng]]

        if should_double:
            try:
                self.STICKERS_ALONE[uid] += 1
            except KeyError:
                self.STICKERS_ALONE[uid] = 1

    def complete_file(self, uid: str|int, articul:str) -> str:
        logging.info(f"USER (id: {uid}) GENERATING STICKERS")
        document = Document()
        sections = document.sections
        for section in sections:
            section.top_margin = Cm(1)
            section.bottom_margin = Cm(1)
            section.left_margin = Cm(1)
            section.right_margin = Cm(1)

        rows = len(self.STICKERS[uid])
        descriptions = False
        
        if uid in self.STICKERS_ALONE:
            rows += self.STICKERS_ALONE[uid]
            descriptions = self.STICKERS_ALONE[uid] // 2
    
        if rows == 1:   # а хули оно ломается
            rows = 2
        table = document.add_table(rows=rows, cols=3)
    
        SAVE_DIR = f"userdata/{uid}/"
        barcode_png = Image.open(f"{SAVE_DIR}label_{articul}.png")

        # ниже пиздец который отнял пол жизни
        # за такой код убивают.............................
        # создано в содружестве с @moksempython
        bills = self.STICKERS[uid] 
        row, column = 0, 0
        while len(bills) > 0:
            for enum1, elem in enumerate(bills):
                if column == 3:# (ну типа по три колонки или хз):
                    column = 0
                    row += 2
                for image in elem:
                    # barcode -- описание
                    row_cells = table.rows[row].cells
                    barcode_cell = row_cells[column].paragraphs[0]
                    barcode_pr = barcode_cell.add_run()
                    # usercode -- штрихкод отправки
                    row_cells = table.rows[row+1].cells
                    usercode_cell = row_cells[column].paragraphs[0]
                    usercode_pr = usercode_cell.add_run()
                    if image.size[0] == 236:
                        usercode_pr.add_picture(utils.image2file_bytes(image), width=Cm(4), height=Cm(3))
                        barcode_pr.add_picture(utils.image2file_bytes(barcode_png), width=Cm(4.82))
                        barcode_cell.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    elif image.size[0] == 342:
                        usercode_pr.add_picture(utils.image2file_bytes(image), width=Cm(5.8), height=Cm(4))
                        barcode_pr.add_picture(utils.image2file_bytes(barcode_png), width=Cm(5.82))
                        barcode_cell.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    else:
                        raise Exception("Неподдерживаемый формат штрихкода!")
                    usercode_cell.alignment = WD_ALIGN_PARAGRAPH.CENTER
                del bills[enum1]
                column += 1
        del self.STICKERS[uid]
        # А ТУТ добавляем маркировки товаров (описание) без клиентских штрихов если попросили...
        if descriptions:
            while descriptions > 0:
                if column == 3:# (ну типа по три колонки или хз):
                    column = 0
                    row += 2

                row_cells = table.rows[row].cells
                barcode_cell_first = row_cells[column].paragraphs[0]
                barcode_pr_first = barcode_cell_first.add_run()

                row_cells = table.rows[row+1].cells
                barcode_cell_second = row_cells[column].paragraphs[0]
                barcode_pr_second = barcode_cell_second.add_run()
                
                barcode_pr_second.add_picture(utils.image2file_bytes(barcode_png), width=Cm(5.82))
                barcode_pr_first.add_picture(utils.image2file_bytes(barcode_png), width=Cm(5.82))

                barcode_cell_first.alignment = WD_ALIGN_PARAGRAPH.CENTER
                barcode_cell_second.alignment = WD_ALIGN_PARAGRAPH.CENTER

                descriptions -= 1
                column += 1
            del self.STICKERS_ALONE[uid]

        filepath = f"userdata/{uid}/stickers_{utils.uuid_gen()}.docx"
        document.save(filepath)
        logging.info(f"USER (id: {uid}) GENERATED STICKERS SUCCESSFULLY")
        return filepath