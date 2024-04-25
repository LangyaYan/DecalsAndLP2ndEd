import easyocr
import string
import re
reader = easyocr.Reader(['en'],gpu=False)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}




def compliesFormat(text):
    """
    Check if the license plate text complies with the required format.

    Args:
        text (str): License plate text.

    Returns:
        bool: True if the license plate complies with the format, False otherwise.
    """

    if len(text) != 7:
        return False

    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
       (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
       (text[2] in string.ascii_uppercase or text[2] in dict_int_to_char.keys()) and \
       (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
       (text[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[4] in dict_char_to_int.keys()) and \
       (text[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[5] in dict_char_to_int.keys()) and \
       (text[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[6] in dict_char_to_int.keys()):
        return True
    else:
        return False

def format(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.

    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """
    pattern = r'[^a-zA-Z0-9\s]'
    removed = re.sub(pattern, '', text)
    lp_=''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 2: dict_int_to_char,
               3: dict_char_to_int, 4: dict_char_to_int,5: dict_char_to_int, 6: dict_char_to_int}
    for j in [0, 1, 2, 3, 4, 5, 6]:
        if compliesFormat(removed):
            if removed[j] in mapping[j].keys():
                lp_ += mapping[j][removed[j]]
            else:
                lp_ += removed[j]
        else:
            return 'NotFound'
    return lp_

def read_lp(croppedImage):
    """
    Read the license plate text from the given cropped image.

    Args:
        license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.

    Returns:
        tuple: Tuple containing the formatted license plate text and its confidence score.
    """

    detections = reader.readtext(croppedImage)
    if len(detections) != 0:
        for detection in detections:
            bbox, text, score = detection
            text = text.upper().replace(' ', '')
            text = text.upper().replace(',', '')
            print(text)
            print(score)
            return text, score
    else:
        return "NotFound",0

def write_csv(results, output_path):
    """
    Write the results to a CSV file.

    Args:
        results (dict): Dictionary containing the results.
        output_path (str): Path to the output CSV file.
    """
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'lp_text',
                                                'lp_score', 'lp_text_score', 'decal_text',
                                                'decal_score','decal_text_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                print(results[frame_nmr][car_id])
                if 'license_plate' in results[frame_nmr][car_id].keys() and \
                   'decal' in results[frame_nmr][car_id].keys() and \
                   'lp_text' in results[frame_nmr][car_id]['license_plate'].keys() and \
                   'decal_text' in results[frame_nmr][car_id]['decal'].keys():
                    f.write('{},{},{},{},{},{},{},{}\n'.format(frame_nmr,
                                                            car_id,
                                                            results[frame_nmr][car_id]['license_plate']['lp_text'],
                                                            results[frame_nmr][car_id]['license_plate']['lp_score'],
                                                            results[frame_nmr][car_id]['license_plate']['lp_text_score'],
                                                            results[frame_nmr][car_id]['decal']['decal_text'],
                                                            results[frame_nmr][car_id]['decal']['decal_score'],
                                                            results[frame_nmr][car_id]['decal']['decal_text_score'])
                            )
        f.close()