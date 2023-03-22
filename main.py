import datetime
import os

INPUT_IMAGE_PATH = os.environ.get("INPUT_IMAGE_PATH", "image.txt")

COMMIT_COUNT_MAP = {
    0: 0,
    1: 1,
    2: 5,
    3: 8,
    4: 10
}


def hoist_nested_lists(lst):
    """ Takes a list of lists
        Returns a list of list where:
        for each sublist nX the i element is extracted and placed in the returned list at index i
        [[n1[0],n2[0] ... ], [n1[1],n2[1],... ]
        Examples:
        [[0,1],[0,1]] -- returns --> [[0,0],[1,1]]
        [[1,3],[2,4]] -- returns --> [[1,2],[3,4]]
    """
    return [list(a) for a in list(zip(*lst))]


def calculate_commit_count() -> int:
    """
    Calculates the required commit count for today
    Using the data in the INPUT_IMAGE_PATH
    Always begins drawing on the first Monday after the file_last_updated timestamp of the INPUT_IMAGE_PATH
    This is to ensure drawing begins on a top left square
    :return:
    """
    current_day = datetime.datetime.utcnow().date()

    with open(INPUT_IMAGE_PATH, 'r') as image:
        img_data = image.read().split('\n')
        # We process the output from top to bottom instead of left to right so we reorder the input here to match
        img_data_ordered = hoist_nested_lists(img_data)
        # Convert the input date to a big str representing the output order
        img_data_ordered_str = "".join(["".join(x) for x in img_data_ordered])

    image_created_date = datetime.datetime.fromtimestamp(os.path.getmtime(INPUT_IMAGE_PATH))

    # We use the file modified date timestamp for the expected image to calculate the start day to begin drawing
    # This is the closest Monday after the file created date
    # Monday == 0 ... Sunday == 6
    file_created_day = image_created_date.weekday()
    print("file_created_day: ", file_created_day)
    # We always start at Monday. If this file was created on a Monday we always wait until the following Monday to
    # being to
    # Ensure image is drawn correctly
    days_before_file_create_began = 7 - file_created_day
    file_begin_creating_date = (image_created_date + datetime.timedelta(days=days_before_file_create_began)).date()
    print("Starting file creation on: ", file_begin_creating_date)
    # file_begin_creating_date is the date we expect output via commits to begin
    # Get the distance between today and that date
    offset = (current_day - file_begin_creating_date).days
    print("Offset: ", offset)
    if offset < 0:
        return 0

    # Loop over the image to allow continuous printing. Starts drawing the image again after completion
    looped_offset = offset % len(img_data_ordered_str)
    # The commit count [more = darker color] required for this day is fetched and returned
    required_commit_count = img_data_ordered_str[looped_offset:looped_offset + 1]
    print("required_commit_count: ", required_commit_count)
    # It appears colors on github contributions change every 3 commits so we scale up the commits here
    required_commit_count = COMMIT_COUNT_MAP[int(required_commit_count)]
    return required_commit_count


if __name__ == '__main__':
    commit_count = calculate_commit_count()
    print(commit_count)
    with open("commit_count", "w") as commit_count_file:
        commit_count_file.write(str(commit_count))
