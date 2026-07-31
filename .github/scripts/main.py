import argparse
import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def get_github_contributions(username, year):
    url = f'https://github-contributions-api.jogruber.de/v4/{username}?y={year}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from GitHub: {response.status_code}")

    body = response.json()

    return [(contribution['date'], contribution['count']) for contribution in body['contributions']]

def draw_grid(draw, grid, cell_size, colors):
    for week in range(len(grid)):
        for day in range(len(grid[0])):
            color = colors[grid[week][day]]
            x0, y0 = week * cell_size + 40, day * cell_size + 20
            x1, y1 = x0 + cell_size, y0 + cell_size
            # Separation & Rounding
            padding = 1.5
            draw.rounded_rectangle([x0 + padding, y0 + padding, x1 - padding, y1 - padding], radius=3, fill=color)

def draw_legend(draw, cell_size, image_width, image_height, username, year):
    try:
        font = ImageFont.truetype(".github/scripts/Roboto-Regular.ttf", 11)
    except IOError:
        font = ImageFont.load_default()

    # Draw day names
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i, day in enumerate(days):
        y = i * cell_size + 20
        draw.text((5, y), day, fill=(125, 133, 144), font=font)

    # Draw month names
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_positions = {1: 0, 2: 4, 3: 8, 4: 12, 5: 16, 6: 20, 7: 24, 8: 28, 9: 32, 10: 36, 11: 40, 12: 44}
    for month, week in month_positions.items():
        x = week * cell_size + 40
        draw.text((x, 5), months[month - 1], fill=(125, 133, 144), font=font)

    # Draw GitHub username and year in top left
    text = f"{year}"
    draw.text((5, 5), text, fill=(125, 133, 144), font=font)

    # Add black bar below months with "Credits: DEBBAWEB" aligned to the right
    legend_width = 40
    bar_height = 20
    bar_y = image_height - bar_height  # Position at the bottom of the image
    draw.rectangle([legend_width, bar_y, image_width, image_height], fill=(0, 0, 0))

    credits_text = f"@{username} - Credits: DEBBAWEB"
    font = ImageFont.load_default()  # Load default font
    text_width, text_height = textsize(credits_text, font=font)  # Calculate text size
    text_x = image_width - text_width - 5
    text_y = bar_y + (bar_height - text_height) // 2
    draw.text((text_x, text_y), credits_text, fill=(255, 255, 255), font=font)  # Draw text with specified font

def create_tetris_gif(username, year, contributions, output_path):
    width = 53  # 53 weeks
    height = 7  # 7 days per week
    cell_size = 20
    legend_width = 40
    image_width = width * cell_size + legend_width
    image_height = height * cell_size + 40  # Increased to accommodate legend and credits bar

    colors = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353']
    background_color = '#0d1117'  # GitHub dark background color

    frames = []
    grid = [[0] * height for _ in range(width)]

    for i, (date, count) in enumerate(contributions):
        week = i // 7
        day = i % 7
        value = min(count, 4)  # Limit max count to 4 for colors

        if value > 0:
            for v in range(1, value + 1):
                for step in range(day + 1):
                    # We can animate every step but maybe skip some to keep file size reasonable
                    img = Image.new('RGB', (image_width, image_height), background_color)
                    draw = ImageDraw.Draw(img)
                    draw_legend(draw, cell_size, image_width, image_height, username, year)
                    draw_grid(draw, grid, cell_size, colors)

                    # Draw moving block
                    x0, y0 = week * cell_size + legend_width, step * cell_size + 20
                    x1, y1 = x0 + cell_size, y0 + cell_size
                    padding = 1.5
                    draw.rounded_rectangle(
                        [x0 + padding, y0 + padding, x1 - padding, y1 - padding],
                        radius=3,
                        fill=colors[v]
                    )

                    frames.append(img)
                
                # After drop finishes, update grid
                grid[week][day] = v
        else:
            grid[week][day] = 0

    # Save as animated GIF (faster duration)
    frames[0].save(output_path, save_all=True, append_images=frames[1:], optimize=False, duration=30, loop=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a GitHub contributions Tetris GIF.')
    parser.add_argument('-u', '--username', type=str, required=True, help='GitHub username')
    parser.add_argument('-y', '--year', type=int, default=datetime.now().year, help='Year for contributions')

    args = parser.parse_args()

    try:
        contributions = get_github_contributions(args.username, args.year)
        create_tetris_gif(args.username, args.year, contributions, f'assets/tetris.gif')
        print("GIF created successfully!")
    except Exception as e:
        print(e)
