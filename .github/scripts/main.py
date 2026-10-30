import argparse
import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    bbox = draw.textbbox((0, 0), text=text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def get_github_contributions(username, year):
    url = f'https://github-contributions-api.jogruber.de/v4/{username}?y={year}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from GitHub: {response.status_code}")

    body = response.json()
    return [(contribution['date'], contribution['level']) for contribution in body['contributions']]

def get_month_positions(contributions):
    month_positions = {}
    week = 0
    for i, (date, _) in enumerate(contributions):
        dt = datetime.strptime(date, '%Y-%m-%d')
        day = (dt.weekday() + 1) % 7
        if i > 0 and day == 0:
            week += 1
        if dt.day == 1:
            month_positions[dt.month] = week
    return month_positions

def draw_grid(draw, grid, cell_size, legend_width, y_offset, colors):
    for week in range(len(grid)):
        for day in range(len(grid[0])):
            color = colors[grid[week][day]]
            x0 = week * cell_size + legend_width
            y0 = day * cell_size + y_offset
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            padding = 1.5
            draw.rounded_rectangle(
                [x0 + padding, y0 + padding, x1 - padding, y1 - padding],
                radius=3,
                fill=color
            )

def draw_legend(draw, cell_size, legend_width, y_offset, image_width, image_height, username, year, month_positions, font, font_credits):
    text_color = (125, 133, 144)

    # 1. Draw Year top-left
    draw.text((8, 6), f"{year}", fill=text_color, font=font)

    # 2. Draw Month names accurately aligned with their starting week column
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for month_num, week_col in month_positions.items():
        if 1 <= month_num <= 12:
            x = week_col * cell_size + legend_width
            draw.text((x, 6), months[month_num - 1], fill=text_color, font=font)

    # 3. Draw Day names vertically centered with cell rows
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i, day in enumerate(days):
        bbox = draw.textbbox((0, 0), day, font=font)
        text_height = bbox[3] - bbox[1]
        y = i * cell_size + y_offset + (cell_size - text_height) // 2 - bbox[1]
        draw.text((8, y), day, fill=text_color, font=font)

    # 4. Clean footer credits seamlessly blended with background
    credits_text = f"@{username} - Credits: DEBBAWEB"
    tw, th = textsize(credits_text, font=font_credits)
    credits_x = image_width - tw - 12
    credits_y = image_height - th - 8
    draw.text((credits_x, credits_y), credits_text, fill=text_color, font=font_credits)

def create_tetris_gif(username, year, contributions, output_path):
    width = 53  # 53 weeks
    height = 7  # 7 days per week
    cell_size = 20
    legend_width = 44
    y_offset = 25
    image_width = width * cell_size + legend_width + 10  # 1114px
    image_height = height * cell_size + y_offset + 25   # 190px

    colors = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353']
    background_color = '#0d1117'

    try:
        font = ImageFont.truetype(".github/scripts/Roboto-Regular.ttf", 12)
        font_credits = ImageFont.truetype(".github/scripts/Roboto-Regular.ttf", 11)
    except IOError:
        font = ImageFont.load_default()
        font_credits = font

    month_positions = get_month_positions(contributions)

    frames = []
    grid = [[0] * height for _ in range(width)]
    week = 0

    for i, (date, level) in enumerate(contributions):
        dt = datetime.strptime(date, '%Y-%m-%d')
        day = (dt.weekday() + 1) % 7
        if i > 0 and day == 0:
            week += 1

        value = min(level, 4)

        if value > 0:
            for step in range(day + 1):
                img = Image.new('RGB', (image_width, image_height), background_color)
                draw = ImageDraw.Draw(img)
                draw_legend(draw, cell_size, legend_width, y_offset, image_width, image_height, username, year, month_positions, font, font_credits)
                draw_grid(draw, grid, cell_size, legend_width, y_offset, colors)

                # Draw falling block
                x0 = week * cell_size + legend_width
                y0 = step * cell_size + y_offset
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                padding = 1.5
                draw.rounded_rectangle(
                    [x0 + padding, y0 + padding, x1 - padding, y1 - padding],
                    radius=3,
                    fill=colors[value]
                )

                frames.append(img)

            grid[week][day] = value
        else:
            grid[week][day] = 0

    # Add pause at the end (120 frames * 20ms = 2.4s pause to admire the completed calendar)
    if frames:
        last_frame = frames[-1]
        frames.extend([last_frame] * 120)

    # Save as animated GIF
    frames[0].save(output_path, save_all=True, append_images=frames[1:], optimize=False, duration=20, loop=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a GitHub contributions Tetris GIF.')
    parser.add_argument('-u', '--username', type=str, required=True, help='GitHub username')
    parser.add_argument('-y', '--year', type=int, default=datetime.now().year, help='Year for contributions')

    args = parser.parse_args()

    try:
        contributions = get_github_contributions(args.username, args.year)
        create_tetris_gif(args.username, args.year, contributions, 'assets/tetris.gif')
        print("GIF created successfully!")
    except Exception as e:
        print(e)
