from cohost.models.user import User
from cohost.models.block import MarkdownBlock
from datetime import datetime

import secrets
from filenames import FILENAMES
from pathlib import Path
from secrets import COHOST_USERNAME, COHOST_PW


BASE_URL = 'https://archive.org/download/bippobeppo/'
COHOST_PAGE = 'rats'
TAGS = ['bippo and/or beppo the rat', 'ratposting', 'rat', 'rats', 'automated post', 'The Cohost Bot feed']
FILENAMES = sorted(FILENAMES)
MAX = len(FILENAMES)
CURRENT_INDEX_FILE = 'index.txt'


def get_current_file_index() -> int:
    """Get what index in list FILENAMES we should post next"""
    if not Path.exists(Path(CURRENT_INDEX_FILE)):
        print(f'{datetime.now()}\t0\tERROR: Cant find current index file: {CURRENT_INDEX_FILE}')
        exit(1)

    with open(CURRENT_INDEX_FILE, 'r') as f:
        current_index = f.read()
        current_index = current_index.strip()

        if not current_index.isdigit():
            print(f'{datetime.now()}\t0\tERROR: Current index file should only contain a positive integer. Contains: {current_index}')

        current_index = int(current_index)
        if current_index < 0:
            print(f'{datetime.now()}\t0\tERROR: Current index int must be >= 0')

        if current_index > MAX:
            current_index = 0

        return current_index


def post_to_cohost(file: str):
    url = f'{BASE_URL}{file}'
    user = User.login(COHOST_USERNAME, COHOST_PW)
    project = user.getProject(COHOST_PAGE)
    new_post = project.post(
        headline="It's a little guy!",
        blocks=[MarkdownBlock(url)],
        tags=TAGS,
    )
    # Print TSV data for logging
    print(f'{datetime.now()}\t{file}\t{new_post.url}')


def increment_index(index: int):
    with open(CURRENT_INDEX_FILE, 'w') as f:
        f.write(str(index + 1))


def main():
    index = get_current_file_index()
    file = FILENAMES[index]
    post_to_cohost(file)
    increment_index(index)


if __name__ == '__main__':
    main()
