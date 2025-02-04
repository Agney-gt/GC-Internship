import mimetypes
import config


def get_extensions_for_type():
    """
    Returns a set of file extensions for the general MIME types excluded in the config.
    """
    return_list = set()
    general_type = set(config.EXCLUDED_URL_EXTENSIONS)

    # Iterate over mime types and check if the type matches the general type in the config
    for ext, mime_type in mimetypes.types_map.items():
        if mime_type.split('/')[0] in general_type:
            return_list.add(ext.lower())

    return return_list


# Getting the list of excluded media extensions from the config
media_extensions_list = get_extensions_for_type()
