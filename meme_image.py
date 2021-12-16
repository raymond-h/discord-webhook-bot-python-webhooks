from urllib.request import urlopen
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image
import requests
from io import BytesIO
import math

def image_with_padding(in_img, padding_x, padding_y):
    out = Image(width=in_img.width + padding_x*2, height=in_img.height + padding_y*2)
    with Drawing() as ctx:
        ctx.composite('src', padding_x, padding_y, in_img.width, in_img.height, in_img)
        ctx.draw(out)
    return out

def draw_text_centered(ctx: Drawing, img: Image, text: str, x: int, y: int):
    metrics = ctx.get_font_metrics(img, text)
    w, h = (metrics.text_width, metrics.text_height)
    ctx.text(int(x - w // 2), int(y + h // 2), text)

def add_polar(x, y, magnitude, angle):
    return (x + math.cos(angle) * magnitude, y + math.sin(angle) * magnitude)

def vector_addition(x1, y1, x2, y2):
    return (x1 + x2, y1 + y2)

size_1_pattern = [False, False, False, False, False, False]
size_2_pattern = [False, True, False, False, False, True, False, False, False, True, False, False]

def get_hexagon_vertices(start_x, start_y, start_angle, side_length, pattern):
    x, y = start_x, start_y
    angle = start_angle
    result = [(start_x, start_y)]

    pi_3rd = math.pi / 3

    for turn_left in pattern:
        result.append((x, y))

        x, y = add_polar(x, y, side_length, angle)
        angle += (-pi_3rd) if turn_left else pi_3rd

    return result

def get_polygon_aabb(polygon):
    return (
        min(x for (x, _) in polygon),
        min(y for (_, y) in polygon),
        max(x for (x, _) in polygon),
        max(y for (_, y) in polygon)
    )

def draw_lancer_pog_outline(ctx: Drawing, center_x, center_y, side_length: int, pattern):
    ctx.push()

    vertices = get_hexagon_vertices(0, 0, math.pi / 6, side_length, pattern)
    left, top, right, bottom = get_polygon_aabb(vertices)
    current_center_x = left + (right - left) / 2
    current_center_y = top + (bottom - top) / 2
    offset_x = center_x - current_center_x
    offset_y = center_y - current_center_y
    vertices = [vector_addition(x, y, offset_x, offset_y) for (x, y) in vertices]

    ctx.polygon(vertices)

    ctx.pop()

def make_image(image_url):
    img_data = requests.get(image_url)

    with Image(blob=img_data.content) as img:
        with Drawing() as draw:
            draw.fill_color = Color('red')
            draw.font_size = 20.0
            # draw_text_centered(draw, img, 'mudders', img.width // 2, img.height // 2)
            draw.draw(img)

        img.save(filename='image.png')

    pass

if __name__ == "__main__":
    lancer_pog_mask_img = Image(width=1024, height=1024)
    with Drawing() as ctx:
        ctx.fill_color = Color('black')
        side_length_for_size = int(256 / math.sqrt(3))
        draw_lancer_pog_outline(ctx, 512, 512+128, side_length_for_size, size_2_pattern)

        ctx.fill_color = Color('red')
        ctx.point(512, 512)

        ctx.draw(lancer_pog_mask_img)

    lancer_pog_mask_img.save(filename='lancer_size-2_mask.png')

    # lancer_pog_outline_img = Image(width=512, height=512)
    # with Drawing() as ctx:
    #     ctx.fill_color = Color('transparent')
    #     ctx.stroke_color = Color('black')
    #     ctx.stroke_width = 10
    #     draw_lancer_pog_outline(ctx, 256, 256, 120, size_2_pattern)
    #     ctx.draw(lancer_pog_outline_img)

    # img_name = 'mudkip'
    # with Image(filename=img_name + '.png') as chara_img:
    #     with image_with_padding(chara_img, 40, 40) as padded_chara_img:
    #         with Drawing() as ctx:
    #             ctx.composite('dst_over', 0, 0, padded_chara_img.width, padded_chara_img.height, lancer_pog_mask_img)
    #             ctx.composite('dst_in', 0, 0, padded_chara_img.width, padded_chara_img.height, lancer_pog_mask_img)
    #             ctx.composite('src_over', 0, 0, padded_chara_img.width, padded_chara_img.height, lancer_pog_outline_img)
    #             ctx.draw(padded_chara_img)

    #         padded_chara_img.save(filename=img_name + '-out.png')
