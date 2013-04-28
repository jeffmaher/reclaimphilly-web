import re

def is_number(anObject):
    """
    Checks to see if the passed object is 
    a number or not. If it is, then True is returned.
    Otherwise, False is returned.
    """
    try:
        float(anObject)
        return True
    except:
        return False
       
def is_street_address(anObject):
	try:
		if re.match("^[\w\s,.-]*$", anObject):
			return True
		return False
	except:
		return False