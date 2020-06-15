"""
Functions for filtering typosquatting-related lists

A module that contains all functions that filter data related to typosquatting
data.
"""

import Levenshtein

# Key constants
MAX_DISTANCE = 1  # Edit distance threshold to determine typosquatting status
MIN_LEN_PACKAGE_NAME = 5  # Minimum length of package name to be included for analysis


def filterByPackageNameLen(package_list, min_len=MIN_LEN_PACKAGE_NAME):
    """
	Filter out package names whose length in characters is
	greater than a specified minimum length

	INPUTS:
	--package_list: a list of package names
	--min_len: a specific minimum length of characters

	OUTPUTS:
	--filtered_package_list: filtered list of package names
	"""

    # Loop thru packages and add package if name's
    # length is greater than or equal to specified min length
    filtered_package_list = []
    for package in package_list:
        if len(package) >= min_len:
            filtered_package_list.append(package)

    return filtered_package_list


def distanceCalculations(top_package, all_packages, max_distance=MAX_DISTANCE):
    """ Find all packages within a defined edit distance

	INPUTS:
	--top_package: package name to perform comparison
	--all_packages: list of all package names
	--max_distance: the maximum distance that justifies reporting

	OUTPUTS:
	--close_package_names: list of potential typosquatters
	"""

    # Empty list to store similar package names
    close_package_names = []

    # Loop thru all package names
    for package in all_packages:

        # Skip if the package IS the same as top_package
        if package == top_package:
            continue

        # Calculate distance
        distance = Levenshtein.distance(top_package, package)

        # If distance is sufficiently close, add to list
        if distance <= max_distance:
            close_package_names.append(package)

    return close_package_names


def whitelist(squat_candidates, whitelist_filename="whitelist.txt"):
    """ Remove whitelisted packages from typosquat candidate list

	Using packages listed in the whitelist_filename file, remove all
	potential typosquatters that are found in the whitelist, a list of
	known good packages.

	INPUT:
	--squat_candidates: dict of packages and potential typosquatters
	--whitelist_filename: file location for whitelist

	OUPUT:
	--dict of packages and post-whitelist potential typosquatters
	"""

    # Create whitelist
    whitelist = []
    with open(whitelist_filename, "r") as file:
        for line in file:
            # Strip out end of line character
            whitelist.append(line.strip("\n"))

    # Remove packages contained in whitelist from dict of
    # top packages (keys) and potential typosquatters (values)
    for pkg in squat_candidates:  # loop thru pkg's
        new_squat_candidates = []
        for candidate in squat_candidates[pkg]:
            # Only keep candidates NOT on whitelist
            if candidate not in whitelist:
                new_squat_candidates.append(candidate)
        # Update typosquat candidate list
        squat_candidates[pkg] = new_squat_candidates

    return squat_candidates
